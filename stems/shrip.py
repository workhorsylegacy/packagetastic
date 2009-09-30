#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'shrip'
		self._category = 'Applications/Video'
		self._priority = 'optional'
		self._authors = [u'Olivier Rolland <billl@users.sf.net>']
		self._copyright = [u'2004-2008 Olivier Rolland']
		self._homepage = 'http://ogmrip.sourceforge.net'
		self._license = 'GPL2+'
		self._source = 'http://downloads.sourceforge.net/ogmrip/shrip-0.5.0.tar.gz'

		self._build_requirements = ["libogmrip-dev (>= 0.10.0)",
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
									"libdbus-glib-dev",
									"libx264-dev",
									"ogmtools",
									"libxml-parser-perl",
									"libnotify-dev"]

		self._short_description = u'Application for ripping and encoding DVD into AVI/OGM files'

		self._long_description = u"shrip is an application and a set of libraries for ripping and encoding\n" + \
								u"DVD into AVI, OGM MP4 or Matroska files using a wide variety of codecs. It\n" + \
								u"relies on mplayer, mencoder, ogmtools, mkvtoolnix, oggenc, lame and faac to\n" + \
								u"perform its tasks.\n" + \
								u" o transcodes from DVD or files\n" + \
								u" o outputs ogm, avi, matroska or mp4 files\n" + \
								u" o provides a lot of codecs (ogg vorbis, mp3, pcm, ac3, aac, dts, xvid, lavc, x264, theora)\n" + \
								u" o calculates video bitrate for a given filesize\n" + \
								u" o calculates cropping parameters and scaling factors\n" + \
								u" o uses maximum quality codec switches\n" + \
								u" o supports subtitles extraction\n" + \
								u" o rips contiguous chapters"

		self._changelog = [ Changelog(version="0.5.0", release=2, time="Sun, 17 May 2009 05:49:14 +0000", text=u"No changes. Rebuilt for fun."), 
							Changelog(version="0.5.0", release=1, time="Sat, 16 May 2009 05:49:14 +0000", text=u"Initial release") ]

class Shrip(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'shrip'
		self._build_method = 'c library'
		self._category = 'Applications/Video'
		self._priority = 'optional'
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

		self._files = ['/usr/bin/shrip', 
						'/usr/share/man/man1/shrip.1*']

