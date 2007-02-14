from zope import interface
from zope import component
from p4a.video import interfaces

from Products.CMFCore import utils as cmfutils

class WMVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl, imageurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        
        # playerurl = "%s/++resource++flashmp3player/musicplayer.swf?song_url=%s"
        url = contentobj.absolute_url()
        # mime_type = contentobj.mime_type()
        
        videoobj = interfaces.IVideo(contentobj)
        
        width = videoobj.width
        height = videoobj.height
        duration = videoobj.duration

        
        return """
        <div class="hVlog">
          <a href="%(url)s" class="hVlogTarget" type="video/x-ms-wmv" onclick="vPIPPlay(this, '', '', 'active=true, controller=true'); return false;">
              <img src="%(imageurl)s" />
              </a>
        <br />
          <a href="%(url)s" type="video/x-ms-wmv" onclick="vPIPPlay(this, '', '', 'active=true, controller=true'); return false;">
        Play WindowsMedia version</a>
        </div>        
        """ % {'url': url, 'imageurl': imageurl}