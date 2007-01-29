from zope import interface
from zope import component
from p4a.audio import interfaces

from Products.CMFDynamicViewFTI import interfaces as cmfdynifaces

class AudioContainerDynamicViews(object):
    
    interface.implements(cmfdynifaces.IDynamicallyViewable)
    component.adapts(interfaces.IAudioContainerEnhanced)

    def __init__(self, context):
        self.context = context # Actually ignored...
        
    def getAvailableViewMethods(self):
        """Get a list of registered view method names
        """
        return [view for view, name in self.getAvailableLayouts()]

    def getDefaultViewMethod(self):
        """Get the default view method name
        """
        return "audio-container.html"

    def getAvailableLayouts(self):
        """Get the layouts registered for this object.
        """        
        return (("audio-container.html", "Audio view"),)
