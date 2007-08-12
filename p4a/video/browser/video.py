import Acquisition
import datetime
import urllib

from zope import event
from zope import component
from zope import interface
from zope.formlib import form
from zope.app.event import objectevent
from zope.app.i18n import ZopeMessageFactory as _
from zope.i18n import translate

from p4a.video import genre
from p4a.video import interfaces
from p4a.video.browser import media
from p4a.video.browser import widget
from p4a.videoembed import interfaces as embedifaces

from p4a.fileimage.image._widget import ImageURLWidget

from p4a.common import formatting

from Products.CMFCore import utils as cmfutils
from Products.CMFPlone import PloneMessageFactory as _

class IVideoView(interface.Interface):
    def title(): pass
    def width(): pass
    def height(): pass
    def duration(): pass
    def video_type(): pass
    def has_media_player(): pass

class VideoView(object):
    """
    """

    def __init__(self, context, request):
        self.video_info = interfaces.IVideo(context)

        mime_type = unicode(context.get_content_type())
        self.media_player = component.queryAdapter(self.video_info.file,
                                                   interfaces.IMediaPlayer,
                                                   mime_type)

    def title(self): return self.video_info.title
    def width(self): return self.video_info.width
    def height(self): return self.video_info.height
    def duration(self): return self.video_info.duration
    def video_type(self): return self.video_info.video_type
    def has_media_player(self): return self.media_player is not None

def has_contentlicensing_support(context):
    try:
        from Products import ContentLicensing
    except ImportError, e:
        return False

    try:
        cmfutils.getToolByName(context, 'portal_contentlicensing')
    except AttributeError, e:
        return False

    return True

def has_contenttagging_support(context):
    try:
        from lovely.tag import interfaces as tagifaces
    except ImportError, e:
        return False
    return component.queryUtility(tagifaces.ITaggingEngine) is not None

def has_commenting_support(context):
    return False

class VideoPageView(media.BaseMediaDisplayView):
    """Page for displaying video.
    """

    adapted_interface = interfaces.IVideo
    media_field = 'file'

    form_fields = form.FormFields(interfaces.IVideo)
    label = u'View Video Info'

    @property
    def template(self):
        return self.index

    def has_contentlicensing_support(self):
        return has_contentlicensing_support(Acquisition.aq_inner(self.context))

    def has_contenttagging_support(self):
        return has_contenttagging_support(Acquisition.aq_inner(self.context))

    def has_commenting_support(self):
        return has_commenting_support(Acquisition.aq_inner(self.context))

    def update(self):
        super(VideoPageView, self).update()
        if not interfaces.IVideo(self.context).video_type:
            self.context.plone_utils.addPortalMessage( \
                _(u'Unsupported video type'))

class PopupVideoPageView(media.BaseMediaDisplayView):
    """Page for displaying video.
    """

    adapted_interface = interfaces.IVideo
    media_field = 'file'

    form_fields = ()
    label = u'Popup Video Player'

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

class VideoEditForm(form.EditForm):
    """Form for editing video fields.
    """

    form_fields = form.FormFields(interfaces.IVideo)
    label = u'Edit Video Data'

    @form.action(_("Apply"), condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        changed = applyChanges(
            self.context, self.form_fields, data, self.adapters)
        if changed:
            attrs = objectevent.Attributes(interfaces.IVideo, *changed)
            event.notify(
                objectevent.ObjectModifiedEvent(self.context, attrs)
                )
            # TODO: Needs locale support. See also Five.form.EditView.
            self.status = _("Successfully updated")
        else:
            self.status = _('No changes')
        redirect = self.request.response.redirect
        msg = urllib.quote(translate(self.status))
        redirect(self.context.absolute_url()+\
                 '/view?portal_status_message=%s' % msg)

class VideoStreamerView(object):
    """View for streaming video file as M3U.
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
        response.setHeader('Content-Type', 'video/x-mpegurl')
        response.setHeader('Content-Disposition',
                           'attachment; filename="%s.m3u"' % file_sans_ext)
        return self.request.URL1 + '\n'


ODDEVEN = ['even', 'odd']

class VideoContainerView(object):
    """View for video containers.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._video_items = None
        self._total_length = 0

        self._build_info()

    def has_contentlicensing_support(self):
        return has_contentlicensing_support(Acquisition.aq_inner(self.context))

    def has_contenttagging_support(self):
        return has_contenttagging_support(Acquisition.aq_inner(self.context))

    def has_commenting_support(self):
        return has_commenting_support(Acquisition.aq_inner(self.context))

    def _build_info(self):
        provider = interfaces.IVideoProvider(self.context)

        # cheating here by getting file properties we need by looking
        # up context attribute which isn't in the interface contract
        self._video_items = []

        users = {}
        membership = cmfutils.getToolByName(self.context, 'portal_membership')
        for pos, x in enumerate(provider.video_items):
            contentobj = x.context
            size = 'N/A'
            if hasattr(Acquisition.aq_base(contentobj), 'getFile'):
                # a little duck typing
                filefield = contentobj.getFile()
                size = formatting.fancy_data_size(filefield.get_size())
            w = self._widget(x)
            # IVideo.duration is a float, we need an int
            duration = int(round(x.duration or 0.0))
            has_image = x.video_image is not None

            author_username = author = contentobj.Creator()
            author_info = membership.getMemberInfo(author_username)
            if author_info is not None:
                author = author_info.get('fullname', author_username)
            users[author_username] = author

            creation_time = contentobj.created()
            creation_time = datetime.date(creation_time.year(),
                                          creation_time.month(),
                                          creation_time.day())
            creation_time = formatting.fancy_date_interval(creation_time)

            if self.has_contenttagging_support():
                tagview = component.getMultiAdapter(
                    (contentobj, self.request),
                    interface=interface.Interface,
                    name=u'tag_info')
                tags = ({'name': x,
                         'url': tagview.tag_url(x) }
                        for x in tagview.contextual_tags())
            else:
                tags = []

            max_length = 30
            description = ''
            count = 0
            for c in x.context.Description():
                if c == ' ':
                    count += 1
                if count >= max_length:
                    break
                description += c

            if len(description) != len(x.context.Description()):
                description += ' ...'

            self._video_items.append( \
                {'title': x.title,
                 'content_author': author_username,
                 'content_author_name': author,
                 'url': contentobj.absolute_url(),
                 'size': size,
                 'duration': formatting.fancy_time_amount(duration),
                 'description': description,
                 'icon': contentobj.getIcon(),
                 'tags': tags,
                 'widget': w,
                 'has_image': has_image,
                 'oddeven': ODDEVEN[pos % 2],
                 'mime_type': contentobj.getContentType(),
                 'imageurlwidget': self._imageurlwidget(x),
                 'creation_time': creation_time,
                 })

            self._total_length += duration

    def _widget(self, video):
        field = interfaces.IVideo['file'].bind(video)
        w = widget.MediaPlayerWidget(field, self.request)
        return w()

    def _imageurlwidget(self, video):
        field = interfaces.IVideo['video_image'].bind(video)
        w = ImageURLWidget(field, self.request)
        return w()

    def video_items(self):
        return self._video_items

    def has_syndication(self):
        try:
            view = self.context.restrictedTraverse('@@rss.xml')
            return True
        except:
            # it's ok if this doesn't exist, just means no syndication
            return False
