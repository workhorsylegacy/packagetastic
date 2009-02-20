#!/usr/bin/env python


import os
import commands
import pexpect

# Move the path to the location of the current file
os.chdir(os.sys.path[0])

class ShripPackage:
	def initialize(self):
		self.name = 'shrip'
		self.section = 'graphics'
		self.priority = 'optional'
		self.author = 'Olivier Rolland <billl@users.sf.net>'
		self.copyright = 'Copyright (C) 2004-2008 Olivier Rolland'
		self.packager = 'Matthew Brennan Jones <mattjones@workhorsy.org>'
		self.homepage = 'http://ogmrip.sourceforge.net'
		self.license = 'GPL'

		self.build_requirements = ["debhelper (>= 7)",
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

		self.install_requirements = ["ogmrip (>= 0.10.0)",
									"mplayer",
									"mencoder",
									"ogmtools",
									"vorbis-tools (>= 1.0)",
									"lame (>= 3.96)",
									"mkvtoolnix (>= 0.9.5)",
									"faac (>= 1.24)",
									"tesseract | ocrad | gocr",
									"gpac"]

		self.short_description = 'Application for ripping and encoding DVD into AVI/OGM files'

		self.long_description = "shrip is an application and a set of libraries for ripping and encoding\n" + \
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

os.environ['DEBFULLNAME'] = "Matthew Brennan Jones"
os.environ['DEBEMAIL'] = "mattjones@workhorsy.org"

p = ShripPackage()

commands.getoutput("tar xzf shrip_0.4.1.orig.tar.gz")
os.chdir("shrip-0.4.1")

expected_lines = ["Maintainer name : [\w|\s]*\r\n",
					"Email-Address   : [\w|\s|\@|\.]*\r\n",
					"Date            : [\w|\s|\,|\:|\-]*\r\n",
					"Package Name    : [\w|\s|\,|\:|\-]*\r\n",
					"Version         : [\w|\s|\-|\~|\.]*\r\n",
					"License         : [\w|\s|\.]*\r\n",
					"Using dpatch    : [\w|\s]*\r\n",
					"Type of Package : [\w|\s]*\r\n",
					"Hit \<enter\> to confirm:[\s]*",
					"Done. [\w|\s\W]*",
					pexpect.EOF]

command = 'bash -c "dh_make -s -c gpl -f ../shrip_0.4.1.orig.tar.gz"'
child = pexpect.spawn(command)

still_reading = True
while still_reading:
	result = child.expect(expected_lines)

	if result >= 0 and result <= 7:
		pass
	elif result == 8:
		child.sendline('')
	elif result == 10:
		still_reading = False





