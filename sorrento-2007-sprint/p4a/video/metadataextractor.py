import logging
logger = logging.getLogger('p4a.z2utils.patches')

from hachoir_parser.guess import createParser
from hachoir_metadata.metadata import extractMetadata
from hachoir_core.error import HachoirError
from hachoir_core.stream import InputStreamError

def extract(filename):
    """Extract the metadata from the media file"""
    
    filename = unicode(filename)
    
    try:
        parser = createParser(filename)
    except InputStreamError, err:
        logger.error("stream error! %s\n" % unicode(err))
    
    if not parser:
        logger.error("Unable to create parser.\n")
        return False
    try:
        metadata = extractMetadata(parser)
    except HachoirError, err:
        logger.error("stream error! %s\n" % unicode(err))

    if not metadata:
        logger.error("unable to extract metadata.\n")
        return False

    return metadata