# Copyright 2006 Joe Wreschnig <piman@sacredchao.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# $Id: m4a.py 3775 2006-08-09 21:38:41Z piman $

"""Read and write MPEG-4 video files with iTunes metadata.

This module will read MPEG-4 video information and metadata,
as found in Apple's M4A (aka MP4, M4B, M4P) files.

There is no official specification for this format. The source code
for TagLib, FAAD, and various MPEG specifications at
http://developer.apple.com/documentation/QuickTime/QTFF/,
http://www.geocities.com/xhelmboyx/quicktime/formats/mp4-layout.txt,
and http://wiki.multimedia.cx/index.php?title=Apple_QuickTime were all
consulted.

This module does not support 64 bit atom sizes, and so will not
work on metadata over 4GB.
"""

import struct
import sys

from cStringIO import StringIO

from mutagen import FileType, Metadata
from mutagen._constants import GENRES
from mutagen._util import cdata, DictMixin, insert_bytes, delete_bytes

class error(IOError): pass
class M4AMetadataError(error): pass
class M4AStreamInfoError(error): pass
class M4AMetadataValueError(ValueError, M4AMetadataError): pass

# This is not an exhaustive list of container atoms, but just the
# ones this module needs to peek inside.
_CONTAINERS = ["moov", "udta", "trak", "mdia", "meta", "ilst",
               "stbl", "minf", "stsd"]
_SKIP_SIZE = { "meta": 4 }

__all__ = ['M4A', 'Open', 'delete']

class Atom(object):
    """An individual atom.

    Attributes:
    children -- list child atoms (or None for non-container atoms)
    length -- length of this atom, including length and name
    name -- four byte name of the atom, as a str
    offset -- location in the constructor-given fileobj of this atom

    This structure should only be used internally by Mutagen.
    """

    children = None

    def __init__(self, fileobj):
        self.offset = fileobj.tell()
        self.length, self.name = struct.unpack(">I4s", fileobj.read(8))
        if self.length == 1:
            raise error("64 bit atom sizes are not supported")
        elif self.length < 8:
            return

        if self.name in _CONTAINERS:
            self.children = []
            fileobj.seek(_SKIP_SIZE.get(self.name, 0), 1)
            while fileobj.tell() < self.offset + self.length:
                self.children.append(Atom(fileobj))
        else:
            fileobj.seek(self.offset + self.length, 0)

    def render(name, data):
        """Render raw atom data."""
        try:
            return struct.pack(">I4s", len(data) + 8, name) + data
        except OverflowError:
            return struct.pack(">I4sQ", 1, name, len(data) + 16) + data
    render = staticmethod(render)

    def __getitem__(self, remaining):
        """Look up a child atom, potentially recursively.

        e.g. atom['udta', 'meta'] => <Atom name='meta' ...>
        """
        if not remaining:
            return self
        elif self.children is None:
            raise KeyError("%r is not a container" % self.name)
        for child in self.children:
            if child.name == remaining[0]:
                return child[remaining[1:]]
        else:
            raise KeyError, "%r not found" % remaining[0]

    def __repr__(self):
        klass = self.__class__.__name__
        if self.children is None:
            return "<%s name=%r length=%r offset=%r>" % (
                klass, self.name, self.length, self.offset)
        else:
            children = "\n".join([" " + line for child in self.children
                                  for line in repr(child).splitlines()])
            return "<%s name=%r length=%r offset=%r\n%s>" % (
                klass, self.name, self.length, self.offset, children)

