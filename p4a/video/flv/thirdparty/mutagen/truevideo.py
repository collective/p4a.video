# True Video support for Mutagen
# Copyright 2006 Joe Wreschnig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.

"""True Video video stream information and tags.

True Video is a lossless format designed for real-time encoding and
decoding. This module is based on the documentation at
http://www.true-video.com/TTA_Lossless_Video_Codec_-_Format_Description

True Video files use ID3 tags.
"""

__all__ = ["TrueVideo", "Open", "delete"]

from mutagen.id3 import ID3FileType
from mutagen._util import cdata

class error(RuntimeError): pass
class TrueVideoHeaderError(error, IOError): pass

class TrueVideoInfo(object):
    """True Video stream information.

    Attributes:
    length - video length, in seconds
    sample_rate - video sample rate, in Hz
    """

    def __init__(self, fileobj, offset):
        fileobj.seek(offset or 0)
        header = fileobj.read(18)
        if len(header) != 18 or not header.startswith("TTA"):
            raise TrueVideoHeaderError("TTA header not found")
        self.sample_rate = cdata.int_le(header[10:14])
        samples = cdata.uint_le(header[14:18])
        self.length = float(samples) / self.sample_rate

    def pprint(self):
        return "True Video, %.2f seconds, %d Hz." % (
            self.length, self.sample_rate)

class TrueVideo(ID3FileType):
    """A True Video file."""

    _Info = TrueVideoInfo

    def score(filename, fileobj, header):
        return (header.startswith("ID3") + header.startswith("TTA") +
                filename.lower().endswith(".tta"))
    score = staticmethod(score)

Open = TrueVideo

def delete(filename):
    """Remove tags from a file."""
    TrueVideo(filename).delete()
