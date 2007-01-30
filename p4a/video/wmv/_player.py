from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

class WMVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        
        # playerurl = "%s/++resource++flashmp3player/musicplayer.swf?song_url=%s"
        url = contentobj.absolute_url()
        # mime_type = contentobj.mime_type()
        
        return """
        <div class="hVlog" style="text-align: center">
          <a href="%(url)s" class="hVlogTarget" type="video/x-ms-wmv" onclick="vPIPPlay(this, '', '', 'active=true, controller=true'); return false;">
              <img src="http://www.plone.org/logo.jpg" /></a>
        <br />
          <a href="%(url)s" type="video/x-ms-wmv" onclick="vPIPPlay(this, '', '', 'active=true, controller=true'); return false;">
        Play WindowsMedia version</a>
        </div>        
        """ % {'url': url}