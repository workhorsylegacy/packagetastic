<%doc> \
    This is a template dpkg rules file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1


# These are used for cross-compiling and for saving the configure script
# from having to guess our platform (since we know it already)
DEB_HOST_GNU_TYPE   ?= @@(shell dpkg-architecture -qDEB_HOST_GNU_TYPE)
DEB_BUILD_GNU_TYPE  ?= @@(shell dpkg-architecture -qDEB_BUILD_GNU_TYPE)
ifneq (@@(DEB_HOST_GNU_TYPE),@@(DEB_BUILD_GNU_TYPE))
CROSS= --build @@(DEB_BUILD_GNU_TYPE) --host @@(DEB_HOST_GNU_TYPE)
else
CROSS= --build @@(DEB_BUILD_GNU_TYPE)
endif



configure: configure-stamp
configure-stamp:
	dh_testdir
	touch configure-stamp
% if not uses_python:
	# Add here commands to configure the package.
ifneq "@@(wildcard /usr/share/misc/config.sub)" ""
	cp -f /usr/share/misc/config.sub config.sub
endif
ifneq "@@(wildcard /usr/share/misc/config.guess)" ""
	cp -f /usr/share/misc/config.guess config.guess
endif
	./configure @@(CROSS) ${configure_params} --prefix=/usr --mandir=\@@@@{prefix}/share/man --infodir=\@@@@{prefix}/share/info CFLAGS="@@(CFLAGS)" LDFLAGS="-Wl,-z,defs"
% endif

build: build-stamp
build-stamp: configure-stamp
	dh_testdir
	touch build-stamp
% for patch in patches:
	patch -p0 < debian/patches/${patch}
% endfor
% if uses_python:
	/usr/bin/python setup.py build
% else:
	# Add here commands to compile the package.
	@@(MAKE) ${make_params}
	#docbook-to-man debian/${name}.sgml > ${name}.1
	touch @@@
% endif

clean:
	dh_testdir
	dh_testroot
	rm -f build-stamp configure-stamp

% if uses_python:
	/usr/bin/python setup.py clean --all
% else:
	# Add here commands to clean up after the build process.
	[ ! -f Makefile ] || @@(MAKE) distclean
	rm -f config.sub config.guess
% endif

	dh_clean

install: build
	dh_testdir
	dh_testroot
	dh_prep
	dh_installdirs
	#make generators

	# Add here commands to install the package into debian/${name}.
% if uses_python:
	/usr/bin/python setup.py install --no-compile --root='debian/${name}' --install-lib=usr/share/python-support/${name}
% else:
	@@(MAKE) DESTDIR=@@(CURDIR)/debian/${name} ${install_params} install
% endif


# Build architecture-dependent files here.
% if not uses_python:
binary-arch: build install
	dh_testdir
	dh_testroot
	dh_installchangelogs #ChangeLog
	dh_installdocs
	dh_installexamples
#	dh_install
#	dh_installmenu
#	dh_installdebconf
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installpam
#	dh_installmime
#	dh_python
#	dh_installinit
#	dh_installcron
#	dh_installinfo
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
#	dh_perl
#	dh_makeshlibs
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb
% else:
binary-arch:
% endif

# Build architecture-independent files here.
% if uses_python:
binary-indep: build install
	dh_testdir
	dh_testroot
	dh_installchangelogs #ChangeLog
	dh_installdocs
	dh_installexamples
#	dh_install
#	dh_installmenu
#	dh_installdebconf
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installpam
#	dh_installmime
	dh_pysupport
#	dh_python
#	dh_installinit
#	dh_installcron
#	dh_installinfo
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
#	dh_perl
#	dh_makeshlibs
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb
% else:
binary-indep:
% endif

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install