class Atoms(object):
    """Root atoms in a given file.

    Attributes:
    atoms -- a list of top-level atoms as Atom objects

    This structure should only be used internally by Mutagen.
    """
    def __init__(self, fileobj):
        self.atoms = []
        fileobj.seek(0, 2)
        end = fileobj.tell()
        fileobj.seek(0)
        while fileobj.tell() < end:
            self.atoms.append(Atom(fileobj))

    def path(self, *names):
        """Look up and return the complete path of an atom.

        For example, atoms.path('moov', 'udta', 'meta') will return a
        list of three atoms, corresponding to the moov, udta, and meta
        atoms.
        """
        path = [self]
        for name in names:
            path.append(path[-1][name,])
        return path[1:]

    def __getitem__(self, names):
        """Look up a child atom.

        'names' may be a list of atoms (['moov', 'udta']) or a string
        specifying the complete path ('moov.udta').
        """
        if isinstance(names, basestring):
            names = names.split(".")
        for child in self.atoms:
            if child.name == names[0]:
                return child[names[1:]]
        else:
            raise KeyError, "%s not found" % names[0]

    def __repr__(self):
        return "\n".join([repr(child) for child in self.atoms])

class M4ATags(Metadata):
    """Dictionary containing Apple iTunes metadata list key/values.

    Keys are four byte identifiers, except for freeform ('----')
    keys. Values are usually unicode strings, but some atoms have a
    special structure:
        cpil -- boolean
        trkn, disk -- tuple of 16 bit ints (current, total)
        tmpo -- 16 bit int
        covr -- raw str data
        gnre -- not supported. Use '\\xa9gen' instead.

    The freeform '----' frames use a key in the format '----:mean:name'
    where 'mean' is usually 'com.apple.iTunes' and 'name' is a unique
    identifier for this frame. The value is a str, but is probably
    text that can be decoded as UTF-8.

    M4A tag data cannot exist outside of the structure of an M4A file,
    so this class should not be manually instantiated.

    Unknown non-text tags are removed.
    """

    def load(self, atoms, fileobj):
        try: ilst = atoms["moov.udta.meta.ilst"]
        except KeyError, key:
            raise M4AMetadataError(key)
        for atom in ilst.children:
            fileobj.seek(atom.offset + 8)
            data = fileobj.read(atom.length - 8)
            parse = self.__atoms.get(atom.name, (M4ATags.__parse_text,))[0]
            parse(self, atom, data)

    def __key_sort((key1, v1), (key2, v2)):
        # iTunes always writes the tags in order of "relevance", try
        # to copy it as closely as possible.
        order = ["\xa9nam", "\xa9ART", "\xa9wrt", "\xa9alb",
                 "\xa9gen", "gnre", "trkn", "disk",
                 "\xa9day", "cpil", "tmpo", "\xa9too",
                 "----", "covr", "\xa9lyr"]
        order = dict(zip(order, range(len(order))))
        last = len(order)
        # If there's no key-based way to distinguish, order by length.
        # If there's still no way, go by string comparison on the
        # values, so we at least have something determinstic.
        return (cmp(order.get(key1[:4], last), order.get(key2[:4], last)) or
                cmp(len(v1), len(v2)) or cmp(v1, v2))
    __key_sort = staticmethod(__key_sort)

    def save(self, filename):
        """Save the metadata to the given filename."""
        values = []
        items = self.items()
        items.sort(self.__key_sort)
        for key, value in items:
            render = self.__atoms.get(
                key[:4], (None, M4ATags.__render_text))[1]
            values.append(render(self, key, value))
        data = Atom.render("ilst", "".join(values))

        # Find the old atoms.
        fileobj = file(filename, "rb+")
        try:
            atoms = Atoms(fileobj)

            moov = atoms["moov"]

            if moov != atoms.atoms[-1]:
                # "Free" the old moov block. Something in the mdat
                # block is not happy when its offset changes and it
                # won't play back. So, rather than try to figure that
                # out, just move the moov atom to the end of the file.
                offset = self.__move_moov(fileobj, moov)
            else:
                offset = 0

            try:
                path = atoms.path("moov", "udta", "meta", "ilst")
            except KeyError:
                self.__save_new(fileobj, atoms, data, offset)
            else:
                self.__save_existing(fileobj, atoms, path, data, offset)
        finally:
            fileobj.close()

    def __move_moov(self, fileobj, moov):
        fileobj.seek(moov.offset)
        data = fileobj.read(moov.length)
        fileobj.seek(moov.offset)
        free = Atom.render("free", "\x00" * (moov.length - 8))
        fileobj.write(free)
        fileobj.seek(0, 2)
        # Figure out how far we have to shift all our successive
        # seek calls, relative to what the atoms say.
        old_end = fileobj.tell()
        fileobj.write(data)
        return old_end - moov.offset

    def __save_new(self, fileobj, atoms, ilst, offset):
        hdlr = Atom.render("hdlr", "\x00" * 8 + "mdirappl" + "\x00" * 9)
        meta = Atom.render("meta", "\x00\x00\x00\x00" + hdlr + ilst)
        moov, udta = atoms.path("moov", "udta")
        insert_bytes(fileobj, len(meta), udta.offset + offset + 8)
        fileobj.seek(udta.offset + offset + 8)
        fileobj.write(meta)
        self.__update_parents(fileobj, [moov, udta], len(meta), offset)

    def __save_existing(self, fileobj, atoms, path, data, offset):
        # Replace the old ilst atom.
        ilst = path.pop()
        delta = len(data) - ilst.length
        fileobj.seek(ilst.offset + offset)
        if delta > 0:
            insert_bytes(fileobj, delta, ilst.offset + offset)
        elif delta < 0:
            delete_bytes(fileobj, -delta, ilst.offset + offset)
        fileobj.seek(ilst.offset + offset)
        fileobj.write(data)
        self.__update_parents(fileobj, path, delta, offset)

    def __update_parents(self, fileobj, path, delta, offset):
        # Update all parent atoms with the new size.
        for atom in path:
            fileobj.seek(atom.offset + offset)
            size = cdata.uint_be(fileobj.read(4)) + delta
            fileobj.seek(atom.offset + offset)
            fileobj.write(cdata.to_uint_be(size))

    def __render_data(self, key, flags, data):
        data = struct.pack(">2I", flags, 0) + data
        return Atom.render(key, Atom.render("data", data))

    def __parse_freeform(self, atom, data):
        try:
            fileobj = StringIO(data)
            mean_length = cdata.uint_be(fileobj.read(4))
            # skip over 8 bytes of atom name, flags
            mean = fileobj.read(mean_length - 4)[8:]
            name_length = cdata.uint_be(fileobj.read(4))
            name = fileobj.read(name_length - 4)[8:]
            value_length = cdata.uint_be(fileobj.read(4))
            # Name, flags, and reserved bytes
            value = fileobj.read(value_length - 4)[12:]
        except struct.error:
            # Some ---- atoms have no data atom, I have no clue why
            # they actually end up in the file.
            pass
        else:
            self["%s:%s:%s" % (atom.name, mean, name)] = value
    def __render_freeform(self, key, value):
        dummy, mean, name = key.split(":", 2)
        mean = struct.pack(">I4sI", len(mean) + 12, "mean", 0) + mean
        name = struct.pack(">I4sI", len(name) + 12, "name", 0) + name
        value = struct.pack(">I4s2I", len(value) + 16, "data", 0x1, 0) + value
        final = mean + name + value
        return Atom.render("----", mean + name + value)

    def __parse_pair(self, atom, data):
        self[atom.name] = struct.unpack(">2H", data[18:22])
    def __render_pair(self, key, value):
        track, total = value
        if 0 <= track < 1 << 16 and 0 <= total < 1 << 16:
            data = struct.pack(">4H", 0, track, total, 0)
            return self.__render_data(key, 0, data)
        else:
            raise M4AMetadataValueError("invalid numeric pair %r" % (value,))

    def __render_pair_no_trailing(self, key, value):
        track, total = value
        if 0 <= track < 1 << 16 and 0 <= total < 1 << 16:
            data = struct.pack(">3H", 0, track, total)
            return self.__render_data(key, 0, data)
        else:
            raise M4AMetadataValueError("invalid numeric pair %r" % (value,))

    def __parse_genre(self, atom, data):
        # Translate to a freeform genre.
        genre = cdata.short_be(data[16:18])
        if "\xa9gen" not in self:
            try: self["\xa9gen"] = GENRES[genre - 1]
            except IndexError: pass

    def __parse_tempo(self, atom, data):
        self[atom.name] = cdata.short_be(data[16:18])
    def __render_tempo(self, key, value):
        if 0 <= value < 1 << 16:
            return self.__render_data(key, 0x15, cdata.to_ushort_be(value))
        else:
            raise M4AMetadataValueError("invalid short integer %r" % value)

    def __parse_compilation(self, atom, data):
        try: self[atom.name] = bool(ord(data[16:17]))
        except TypeError: self[atom.name] = False

    def __render_compilation(self, key, value):
        return self.__render_data(key, 0x15, chr(bool(value)))

    def __parse_cover(self, atom, data):
        self[atom.name] = data[16:]
    def __render_cover(self, key, value):
        return self.__render_data(key, 0xD, value)

    def __parse_text(self, atom, data):
        flags = cdata.uint_be(data[8:12])
        if flags == 1:
            self[atom.name] = data[16:].decode('utf-8', 'replace')
    def __render_text(self, key, value):
        return self.__render_data(key, 0x1, value.encode('utf-8'))

    def delete(self, filename):
        self.clear()
        self.save(filename)

    __atoms = {
        "----": (__parse_freeform, __render_freeform),
        "trkn": (__parse_pair, __render_pair),
        "disk": (__parse_pair, __render_pair_no_trailing),
        "gnre": (__parse_genre, None),
        "tmpo": (__parse_tempo, __render_tempo),
        "cpil": (__parse_compilation, __render_compilation),
        "covr": (__parse_cover, __render_cover),
        }

    def pprint(self):
        values = []
        for key, value in self.iteritems():
            key = key.decode('latin1')
            try: values.append("%s=%s" % (key, value))
            except UnicodeDecodeError:
                values.append("%s=[%d bytes of data]" % (key, len(value)))
        return "\n".join(values)

