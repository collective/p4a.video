from zope import interface
from zope import schema
from p4a.fileimage import file as p4afile
from p4a.fileimage import image as p4aimage
from p4a.video import genre

class IAnyVideoCapable(interface.Interface):
    """Any aspect of video/content capable.
    """

class IPossibleVideo(IAnyVideoCapable):
    """All objects that should have the ability to be converted to some
    form of video should implement this interface.
    """

class IVideoEnhanced(interface.Interface):
    """All objects that have their media features activated/enhanced
    should have this marker interface applied.
    """

class IVideo(interface.Interface):
    """Objects which have video information.
    """

    title = schema.TextLine(title=u'Video Title', required=False)
    description = schema.Text(title=u'Description', required=False)
    rich_description = schema.Text(title=u'Rich Text Description',
                                   required=False)
    file = p4afile.FileField(title=u'File', required=False)
    width = schema.Int(title=u'Width', required=False, readonly=False)
    height = schema.Int(title=u'Height', required=False, readonly=False)
    duration = schema.Float(title=u'Duration', required=False, readonly=False)

    video_image = p4aimage.ImageField(title=u'Video Image', required=False,
                                      preferred_dimensions=(320, 240))

    video_type = schema.TextLine(title=u'Video Type',
                                 required=True,
                                 readonly=True)

    video_author = schema.TextLine(title=u'Video Author', required=False)

class IVideoDataAccessor(interface.Interface):
    """Video implementation accessor (ie mov, wma, flv).
    """

    video_type = schema.TextLine(title=u'Video Type',
                                 required=True,
                                 readonly=True)

    def load(filename):
        pass
    def store(filename):
        pass

class IMediaPlayer(interface.Interface):
    """Media player represented as HTML.
    """

    def __call__(downloadurl, imageurl):
        """Return the HTML required to play the video content located
        at *downloadurl* with the *imageurl* representing the video.
        """

class IPossibleVideoContainer(IAnyVideoCapable):
    """Any folderish entity tha can be turned into an actual video 
    container.
    """

class IVideoContainerEnhanced(interface.Interface):
    """Any folderish entity that has had it's IVideoContainer features
    enabled.
    """

class IVideoProvider(interface.Interface):
    """Provide video.
    """
    
    video_items = schema.List(title=u'Video Items',
                              required=True,
                              readonly=True)

class IBasicVideoSupport(interface.Interface):
    """Provides certain information about video support.
    """

    support_enabled = schema.Bool(title=u'Video Support Enabled?',
                                  required=True,
                                  readonly=True)

class IVideoSupport(IBasicVideoSupport):
    """Provides full information about video support.
    """

class IMediaActivator(interface.Interface):
    """For seeing the activation status or toggling activation."""

    media_activated = schema.Bool(title=u'Media Activated',
                                  required=True,
                                  readonly=False)
