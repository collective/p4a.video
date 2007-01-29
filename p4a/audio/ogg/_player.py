from zope import interface
from zope import component
from p4a.audio import interfaces
from Products.CMFCore import utils as cmfutils

class OggAudioPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        
        player = "%s/++resource++oggplayer/cortado-ovt-debug-0.2.1.jar" % site.absolute_url()
        
        return """
        <div class="ogg-player">
            <applet code="com.fluendo.player.Cortado.class" 
                    archive="%(player)s" 
         	        width="100" height="50">
              <param name="url" value="%(url)s"/>
              <param name="local" value="false"/>
              <param name="duration" value="00352"/>
              <param name="video" value="false"/>
              <param name="audio" value="true"/>
              <param name="bufferSize" value="200"/>
              <param name="debug" value="3" />
            </applet>
        </div>
        """ % {'player': player, 'url': downloadurl}