class M4AInfo(object):
    """MPEG-4 stream information.

    Attributes:
    bitrate -- bitrate in bits per second, as an int
    length -- file length in seconds, as a float
    """

    bitrate = 0

    def __init__(self, atoms, fileobj):
        hdlr = atoms["moov.trak.mdia.hdlr"]
        fileobj.seek(hdlr.offset)
        if "soun" not in fileobj.read(hdlr.length):
            raise M4AStreamInfoError("track has no video data")

        mdhd = atoms["moov.trak.mdia.mdhd"]
        fileobj.seek(mdhd.offset)
        data = fileobj.read(mdhd.length)
        if ord(data[8]) == 0:
            offset = 20
            format = ">2I"
        else:
            offset = 28
            format = ">IQ"
        end = offset + struct.calcsize(format)
        unit, length = struct.unpack(format, data[offset:end])
        self.length = float(length) / unit

        try:
            atom = atoms["moov.trak.mdia.minf.stbl.stsd"]
            fileobj.seek(atom.offset)
            data = fileobj.read(atom.length)
            self.bitrate = cdata.uint_be(data[-17:-13])
        except (ValueError, KeyError):
            # Bitrate values are optional.
            pass

    def pprint(self):
        return "MPEG-4 video, %.2f seconds, %d bps" % (
            self.length, self.bitrate)

class M4A(FileType):
    """An MPEG-4 video file, probably containing AAC.

    If more than one track is present in the file, the first is used.
    Only video ('soun') tracks will be read.
    """

    def load(self, filename):
        self.filename = filename
        fileobj = file(filename, "rb")
        try:
            atoms = Atoms(fileobj)
            try: self.info = M4AInfo(atoms, fileobj)
            except StandardError, err:
                raise M4AStreamInfoError, err, sys.exc_info()[2]
            try: self.tags = M4ATags(atoms, fileobj)
            except M4AMetadataError:
                self.tags = None
            except StandardError, err:
                raise M4AMetadataError, err, sys.exc_info()[2]
        finally:
            fileobj.close()

    def add_tags(self):
        self.tags = M4ATags()

    def score(filename, fileobj, header):
        return ("ftyp" in header) + ("mp4" in header)
    score = staticmethod(score)

Open = M4A

def delete(filename):
    """Remove tags from a file."""
    M4A(filename).delete()
