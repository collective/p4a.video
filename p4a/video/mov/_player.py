from zope import interface
from zope import component
from p4a.audio import interfaces
from Products.CMFCore import utils as cmfutils

class MP3AudioPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        
        playerurl = "%s/++resource++flashmp3player/musicplayer.swf?song_url=%s"
        playerurl = playerurl % (site.absolute_url(), downloadurl)

        return """
        <div class="mp3-player">
            <object type="application/x-shockwave-flash"
                    data="%(playerurl)s"
                    style="margin-top: 2px"
                    width="17" 
                    height="17">
                    <param name="movie"
                           value="%(playerurl)s"
                    />
            </object>
        </div>
        """ % {'playerurl': playerurl}
