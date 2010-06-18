from zope import interface
from zope import component
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils

def generate_config(config_name, **kw):
    text = '%s : {' % config_name
    for key, value in kw.items():
        if value is not None and value is not 'false' and value is not 'true':
            text += "%s: '%s', " % (key, value)
        else:
            text += "%s: %s, " % (key, value)
    if text.endswith(', '):
        text = text[:-2]
    text += ' }'
    return text

class FLVVideoPlayer(object):
    interface.implements(interfaces.IMediaPlayer)
    component.adapts(object)

    def __init__(self, context):
        self.context = context

    def __call__(self, downloadurl, imageurl, width, height):
        contentobj = self.context.context.context
        portal_tool = cmfutils.getToolByName(contentobj, 'portal_url')
        portal_url = portal_tool.getPortalObject().absolute_url()
        flow_player_base = portal_url + "/%2B%2Bresource%2B%2Bflowplayer"
        player = flow_player_base + "/flowplayer-3.2.2.swf"
        downloadurl = contentobj.absolute_url()
        title = contentobj.title
        if not (width and height):
            width = 320
            height = 240
        image_tag = ""
        if not imageurl:
            imageurl = flow_player_base + "/example/play-button-328x240.jpg"
        tag = '<img src="%s" alt="%s" height="%s" width="%s" />'
        image_tag = tag % (imageurl, title, height, width)
        # 22 is added to the height so that FlowPlayer controls fit
        height = height + 22
        config = generate_config(
            'clip',
            url=downloadurl,
            autoPlay='false',
            )
        return """
<div id="playerContainer" style="height: %(height)spx; width: %(width)spx">
</div>

<script type="text/javascript">
jq(document).ready(function() {

    flowplayer("playerContainer", {
        src: '%(player)s',

        // we need at least this version
        version: [9, 115],

        // older versions will see a custom message
        onFail: function()  {
            document.getElementById("info").innerHTML =
                "You need the latest Flash version to view MP4 movies. " +
                "Your version is " + this.getVersion()
            ;
        },
    }, {
        // here is our third argument which is the Flowplayer configuration
        %(config)s,
    });
    })
</script>
        """ % locals()
