from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

def generate_config(**kw):
    text = 'config={'
    for key, value in kw.items():
        if value is not None:
            text += "%s: '%s', " % (key, value)
    if text.endswith(', '):
        text = text[:-2]
    text += ' }'
    return text

class FLVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl, imageurl):
        contentobj = self.context.context.context
        portal_tool = cmfutils.getToolByName(contentobj, 'portal_url')
        portal_url = portal_tool.getPortalObject().absolute_url()

        player = portal_url + "/++resource++flowplayer/FlowPlayer.swf"
        if not imageurl:
            # must replace + with %2b so that the FlowPlayer finds the image
            imageurl = portal_url + \
                       "/%2b%2bresource%2b%2bflowplayer/play-button-328x240.jpg"
        downloadurl = contentobj.absolute_url()
        title = contentobj.title

        # how do we get the imageurl?
        #
        videoobj = interfaces.IVideo(contentobj)
        # let's make sure that we have some values
        if not videoobj.width:
            videoobj.width = 0
        if not videoobj.height:
            videoobj.height = 0
        width = videoobj.width
        # 22 is added to the height so that FlowPlayer controls fit
        height = videoobj.height + 22
        config = generate_config(videoFile=downloadurl,
                                 splashImageFile=imageurl,
                                 autoPlay='false',
                                 loop='false')

        return """
        <div class="flowplayer">
            <object type="application/x-shockwave-flash" data="%(player)s" 
            	width="%(width)s" height="%(height)s" id="FlowPlayer">
            	<param name="allowScriptAccess" value="sameDomain" />
            	<param name="movie" value="%(player)s" />
            	<param name="quality" value="high" />
            	<param name="scale" value="noScale" />
            	<param name="wmode" value="transparent" />
            	<param name="flashvars" value="%(config)s" />
            </object>
        </div>
        """ % {'player': player,
               'config': config,
               'title': title,
               'width': width,
               'height': height}

        # <div class="hVlog">
        #   <a href="" class="hVlogTarget" type="" onclick="vPIPPlay(this, '', '', ''); return false;">
        #       <img src="http://www.plone.org/logo.jpg" /></a>
        # <br />
        #   <a href="%(url)s" type="application/x-shockwave-flash" onclick="vPIPPlay(this, 'width=%(width)s, height=%(height)s, name=%(title)s, quality=High, bgcolor=#FFFFFF, revert=true, flv=true', ''FLVbuffer=15', 'active=true, caption=%(title)s'); return false;">
        # Play Flash version</a>
        # </div>
        
