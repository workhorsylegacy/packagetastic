#!/usr/bin/env python

from universal_packages import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class ShripPackage(BasePackage):
	def __init__(self):
		self._name = 'shrip'
		self._version = '0.4.1'
		self._section = 'graphics'
		self._priority = 'optional'
		self._author = 'Olivier Rolland <billl@users.sf.net>'
		self._copyright = 'Copyright (C) 2004-2008 Olivier Rolland'
		self._packager_name = 'Matthew Brennan Jones'
		self._packager_email = 'mattjones@workhorsy.org'
		self._bug_mail = 'mattjones@workhorsy.org'
		self._homepage = 'http://ogmrip.sourceforge.net'
		self._license = 'GPL'
		self._source = 'http://downloads.sourceforge.net/ogmrip/shrip-0.4.1.tar.gz'

		self._build_requirements = ["debhelper (>= 7)",
									"autotools-dev",
									"libogmrip-dev (>= 0.10.0)",
									"libdvdread-dev",
									"libhal-dev",
									"eject",
									"mplayer",
									"mencoder",
									"libenchant-dev",
									"vorbis-tools (>= 1.0)",
									"lame",
									"libgconf2-dev",
									"libglade2-dev",
									"mkvtoolnix (>= 0.9.5)",
									"libtheora-dev",
									"faac",
									"libvorbis-dev",
									"libdbus-glib-1-dev",
									"libx264-dev",
									"ogmtools",
									"libxml-parser-perl",
									"libnotify-dev-gtk2.10"]

		self._install_requirements = ["ogmrip (>= 0.10.0)",
									"mplayer",
									"mencoder",
									"ogmtools",
									"vorbis-tools (>= 1.0)",
									"lame (>= 3.96)",
									"mkvtoolnix (>= 0.9.5)",
									"faac (>= 1.24)",
									"tesseract | ocrad | gocr",
									"gpac"]

		self._short_description = 'Application for ripping and encoding DVD into AVI/OGM files'

		# FIXME: Having a one space indent on this is a Debian specific thing and should be handled by the framework instead.
		self._long_description = " shrip is an application and a set of libraries for ripping and encoding\n" + \
								" DVD into AVI, OGM MP4 or Matroska files using a wide variety of codecs. It\n" + \
								" relies on mplayer, mencoder, ogmtools, mkvtoolnix, oggenc, lame and faac to\n" + \
								" perform its tasks.\n" + \
								"  o transcodes from DVD or files\n" + \
								"  o outputs ogm, avi, matroska or mp4 files\n" + \
								"  o provides a lot of codecs (ogg vorbis, mp3, pcm, ac3, aac, dts, xvid, lavc, x264, theora)\n" + \
								"  o calculates video bitrate for a given filesize\n" + \
								"  o calculates cropping parameters and scaling factors\n" + \
								"  o uses maximum quality codec switches\n" + \
								"  o supports subtitles extraction\n" + \
								"  o rips contiguous chapters"

	def build(self):
		self.configure_make_install()



build_ubuntu(ShripPackage())

