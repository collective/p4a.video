import mimetypes
import os
from zope.app.annotation import interfaces as annointerfaces
from zope import interface
from OFS import Image as ofsimage
from p4a.video import interfaces
from p4a.video.mp3.thirdparty import eyeD3
from p4a.video.mp3.thirdparty.eyeD3 import frames
from p4a.fileimage import utils as fileutils

def write_video_image(id3tags, video_image):
    size = video_image.get_size()
    mime_type = video_image.content_type
    desc = u''

    tempfilename = fileutils.write_to_tempfile(video_image)
    frame = frames.ImageFrame.create(frames.ImageFrame.FRONT_COVER, 
                                     tempfilename,
                                     desc)

    imgs = id3tags.getImages()
    if len(imgs) == 0:
        id3tags.frames.append(frame)
    else:
        # find the frame index of the first image so we can
        # replace it with our new image frame
        for i in id3tags.frames:
            if i == imgs[0]:
                index = id3tags.frames.index(i)
                id3tags.frames[index] = frame
                break

class MP3VideoDataAccessor(object):
    interface.implements(interfaces.IVideoDataAccessor)
    
    def __init__(self, context):
        self._filecontent = context

    @property
    def video_type(self):
        return 'MP3'

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
        id3tags = eyeD3.Tag()
        id3tags.link(filename)
        
        self._video_data['title'] = id3tags.getTitle()
        self._video_data['artist'] = id3tags.getArtist()
        self._video_data['album'] = id3tags.getAlbum()
        self._video_data['year'] = id3tags.getYear()
        
        image_frames = id3tags.getImages()
        image_frame = None
        if len(image_frames)>0:
            image_frame = image_frames[0]
        if image_frame is not None and image_frame.imageData:
            mime_type = image_frame.mimeType
            ext = mimetypes.guess_extension(mime_type) or '.jpg'
            kwargs = dict(id=os.path.basename(filename)+ext, 
                          title='', 
                          file=image_frame.imageData)
            if image_frame.mimeType:
                kwargs['content_type'] = image_frame.mimeType
            image = ofsimage.Image(**kwargs)
            self._video_data['video_image'] = image
        
        genre = id3tags.getGenre()
        if genre and genre.getId() is not None:
            self._video_data['genre'] = int(genre.getId())
        
        self._video_data['comment'] = id3tags.getComment()

        mp3_header = eyeD3.Mp3VideoFile(filename)
        variable, bit_rate = mp3_header.getBitRate()
        bit_rate = bit_rate * 1000  # id3 bit_rate info is in Kbps
        self._video_data['variable_bit_rate'] = bool(variable)
        self._video_data['bit_rate'] = bit_rate
        self._video_data['frequency'] = mp3_header.getSampleFreq()
        self._video_data['length'] = mp3_header.getPlayTime()

    def store(self, filename):
        content_type = self._filecontent.get_content_type()

        id3tags = eyeD3.Tag()
        id3tags.link(filename)
        id3tags.setVersion(eyeD3.ID3_V2_4)
        id3tags.setTextEncoding(eyeD3.frames.UTF_8_ENCODING)
        
        id3tags.setTitle(self._video.title or u'')
        id3tags.setArtist(self._video.artist or u'')
        id3tags.setAlbum(self._video.album or u'')
        id3tags.setDate(self._video.year or 0)
        id3tags.setGenre(self._video.genre)
        
        for c in id3tags.frames['COMM']:
            id3tags.frames.remove(c)
        if self._video.comment:
            id3tags.addComment(self._video.comment)
        
        # saving the image(s)
        if self._video.video_image is not None:
            write_video_image(id3tags, self._video.video_image)

        id3tags.update(version=eyeD3.ID3_V2_4)
