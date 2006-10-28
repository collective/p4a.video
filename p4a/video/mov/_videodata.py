import mimetypes
import os
from zope.app.annotation import interfaces as annointerfaces
from zope import interface
from OFS import Image as ofsimage
from p4a.video import interfaces
from p4a.fileimage import utils as fileutils

#def write_audio_image(id3tags, audio_image):
#    size = audio_image.get_size()
#    mime_type = audio_image.content_type
#    desc = u''
#
#    tempfilename = fileutils.write_to_tempfile(audio_image)
#    frame = frames.ImageFrame.create(frames.ImageFrame.FRONT_COVER, 
#                                     tempfilename,
#                                     desc)
#
#    imgs = id3tags.getImages()
#    if len(imgs) == 0:
#        id3tags.frames.append(frame)
#    else:
#        # find the frame index of the first image so we can
#        # replace it with our new image frame
#        for i in id3tags.frames:
#            if i == imgs[0]:
#                index = id3tags.frames.index(i)
#                id3tags.frames[index] = frame
#                break

class MOVVideoDataAccessor(object):
    interface.implements(interfaces.IVideoDataAccessor)
    
    def __init__(self, context):
        self._filecontent = context

    @property
    def video_type(self):
        return 'MOV'

    @property
    def _video(self):
        video = getattr(self, '__cached_video', None)
        if video is not None:
            return video
        self.__cached_video = interfaces.IVideo(self._filecontent)
        return self.__cached_video

    @property
    def _video_data(self):
        annotations = annointerfaces.IAnnotations(self._filecontent)
        return annotations.get(self._video.ANNO_KEY, None)

    def load(self, filename):
        
        self._video_data['title'] = 'foo'
        self._video_data['artist'] = 'bar'
        self._video_data['year'] = '2007'
        self._video_data['video_image'] = 'fake image'
        
        self._video_data['comment'] = 'this is a comment'

        self._video_data['bit_rate'] = '256'
        self._video_data['frequency'] = ''
        self._video_data['length'] = '5:13'

    def store(self, filename):
        content_type = self._filecontent.get_content_type()

        #id3tags = eyeD3.Tag()
        #id3tags.link(filename)
        #id3tags.setVersion(eyeD3.ID3_V2_4)
        #id3tags.setTextEncoding(eyeD3.frames.UTF_8_ENCODING)
        
        #id3tags.setTitle(self._audio.title or u'')
        #id3tags.setArtist(self._audio.artist or u'')
        #id3tags.setAlbum(self._audio.album or u'')
        #id3tags.setDate(self._audio.year or 0)
        #id3tags.setGenre(self._audio.genre)
        
        #for c in id3tags.frames['COMM']:
        #    id3tags.frames.remove(c)
        #if self._audio.comment:
        #    id3tags.addComment(self._audio.comment)
        
        # saving the image(s)
        #if self._audio.audio_image is not None:
        #    write_audio_image(id3tags, self._audio.audio_image)

        #id3tags.update(version=eyeD3.ID3_V2_4)
