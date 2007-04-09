from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

class MOVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, downloadurl, imageurl):
        contentobj = self.context.context.context    
        url = contentobj.absolute_url()
        
        return """
        <div class="hVlog" >
          <a href="%(url)s" class="hVlogTarget" type="video/quicktime" onclick="vPIPPlay(this, '', '', ''); return false;">
              <img src="%(imageurl)s" /></a>
        <br />
          <a href="%(url)s" type="video/quicktime" onclick="vPIPPlay(this, '', '', ''); return false;">
        Play Quicktime version</a>
        </div>        
        """ % {'url': url,
               'imageurl': imageurl}
        