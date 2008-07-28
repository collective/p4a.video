from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

class RealVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl, imageurl, width, height):

        if not (width and height):
            width = 320
            height = 240

        # playerurl = "%s/++resource++flashmp3player/musicplayer.swf?song_url=%s"
        url = "%s?embed" % downloadurl
        # mime_type = contentobj.mime_type()

        return """
              <embed href="%(url)s" name="realvideoax" controls="ImageWindow" AUTOSTART="true" console="clip1" LOOP=true height="%(height)s" width="%(width)s" border="0">     
              """ % {'url': downloadurl,
                     'height': height, 
                     'width': width}
        


