# This file is copied from p4a.audio. After the 1.0 release this is
# supposed to be refactored to p4a.media, but currently this is a copy
# of p4a.audio.media.py

from zope import interface
from zope import component
from p4a.video import interfaces
from p4a.common import feature

_marker = object()

class MediaActivator(object):
    """An adapter for seeing the activation status or toggling activation.
    """

    interface.implements(interfaces.IMediaActivator)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context

    _video_activated = feature.FeatureProperty(interfaces.IPossibleVideo,
                                               interfaces.IVideoEnhanced,
                                               'context')
    _video_container_activated = \
        feature.FeatureProperty(interfaces.IPossibleVideoContainer,
                                interfaces.IVideoContainerEnhanced,
                                'context')

    def media_activated(self, v=_marker):
        if v is _marker:
            if interfaces.IPossibleVideo.providedBy(self.context):
                return self._video_activated
            elif interfaces.IPossibleVideoContainer.providedBy(self.context):
                return self._video_container_activated
            return False

        if interfaces.IPossibleVideo.providedBy(self.context):
            self._video_activated = v
        elif interfaces.IPossibleVideoContainer.providedBy(self.context):
            self._video_container_activated = v

    media_activated = property(media_activated, media_activated)
