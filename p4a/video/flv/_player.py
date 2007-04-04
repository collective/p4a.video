from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

class FLVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl, imageurl):
        contentobj = self.context.context.context
        site = cmfutils.getToolByName(contentobj, 'portal_url').getPortalObject()
        
        player = "%s/++resource++flowplayer/FlowPlayer.swf" % site.absolute_url()
        
        downloadurl = contentobj.absolute_url()
        title = contentobj.title
        
        # how do we get the imageurl?
        # 
        videoobj = interfaces.IVideo(contentobj) 
        width = videoobj.width
        height = videoobj.height
                
        return """
        <div class="flowplayer">
            <object type="application/x-shockwave-flash" data="%(player)s" 
            	width="320" height="263" id="FlowPlayer">
            	<param name="allowScriptAccess" value="sameDomain" />
            	<param name="movie" value="%(player)s" />
            	<param name="quality" value="high" />
            	<param name="scale" value="noScale" />
            	<param name="wmode" value="transparent" />
            	<param name="flashvars" value="config={
            	    splashImageFile: '%(imageurl)s',
            	    videoFile: '%(url)s'}" />
            </object>
        </div>
        """ % {'player': player, 'url': downloadurl, 'imageurl': imageurl, 'title': title, 'width': width, 'height': height}

        # <div class="hVlog">
        #   <a href="" class="hVlogTarget" type="" onclick="vPIPPlay(this, '', '', ''); return false;">
        #       <img src="http://www.plone.org/logo.jpg" /></a>
        # <br />
        #   <a href="%(url)s" type="application/x-shockwave-flash" onclick="vPIPPlay(this, 'width=%(width)s, height=%(height)s, name=%(title)s, quality=High, bgcolor=#FFFFFF, revert=true, flv=true', ''FLVbuffer=15', 'active=true, caption=%(title)s'); return false;">
        # Play Flash version</a>
        # </div>
        
