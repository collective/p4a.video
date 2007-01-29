from zope import component
from zope.app.form.browser import widget
from p4a.audio import interfaces
from p4a.fileimage import file

class MediaPlayerWidget(file.FileDownloadWidget):
    """Widget which produces some form of media player.
    """
    
    def __call__(self):
        file_present = True
        if not self._data:
            file_present = False
        
        url = self.url
        if not url:
            file_present = False
        
        if not file_present:
            return widget.renderElement(u'span',
                                        cssClass='media-absent media-player',
                                        contents='No media to play')
        
        field = self.context
        contentobj = field.context.context

        mime_type = unicode(contentobj.get_content_type())
        media_player = component.queryAdapter(field,
                                              interface=interfaces.IMediaPlayer,
                                              name=mime_type)
        
        if media_player is None:
            return widget.renderElement(u'span',
                                        cssClass='player-not-available media-player',
                                        contents='No available player for mime type "%s"' % mime_type)
        
        return u"""<div class="media-player">%s</div>""" % media_player(url)
