from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

class FLVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        
        player = "%s/++resource++flowplayer/FlowPlayer.swf" % site.absolute_url()
        
        return """
        <div class="flowplayer">
            <object type="application/x-shockwave-flash" data="%(player)s" 
            	width="320" height="263" id="FlowPlayer">
            	<param name="allowScriptAccess" value="sameDomain" />
            	<param name="movie" value="%(player)s" />
            	<param name="quality" value="high" />
            	<param name="scale" value="noScale" />
            	<param name="wmode" value="transparent" />
            	<param name="flashvars" value="config={videoFile: '%(url)s'}" />
            </object>
        </div>
        """ % {'player': player, 'url': downloadurl}
