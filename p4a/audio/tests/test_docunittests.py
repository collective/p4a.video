import unittest
from zope import component
from zope.component import testing
from zope.testing import doctestunit

def test_suite():
    return unittest.TestSuite((
        doctestunit.DocTestSuite('p4a.audio.utils'),
        
        doctestunit.DocFileSuite('media-player.txt',
                                 package="p4a.audio",
                                 setUp=testing.setUp,
                                 tearDown=testing.tearDown),

        doctestunit.DocFileSuite('migration.txt',
                                 package="p4a.audio",
                                 setUp=testing.setUp,
                                 tearDown=testing.tearDown)
        ))
