from zope import interface
from p4a.video import interfaces
from p4a.subtyper.interfaces import (IPortalTypedDescriptor,
                                     IPortalTypedFolderishDescriptor)

class VideoDescriptor(object):
    interface.implements(IPortalTypedDescriptor)

    title = u'Video'
    description = u'Video-based media content'
    type_interface = interfaces.IVideoEnhanced
    for_portal_type = 'File'

class AbstractVideoContainerDescriptor(object):
    interface.implements(IPortalTypedFolderishDescriptor)

    title = u'Video Container'
    description = u'Container for holding Video-based media content'
    type_interface = interfaces.IVideoContainerEnhanced

class FolderVideoContainerDescriptor(AbstractVideoContainerDescriptor):
    for_portal_type = 'Folder'

class TopicVideoContainerDescriptor(AbstractVideoContainerDescriptor):
    for_portal_type = 'Topic'
