#!/usr/bin/env python

import os, time
import commands
import pexpect

# Move the path to the location of the current file
os.chdir(os.sys.path[0])

class ShripPackage(object):
	def __init__(self):
		self._name = 'shrip'
		self._section = 'graphics'
		self._priority = 'optional'
		self._author = 'Olivier Rolland <billl@users.sf.net>'
		self._copyright = 'Copyright (C) 2004-2008 Olivier Rolland'
		self._packager = 'Matthew Brennan Jones <mattjones@workhorsy.org>'
		self._homepage = 'http://ogmrip.sourceforge.net'
		self._license = 'GPL'

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

		self._long_description = "shrip is an application and a set of libraries for ripping and encoding\n" + \
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

	def get_name(self): return self._name
	def set_name(self, value): self._name = value
	name = property(get_name, set_name)

	def get_section(self): return self._section
	def set_section(self, value): self._section = value
	section = property(get_section, set_section)

	def get_priority(self): return self._priority
	def set_priority(self, value): self._priority = value
	priority = property(get_priority, set_priority)

	def get_author(self): return self._author
	def set_author(self, value): self._author = value
	author = property(get_author, set_author)

	def get_copyright(self): return self._copyright
	def set_copyright(self, value): self._copyright = value
	copyright = property(get_copyright, set_copyright)

	def get_packager(self): return self._packager
	def set_packager(self, value): self._packager = value
	packager = property(get_packager, set_packager)

	def get_homepage(self): return self._homepage
	def set_homepage(self, value): self._homepage = value
	homepage = property(get_homepage, set_homepage)

	def get_license(self): return self._license
	def set_license(self, value): self._license = value
	license = property(get_license, set_license)

	def get_build_requirements(self): return self._build_requirements
	def set_build_requirements(self, value): self._build_requirements = value
	build_requirements = property(get_build_requirements, set_build_requirements)

	def get_install_requirements(self): return self._install_requirements
	def set_install_requirements(self, value): self._install_requirements = value
	install_requirements = property(get_install_requirements, set_install_requirements)

	def get_short_description(self): return self._short_description
	def set_short_description(self, value): self._short_description = value
	short_description = property(get_short_description, set_short_description)

	def get_long_description(self): return self._long_description
	def set_long_description(self, value): self._long_description = value
	long_description = property(get_long_description, set_long_description)

	def to_hash(self):
		return { 'name' : self._name,
				'section' : self._section,
				'priority' : self._priority,
				'author' : self.author,
				'copyright' : self.copyright,
				'packager' : self.packager,
				'homepage' : self.homepage,
				'license' : self.license,
				'build_requirements' : self.build_requirements,
				'install_requirements' : self.install_requirements,
				'short_description' : self.short_description,
				'long_description' : self.long_description}

	def build(self):
		self.configure_make_install()

package = ShripPackage()

licenses = { 'GPL' : \
"""    This package is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this package; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

On Debian systems, the complete text of the GNU General
Public License can be found in `/usr/share/common-licenses/GPL'."""
}

# Uncompress the source code
commands.getoutput("tar xzf shrip_0.4.1.orig.tar.gz")
os.chdir("shrip-0.4.1")

# Set the environmental variables fro dh_make
os.environ['DEBFULLNAME'] = "Matthew Brennan Jones"
os.environ['DEBEMAIL'] = "mattjones@workhorsy.org"

# Run dh_make
command = 'bash -c "dh_make -s -c gpl -f ../shrip_0.4.1.orig.tar.gz"'
child = pexpect.spawn(command)

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

still_reading = True
while still_reading:
	result = child.expect(expected_lines)

	if result >= 0 and result <= 7:
		pass
	elif result == 8:
		child.sendline('')
	elif result == 10:
		still_reading = False

child.close()

# Remove the unnessesary debian files
os.chdir("debian")
commands.getoutput('rm *.ex *.EX dirs docs info README.Debian copyright')

# Create the copyright file
f = open('copyright', 'w')

f.write(\
"""This package was debianized by %(packager)s on 
%(timestring)s.

It was downloaded from %(homepage)s

Upstream Author(s):

    %(author)s

Copyright:

    %(copyright)s

License:

%(license_text)s

The Debian packaging is (C) %(year)s, %(packager)s and
is licensed under the %(license)s, see above.
""" % 
{ 'name' : package._name, 
'section' : package._section, 
'priority' : package._priority, 
'author' : package.author, 
'copyright' : package.copyright, 
'packager' : package.packager, 
'homepage' : package.homepage, 
'license' : package.license, 
'build_requirements' : package.build_requirements, 
'install_requirements' : package.install_requirements, 
'short_description' : package.short_description, 
'long_description' : package.long_description,
'year' : time.strftime("%Y", time.localtime()),
'timestring' : time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime()),
'license_text' : licenses['GPL'],
})

f.close()



