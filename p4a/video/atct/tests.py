import unittest
from zope import component
from zope.component import testing
from zope.testing import doctestunit

def test_suite():
    return unittest.TestSuite((
        doctestunit.DocTestSuite('p4a.video.atct._atct'),
        ))
