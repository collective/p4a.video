from zope import interface
from zope import schema
from p4a.fileimage import file as p4afile
from p4a.fileimage import image as p4aimage
from p4a.audio import genre

class IAnyAudioCapable(interface.Interface):
    """Any aspect of audio/content capable.
    """

class IPossibleAudio(IAnyAudioCapable):
    """All objects that should have the ability to be converted to some
    form of audio should implement this interface.
    """

class IAudioEnhanced(interface.Interface):
    """All objects that have their media features activated/enhanced
    should have this marker interface applied.
    """

class IAudio(interface.Interface):
    """Objects which have audio information.
    """
    
    title = schema.TextLine(title=u'Audio Title', required=False)
    file = p4afile.FileField(title=u'File', required=False)
    artist = schema.TextLine(title=u'Artist', required=False)
    album = schema.TextLine(title=u'Album', required=False)
    audio_image = p4aimage.ImageField(title=u'Audio Image', required=False,
                                      preferred_dimensions=(150, 150))
    year = schema.Int(title=u'Year', required=False)
    genre = schema.Choice(title=u'Genre', required=False, 
                          vocabulary=genre.GENRE_VOCABULARY)
    comment = schema.Text(title=u'Comment', required=False)

    variable_bit_rate = schema.Bool(title=u'Variable Bit Rate',
                                    readonly=True)
    bit_rate = schema.Int(title=u'Bit Rate',
                          readonly=True)
    frequency = schema.Int(title=u'Frequency',
                           readonly=True)
    length = schema.Int(title=u'Length',
                        readonly=True)

    audio_type = schema.TextLine(title=u'Audio Type', 
                                 required=True, 
                                 readonly=True)

class IAudioDataAccessor(interface.Interface):
    """Audio implementation accessor (ie mp3, ogg, etc).
    """
    
    audio_type = schema.TextLine(title=u'Audio Type', 
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
        """Return the HTML required to play the audio content located
        at *downloadurl*.
        """

class IPossibleAudioContainer(IAnyAudioCapable):
    """Any folderish entity tha can be turned into an actual audio 
    container.
    """

class IAudioContainerEnhanced(interface.Interface):
    """Any folderish entity that has had it's IAudioContainer features
    enabled.
    """

class IAudioProvider(interface.Interface):
    """Provide audio.
    """
    
    audio_items = schema.List(title=u'Audio Items',
                              required=True,
                              readonly=True)

class IBasicAudioSupport(interface.Interface):
    """Provides certain information about audio support.
    """

    support_enabled = schema.Bool(title=u'Audio Support Enabled?',
                                  required=True,
                                  readonly=True)

class IAudioSupport(IBasicAudioSupport):
    """Provides full information about audio support.
    """
