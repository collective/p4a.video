from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

class RealVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        
        # playerurl = "%s/++resource++flashmp3player/musicplayer.swf?song_url=%s"
        url = ''.join(contentobj.absolute_url(),'?embed'
        # mime_type = contentobj.mime_type()
        
        return """
        <embed href="%(url)s" name="realvideoax" controls="ImageWindow" AUTOSTART="true" console="clip1" LOOP=true height="" width="" border="0">     
        """ % {'url': url}

