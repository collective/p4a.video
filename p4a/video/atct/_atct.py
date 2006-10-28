import os
from OFS import Image as ofsimage

from zope import component
from zope import interface
from zope.app.event import objectevent

from p4a.video import videoanno
from p4a.video import interfaces
from p4a.video import utils

from p4a.fileimage import file as p4afile
from p4a.fileimage import utils as fileutils

from Products.ATContentTypes import interface as atctifaces  
from Products.CMFCore import utils as cmfutils

class ATCTFolderVideoProvider(object):
    interface.implements(interfaces.IVideoProvider)
    component.adapts(atctifaces.IATFolder)
    
    def __init__(self, context):
        self.context = context

    @property
    def video_items(self):
        files = []
        for x in self.context.getFolderContents(full_objects=True):
            adapted = component.queryAdapter(x, interfaces.IVideo)
            if adapted is not None:
                files.append(adapted)

        return files

class ATCTTopicVideoProvider(object):
    interface.implements(interfaces.IVideoProvider)
    component.adapts(atctifaces.IATTopic)
    
    def __init__(self, context):
        self.context = context

    @property
    def video_items(self):
        files = []
        for x in self.context.queryCatalog(full_objects=True):
            adapted = component.queryAdapter(x, interfaces.IVideo)
            if adapted is not None:
                files.append(adapted)

        return files

@interface.implementer(interfaces.IVideo)
@component.adapter(atctifaces.IATFile)
def ATCTFileVideo(context):
    if not interfaces.IVideoEnhanced.providedBy(context):
        return None
    return _ATCTFileVideo(context)

class _ATCTFileVideo(videoanno.AnnotationVideo):
    """An IVideo adapter designed to handle ATCT based file content.
    """
    
    interface.implements(interfaces.IVideo)
    component.adapts(atctifaces.IATFile)

    ANNO_KEY = 'p4a.video.atct.ATCTFileVideo'

    def _load_video_metadata(self):
        """Retrieve audio metadata from the raw file data and update
        this object's appropriate metadata fields.
        """
        
        mime_type = self.context.get_content_type()
        accessor = component.queryAdapter(self.context, 
                                          interfaces.IVideoDataAccessor,
                                          unicode(mime_type))
        if accessor is not None:
            filename = fileutils.write_ofsfile_to_tempfile(self.context.getRawFile())
            accessor.load(filename)
            os.remove(filename)

    def _save_video_metadata(self):
        """Write the audio metadata fields of this object as metadata
        on the raw file data.
        """
        
        mime_type = self.context.get_content_type()
        accessor = component.queryAdapter(self.context, 
                                          interfaces.IVideoDataAccessor,
                                          unicode(mime_type))
        if accessor is not None:
            filename = fileutils.write_ofsfile_to_tempfile(self.context.getRawFile())
            accessor.store(filename)

            zodb_file = self.context.getRawFile()
            fin = open(filename, 'rb')
            # very inefficient, loading whole file in memory upon upload
            # TODO: fix in-memory loading
            data, size = zodb_file._read_data(fin)
            zodb_file.update_data(data, mime_type, size)
            fin.close()
            
            os.remove(filename)

    @property
    def _default_charset(self):
        """The charset determined by the active Plone site to be the
        default.
        """
        
        charset = getattr(self, '__cached_default_charset', None)
        if charset is not None:
            return charset
        try:
            props = cmfutils.getToolByName(self.context, 'portal_properties')
            self.__cached_default_charset = props.site_properties.default_charset
        except:
            self.__cached_default_charset = DEFAULT_CHARSET
        return self.__cached_default_charset
        
    def _u(self, v):
        """Return the unicode object representing the value passed in an
        as error-immune manner as possible.
        """
        
        return utils.unicodestr(v, self._default_charset)

    def _get_file(self):
        return self.context.getRawFile()
    def _set_file(self, v):
        if v != interfaces.IAudio['file'].missing_value:
            self.context.getRawFile().manage_upload(file=v)
    file = property(_get_file, _set_file)

    def _get_video_image(self):
        v = self.video_data.get('video_image', None)
        if v == None or v.get_size() == 0:
            return None
        return v
    def _set_video_image(self, v):
        if v == interfaces.IVideo['video_image'].missing_value:
            return
        upload = v
        if isinstance(upload, ofsimage.Image):
            image = upload
        else:
            image = ofsimage.Image(id=upload.filename, 
                                   title=upload.filename, 
                                   file=upload)
        self.video_data['video_image'] = image
    video_image = property(_get_video_image, _set_video_image)

    @property
    def video_type(self):
        mime_type = self.context.get_content_type()
        accessor = component.getAdapter(self.context, 
                                        interfaces.IVideoDataAccessor,
                                        unicode(mime_type))
        return accessor.video_type

    def __str__(self):
        return '<p4a.video ATCTFileVideo title=%s>' % self.title
    __repr__ = __str__

def load_metadata(obj, evt):
    """An event handler for loading metadata.
    """
    
    obj._load_video_metadata()

def sync_audio_metadata(obj, evt):
    """An event handler for saving id3 tag information back onto the file.
    """
    
    audio = interfaces.IAudio(obj)
    for description in evt.descriptions:
        if isinstance(description, objectevent.Attributes):
            attrs = description.attributes
            orig = {}
            for key in attrs:
                if key != 'file':
                    orig[key] = getattr(audio, key)
            if 'file' in attrs:
                audio._load_audio_metadata()
                for key, value in orig.items():
                    setattr(audio, key, value)
    audio._save_audio_metadata()

def attempt_media_activation(obj, evt):
    """Try to activiate the media capabilities of the given object.
    """

    view = obj.restrictedTraverse('@@media-config.html')
    if view.media_activated:
        return
    
    mime_type = obj.get_content_type()
    try:
        accessor = component.getAdapter(obj, 
                                        interfaces.IVideoDataAccessor,
                                        unicode(mime_type))
    except Exception, e:
        accessor = None

    if accessor is not None:
        view.media_activated = True
        update_dublincore(obj, evt)
        update_catalog(obj, evt)

def update_dublincore(obj, evt):
    """Update the dublincore properties.
    """
    
    video = interfaces.IVideo(obj)
    obj.setTitle(video.title)
    desc = ''
    fields = [(x, interfaces.IVideo[x])
               for x in interfaces.IVideo if x != 'title']
    for name, field in fields:
        if isinstance(field, p4afile.FileField):
            continue
        value = getattr(video, name) or None
        if value is not None:
            desc += u'%s is %s\n' % (field.title, unicode(value))
    obj.setDescription(desc)

def update_catalog(obj, evt):
    """Reindex the object in the catalog.
    """

    obj.reindexObject()
