from zope import interface
from zope.formlib import form
from p4a.video import interfaces
from p4a.video import media
from p4a.video.browser import widget
from p4a.common import feature
try:
    from zope.app.annotation import interfaces as annointerfaces
except ImportError, err:
    # Zope 2.10 support
    from zope.annotation import interfaces as annointerfaces

_marker = object()

class ToggleEnhancementsView(media.MediaActivator):
    """
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        was_activated = self.media_activated
        self.media_activated = not was_activated
        response = self.request.response
        
        if was_activated:
            activated = 'Media+deactivated'
        else:
            activated = 'Media+activated'
        
        response.redirect(self.context.absolute_url() + \
                          '/view?portal_status_message='+activated)

class BaseMediaDisplayView(form.PageDisplayForm):
    """Base view for displaying media.
    """

    adapted_interface = None
    media_field = None

    def _media_player(self):
        video = self.adapters.get(self.adapted_interface,
                                  self.adapted_interface(self.context))
        field = self.adapted_interface[self.media_field].bind(video)
        player_widget = widget.MediaPlayerWidget(field, self.request)
        player_widget.name = self.prefix + 'media_player'
        player_widget._data = field.get(video)
        return player_widget
    
    def update(self):
        super(BaseMediaDisplayView, self).update()
        player_widget = self._media_player()
        self.widgets += form.Widgets([(None, player_widget)], len(self.prefix))
