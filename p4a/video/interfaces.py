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
    file = p4afile.FileField(title=u'File', required=False)
    # artist = schema.TextLine(title=u'Artist', required=False)
    # album = schema.TextLine(title=u'Album', required=False)
    # video_image = p4aimage.ImageField(title=u'Video Image', required=False,
    #                                   preferred_dimensions=(150, 150))
    # year = schema.Int(title=u'Year', required=False)
    # genre = schema.Choice(title=u'Genre', required=False, 
    #                       vocabulary=genre.GENRE_VOCABULARY)
    # comment = schema.Text(title=u'Comment', required=False)
    # 
    # variable_bit_rate = schema.Bool(title=u'Variable Bit Rate',
    #                                 readonly=True)
    # bit_rate = schema.Int(title=u'Bit Rate',
    #                       readonly=True)
    # frequency = schema.Int(title=u'Frequency',
    #                        readonly=True)
    # length = schema.Int(title=u'Length',
    #                     readonly=True)

    video_type = schema.TextLine(title=u'Video Type', 
                                 required=True, 
                                 readonly=True)

class IVideoDataAccessor(interface.Interface):
    """Video implementation accessor (ie mp3, ogg, etc).
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
    
    def __call__(downloadurl):
        """Return the HTML required to play the video content located
        at *downloadurl*.
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
