from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

class SWFVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)

    def __init__(self, context):
        self.context = context

    def __call__(self, downloadurl, imageurl):
        contentobj = self.context.context.context
        file_url = contentobj.absolute_url()+'/download'

        videoobj = interfaces.IVideo(contentobj)

        if not videoobj.width or not videoobj.height:
            return '''<div class="flas-movie no-dimensions">
            No dimensions specified for flash video
            </div>'''

        width = videoobj.width
        height = videoobj.height + 22

        return '''
<div class="flash-movie">
  <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
          codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=7,0,0,0" 
          width="%(width)s" height="%(height)s" id="Untitled-1" align="middle">
    <param name="allowScriptAccess" value="sameDomain" />
    <param name="movie" value="%(file_url)s" />
    <param name="quality" value="high" />
    <param name="bgcolor" value="#ffffff" />
    <embed src="%(file_url)s" quality="high" bgcolor="#ffffff"
           width="%(width)s" height="%(height)s" name="%(title)s"
           align="middle" allowScriptAccess="sameDomain"
           type="application/x-shockwave-flash"
           pluginspage="http://www.adobe.com/go/getflashplayer" />
  </object>
</div>
        ''' % {'file_url': file_url,
               'width': width,
               'height': height,
               'title': contentobj.Title()}
