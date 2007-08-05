import datetime
import urllib

from zope import event
from zope import component
from zope import interface
from zope.formlib import form
from zope.app.event import objectevent
from zope.app.i18n import ZopeMessageFactory as _
from zope.i18n import translate

from p4a.video import genre
from p4a.video import interfaces
from p4a.video.browser import media
from p4a.video.browser import widget

from p4a.common import formatting

from Products.CMFCore import utils as cmfutils
from Products.CMFPlone import PloneMessageFactory as _

class IVideoView(interface.Interface):
    def title(): pass
    def width(): pass
    def height(): pass
    def duration(): pass
    def video_type(): pass
    def has_media_player(): pass

class VideoView(object):
    """
    """
    
    def __init__(self, context, request):
        self.video_info = interfaces.IVideo(context)

        mime_type = unicode(context.get_content_type())
        self.media_player = component.queryAdapter(self.video_info.file,
                                                   interfaces.IMediaPlayer,
                                                   mime_type)
                                                       
    def title(self): return self.video_info.title
    def width(self): return self.video_info.width
    def height(self): return self.video_info.height
    def duration(self): return self.video_info.duration
    def video_type(self): return self.video_info.video_type
    def has_media_player(self): return self.media_player is not None
        
        
    # def genre(self): 
    #     g = self.video_info.genre
    #     if g in genre.GENRE_VOCABULARY:
    #         return genre.GENRE_VOCABULARY.getTerm(g).title
    #     return u''
    # 
    # def frequency(self): 
    #     if not self.video_info.frequency:
    #         return 'N/A'
    #     return '%i Khz' % (self.video_info.frequency / 1000)
    # 
    # def bit_rate(self): 
    #     return '%i Kbps' % (self.video_info.bit_rate / 1000)
    # 
    # def length(self):
    #     return formatting.fancy_time_amount(self.video_info.length)

class VideoPageView(media.BaseMediaDisplayView):
    """Page for displaying video.
    """

    adapted_interface = interfaces.IVideo
    media_field = 'file'

    form_fields = form.FormFields(interfaces.IVideo)
    label = u'View Video Info'

    @property
    def template(self):
        return self.index
    
    def has_contentlicensing_support(self):
        try:
            from Products import ContentLicensing
        except ImportError, e:
            return False

        try:
            cmfutils.getToolByName(self.context, 'portal_contentlicensing')
        except AttributeError, e:
            return False

        return True

    def has_contenttagging_support(self):
        try:
            from lovely.tag import interfaces as tagifaces
        except ImportError, e:
            return False
        return component.queryUtility(tagifaces.ITaggingEngine) is not None

    def update(self):
        super(VideoPageView, self).update()        
        if not interfaces.IVideo(self.context).video_type:
            self.context.plone_utils.addPortalMessage(_(u'Unsupported video type'))

class PopupVideoPageView(media.BaseMediaDisplayView):
    """Page for displaying video.
    """

    adapted_interface = interfaces.IVideo
    media_field = 'file'

    form_fields = ()
    label = u'Popup Video Player'

def applyChanges(context, form_fields, data, adapters=None):
    if adapters is None:
        adapters = {}

    changed = []

    for form_field in form_fields:
        field = form_field.field
        # Adapt context, if necessary
        interface = field.interface
        adapter = adapters.get(interface)
        if adapter is None:
            if interface is None:
                adapter = context
            else:
                adapter = interface(context)
            adapters[interface] = adapter

        name = form_field.__name__
        newvalue = data.get(name, form_field) # using form_field as marker
        if (newvalue is not form_field) and (field.get(adapter) != newvalue):
            changed.append(name)
            field.set(adapter, newvalue)

    return changed

class VideoEditForm(form.EditForm):
    """Form for editing video fields.
    """
    
    form_fields = form.FormFields(interfaces.IVideo)
    label = u'Edit Video Data'
    
    @form.action(_("Apply"), condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        changed = applyChanges(
            self.context, self.form_fields, data, self.adapters)
        if changed:
            attrs = objectevent.Attributes(interfaces.IVideo, *changed)
            event.notify(
                objectevent.ObjectModifiedEvent(self.context, attrs)
                )
            # TODO: Needs locale support. See also Five.form.EditView.
            self.status = _("Successfully updated")
        else:
            self.status = _('No changes')
        redirect = self.request.response.redirect
        msg = urllib.quote(translate(self.status))
        redirect(self.context.absolute_url()+'/view?portal_status_message=%s' % msg)
    
class VideoStreamerView(object):
    """View for streaming video file as M3U.
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        file_sans_ext = self.context.getId()
        pos = file_sans_ext.rfind('.')
        if pos > -1:
            file_sans_ext = file_sans_ext[:pos]
        
        response = self.request.response
        response.setHeader('Content-Type', 'video/x-mpegurl')
        response.setHeader('Content-Disposition', 
                           'attachment; filename="%s.m3u"' % file_sans_ext)
        return self.request.URL1 + '\n'


class VideoContainerView(object):
    """View for video containers.
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._video_items = None
        self._total_length = 0
        
        self._build_info()

    def _build_info(self):
        provider = interfaces.IVideoProvider(self.context)
        
        # cheating here by getting file properties we need by looking
        # up context attribute which isn't in the interface contract
        self._video_items = []
        
        for x in provider.video_items:
            aFile = x.context
            field = aFile.getFile()
            w = self._widget(x)
            # IVideo.duration is a float, we need an int
            duration = int(round(x.duration or 0.0))
            self._video_items.append( \
                {'title': x.title,
                 'url': aFile.absolute_url(),
                 'size': formatting.fancy_data_size(field.get_size()),
                 'duration': formatting.fancy_time_amount(duration),
                 'description': x.context.Description(),
                 'icon': aFile.getIcon(),
                 'widget': w,
                 })
            
            self._total_length += duration

    def _widget(self, video):
        field = interfaces.IVideo['file'].bind(video)
        w = widget.MediaPlayerWidget(field, self.request)
        return w()
        
    def video_items(self):
        return self._video_items
    
    # def total_length(self):
    #     return formatting.fancy_time_amount(self._total_length)

    def has_syndication(self):
        try:
            view = self.context.restrictedTraverse('@@rss.xml')
            return True
        except:
            # it's ok if this doesn't exist, just means no syndication
            return False
        
