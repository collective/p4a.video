import datetime
import urllib

from zope import event
from zope import component
from zope import interface
from zope.formlib import form
from zope.app.event import objectevent
from zope.app.i18n import ZopeMessageFactory as _
from zope.i18n import translate

from p4a.audio import genre
from p4a.audio import interfaces
from p4a.audio.browser import media
from p4a.audio.browser import widget

from p4a.common import formatting

from Products.CMFCore import utils as cmfutils

class IAudioView(interface.Interface):
    def title(): pass
    def artist(): pass
    def album(): pass
    def year(): pass
    def genre(): pass
    def comment(): pass
    def variable_bit_rate(): pass
    def bit_rate(): pass
    def frequency(): pass
    def length(): pass
    def audio_type(): pass
    def has_media_player(): pass


class AudioView(object):
    """
    """
    
    def __init__(self, context, request):
        self.audio_info = interfaces.IAudio(context)

        mime_type = unicode(context.get_content_type())
        self.media_player = component.queryAdapter(self.audio_info.file,
                                                   interfaces.IMediaPlayer,
                                                   mime_type)

    def title(self): return self.audio_info.title
    def artist(self): return self.audio_info.artist
    def album(self): return self.audio_info.album
    def year(self): return self.audio_info.year
    def comment(self): return self.audio_info.comment
    def variable_bit_rate(self): return self.audio_info.variable_bit_rate
    def audio_type(self): return self.audio_info.audio_type
    def has_media_player(self): return self.media_player is not None

    def genre(self): 
        g = self.audio_info.genre
        if g in genre.GENRE_VOCABULARY:
            return genre.GENRE_VOCABULARY.getTerm(g).title
        return u''

    def frequency(self): 
        if not self.audio_info.frequency:
            return 'N/A'
        return '%i Khz' % (self.audio_info.frequency / 1000)

    def bit_rate(self): 
        return '%i Kbps' % (self.audio_info.bit_rate / 1000)

    def length(self):
        return formatting.fancy_time_amount(self.audio_info.length)

class AudioPageView(media.BaseMediaDisplayView):
    """Page for displaying audio.
    """

    adapted_interface = interfaces.IAudio
    media_field = 'file'

    form_fields = form.FormFields(interfaces.IAudio)
    label = u'View Audio Info'
    
    def has_contentlicensing_support(self):
        try:
            from Products import ContentLicensing
        except ImportError, e:
            return False

        try:
            cmfutils.getToolByName(self.context, 'portal_contentlicensing')
        except AttributeError, e:
            return False

        return True

class PopupAudioPageView(media.BaseMediaDisplayView):
    """Page for displaying audio.
    """

    adapted_interface = interfaces.IAudio
    media_field = 'file'

    form_fields = ()
    label = u'Popup Audio Player'

def applyChanges(context, form_fields, data, adapters=None):
    if adapters is None:
        adapters = {}

    changed = []

    for form_field in form_fields:
        field = form_field.field
        # Adapt context, if necessary
        interface = field.interface
        adapter = adapters.get(interface)
        if adapter is None:
            if interface is None:
                adapter = context
            else:
                adapter = interface(context)
            adapters[interface] = adapter

        name = form_field.__name__
        newvalue = data.get(name, form_field) # using form_field as marker
        if (newvalue is not form_field) and (field.get(adapter) != newvalue):
            changed.append(name)
            field.set(adapter, newvalue)

    return changed

class AudioEditForm(form.EditForm):
    """Form for editing audio fields.
    """
    
    form_fields = form.FormFields(interfaces.IAudio)
    label = u'Edit Audio Data'
    
    @form.action(_("Apply"), condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        changed = applyChanges(
            self.context, self.form_fields, data, self.adapters)
        if changed:
            attrs = objectevent.Attributes(interfaces.IAudio, *changed)
            event.notify(
                objectevent.ObjectModifiedEvent(self.context, attrs)
                )
            # TODO: Needs locale support. See also Five.form.EditView.
            self.status = _("Successfully updated")
        else:
            self.status = _('No changes')
        redirect = self.request.response.redirect
        msg = urllib.quote(translate(self.status))
        redirect(self.context.absolute_url()+'/view?portal_status_message=%s' % msg)
    
class AudioStreamerView(object):
    """View for streaming audio file as M3U.
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        file_sans_ext = self.context.getId()
        pos = file_sans_ext.rfind('.')
        if pos > -1:
            file_sans_ext = file_sans_ext[:pos]
        
        response = self.request.response
        response.setHeader('Content-Type', 'audio/x-mpegurl')
        response.setHeader('Content-Disposition', 
                           'attachment; filename="%s.m3u"' % file_sans_ext)
        return self.request.URL1 + '\n'


class AudioContainerView(object):
    """View for audio containers.
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._audio_items = None
        self._total_length = None
        
        self._build_info()

    def _build_info(self):
        provider = interfaces.IAudioProvider(self.context)
        
        # cheating here by getting file properties we need by looking
        # up context attribute which isn't in the interface contract
        self._audio_items = []
        self._total_length = 0
        
        for x in provider.audio_items:
            aFile = x.context
            field = aFile.getFile()
            w = self._widget(x)
            self._audio_items.append( \
                {'title': x.title,
                 'url': aFile.absolute_url(),
                 'size': formatting.fancy_data_size(field.get_size()),
                 'length': formatting.fancy_time_amount(x.length),
                 'description': x.context.Description(),
                 'icon': aFile.getIcon(),
                 'widget': w,
                 })
            self._total_length += x.length

    def _widget(self, audio):
        field = interfaces.IAudio['file'].bind(audio)
        w = widget.MediaPlayerWidget(field, self.request)
        return w()
        
    def audio_items(self):
        return self._audio_items
    
    def total_length(self):
        return formatting.fancy_time_amount(self._total_length)

    def has_syndication(self):
        try:
            view = self.context.restrictedTraverse('@@rss.xml')
            return True
        except:
            # it's ok if this doesn't exist, just means no syndication
            return False
        
