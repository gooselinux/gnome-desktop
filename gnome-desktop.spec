%define libxml2_version 2.4.20
%define gtk2_version 2.11.3
%define glib2_version 2.15.4
%define libgnomeui_version 2.2.0
%define libgnomecanvas_version 2.0.0
%define startup_notification_version 0.5
%define gnome_doc_utils_version 0.3.2
%define gtk_doc_version 1.9

%define po_package gnome-desktop-2.0

Summary: Shared code among gnome-panel, gnome-session, nautilus, etc
Name: gnome-desktop
Version: 2.28.2
Release: 8%{?dist}
URL: http://www.gnome.org
Source0: http://download.gnome.org/sources/gnome-desktop/2.28/%{name}-%{version}.tar.bz2
Patch1: concatenate-edid-descriptors.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=597874
Patch2: randr-gamma.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599914
Patch3: ignore-xrandr-badmatch.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=147808
Patch4: per-monitor-background.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=601753
Patch5: slideshow.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=606456
Patch6: gnome-desktop-crash.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=606457
Patch7: randr-version.patch
# upstream fix
Patch8: width-for-height.patch
# updated translations
# https://bugzilla.redhat.com/show_bug.cgi?id=589200
Patch9: gnome-desktop-translations.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=582564
# https://bugzilla.gnome.org/show_bug.cgi?id=621046
Patch10: fix-detect-displays.patch

License: GPLv2+ and LGPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: redhat-menus
Requires: pycairo
Requires: pygtk2
Requires: gnome-python2-gnome

Obsoletes: gnome-core gnome-core-devel
Provides: gnome-core

# Make sure to update libgnome schema when changing this
Requires: system-logos

BuildRequires: gnome-common
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libgnomecanvas-devel >= %{libgnomecanvas_version}
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: gnome-doc-utils >= %{gnome_doc_utils_version}
BuildRequires: scrollkeeper
BuildRequires: gettext
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: automake autoconf libtool intltool

%description

The gnome-desktop package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop, and also some data files and other shared components of the
GNOME user environment.

%package devel
Summary: Libraries and headers for libgnome-desktop
License: LGPLv2+
Group: Development/Libraries
Requires: %name = %{version}-%{release}

Requires: libxml2-devel >= %{libxml2_version}
Requires: gtk2-devel >= %{gtk2_version}
Requires: glib2-devel >= %{glib2_version}
Requires: libgnomeui-devel >= %{libgnomeui_version}
Requires: libgnomecanvas-devel >= %{libgnomecanvas_version}
Requires: startup-notification-devel >= %{startup_notification_version}
Requires: gnome-doc-utils >= %{gnome_doc_utils_version}
Requires: pkgconfig
Requires: gtk-doc >= %{gtk_doc_version}

%description devel
Libraries and header files for the GNOME-internal private library
libgnomedesktop.

%prep
%setup -q
%patch1 -p1 -b .concatenate-edid-descriptors
%patch2 -p1 -b .randr-gamma
%patch3 -p1 -b .ignore-xrandr-badmatch
%patch4 -p1 -b .per-monitor-background
%patch5 -p1 -b .slideshow
%patch6 -p1 -b .crash
%patch7 -p1 -b .randr-version
%patch8 -p1 -b .width-for-height
%patch9 -p1 -b .translations
%patch10 -p1 -b .fix-detect-displays

%build
%configure --with-gnome-distributor="Red Hat, Inc" \
	   --with-pnp-ids-path="/usr/share/hwdata/pnp.ids" \
	   --disable-scrollkeeper
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# stuff we don't want
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%find_lang %{po_package} --all-name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_datadir}/applications/gnome-about.desktop
%{_datadir}/gnome-about
%{_datadir}/pixmaps/*
%{_datadir}/omf/*
%doc %{_mandir}/man*/*
# GPL
%{_bindir}/gnome-about
# LGPL
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%doc %{_datadir}/gtk-doc/html/gnome-desktop/

%changelog
* Thu Jul 08 2010 Ray Strode <rstrode@redhat.com> 2.28.2-8
- Fix XError problem in previous patch
  Resolves: #610239

* Tue Jun 08 2010 Ray Strode <rstrode@redhat.com> 2.28.2-7
- Hide randr events from "Detect Displays" button from g-s-d's
  autoconfiguration logic
  Resolves: #582564

* Mon May 10 2010 Matthias Clasen <mclasen@redhat.com> 2.28.2-6
- Updated translations
Resolve: #589200

* Wed Apr 21 2010 Matthias Clasen <mclasen@redhat.com> 2.28.2-5
- Fix a typo that can cause huge memory allocations
Resolves: #584494

* Wed Feb 17 2010 Ray Strode <rstrode@redhat.com> 2.28.2-4
Resolves: #565886
- Drop dep on desktop-backgrounds

* Tue Feb 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-3
- Fix a crash in the display capplet

* Tue Jan 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-2
- Fix gnome-settings-daemon crashes (#554944, #554945)

* Mon Jan  4 2010 Matthias Clasen <mclasne@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Mon Nov 23 2009 Ray Strode <rstrode@redhat.com> - 2.28.1-1
Resolves: #547731
- Update to 2.28.1 with latest patches

* Mon Nov 23 2009 Ray Strode <rstrode@redhat.com> - 2.26.3-1
- Update to 2.26.3

* Fri Aug 28 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.26.1-6
- Bump for rebuild

* Fri May 29 2009 Ray Strode <rstrode@redhat.com> 2.26.1-5
- Update default background requires

* Wed Apr 29 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-4
- Remove debug spew

* Wed Apr 29 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-3
- Fix needle/haystack confusion causing most monitors to be 'Unknown'

* Tue Apr 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-2
- Fix a case of disappearing rotations (#497515)

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/gnome-desktop/2.26/gnome-desktop-2.26.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Mar 10 2009 Ray Strode <rstrode@redhat.com> - 2.25.92-1
- Change default backgrounds to leonidas ones

* Tue Mar  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-2
- Fix the Detect Monitors button

* Thu Feb 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Mon Jan 19 2009 Ray Strode <rstrode@redhat.com> - 2.25.5-2
- Rebuild so i can chain-build

* Mon Jan 19 2009 Ray Strode <rstrode@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Tue Jan  6 2009 Ray Strode <rstrode@redhat.com> - 2.25.3-3
- Stop cross fade before freeing pixmaps in finalize instead
  of after.

* Tue Dec 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.3-2
- Update to 2.25.3

* Fri Dec  5 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-4
- Fix leak in previous update (bug 468339)

* Thu Dec  4 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-3
- Rebase fade-in patch to latest from upstream report

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-2
- Update to 2.25.2

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1.1-4
- Install gnome-bg-crossfade.h

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1.1-3
- Update to 2.25.1.1

* Thu Nov  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-5
- Require gnome-python2-gnome (#469938)

* Tue Oct 28 2008 Ray Strode <rstrode@redhat.com> - 2.24.1-4
- Take Requires: solar-backgrounds from libgnome so KDE
  spin doesn't pull it in (Requested by Rex).

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> - 2.24.1-3
- Don't leak memory when crossfading if nautilus is disabled
  (bug 468339)

* Fri Oct 24 2008 Ray Strode <rstrode@redhat.com> - 2.24.1-2
- properly initialize variable in gnome_bg_get_pixmap_from_root
  (bug 460758)

* Wed Oct 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-9
- Fix icon flicker at start of cross fade

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-8
- consoliate window repaint code to one place
- Lengthen duration of animation if getting to the first frame
  takes a long time.

* Wed Oct 15 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-7
- Add new api for getting the root window pixmap
- Pass start window to crossfade "finished" signal

* Tue Oct 14 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-6
- Hold off on settings daemon cross fade if nautilus is going
  to do it anyway.  Grab the server while getting the initial
  pixmap source and target to prevent BadDrawable race

* Sun Oct 12 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-5
- Don't crossfade between frames on a slideshow

* Fri Oct 10 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-4
- Try to address bug 465699 by throttling animation frames
  to X server.  May revert if it ends up making animation
  choppy for a lot of people.

* Wed Sep 24 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-3
- make bg crossfade animation .75 seconds instead of .5

* Wed Sep 24 2008 Soren Sandmann <sandmann@redhat.com> - 2.24.0-2
- Make clone-modes.patch work again

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep 22 2008 Ray Strode <rstrode@redhat.com> - 2.23.92-5
- s/animatins/animations/ yes there's deja vu here

* Mon Sep 22 2008 Ray Strode <rstrode@redhat.com> - 2.23.92-4
- Add some flush calls to make transition smoother

* Thu Sep 18 2008 Ray Strode <rstrode@redhat.com> - 2.23.92-3
- s/animatins/animations/

* Thu Sep 18 2008 Ray Strode <rstrode@redhat.com> - 2.23.92-2
- Add new api for doing desktop background change transition

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Thu Sep  4 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-4
- Fix bug 461152

* Wed Sep  3 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-3
- Bump release number to make chain-build work

* Wed Sep  3 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-2
- Add patch to move clone mode enumeration to gnome-rr.c

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-5
- Plug more memory leaks

* Fri Aug 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-4
- Plug a memory leak

* Mon Aug 25 2008 Adam Jackson <ajax@redhat.com> 2.23.90-3
- gnome-desktop-2.23.90-eedid.patch: Allow E-EDID blocks.

* Sat Aug 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-2
- Require enough python to make gnome-about work

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-2
- Remove a long-obsolete patch

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Wed Jun  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.3-1
- Update to 2.23.3
- Removed patches that are upstream

* Wed May 14 2008 Jon McCann <jmccann@redhat.com> - 2.23.2-0.2008.05.14.1
- Update to 2.23.2 snapshot

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Tue Apr 8 2008 Soren Sandmann <sandmann@redhat.com> - 2.22.1-2
- Fix bug where the dpi of the screen got miscalculated

* Mon Apr 7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Tue Apr 5 2008 Soren Sandmann <sandmann@redhat.com> - 2.22.0-6
- Update randr code

* Fri Apr  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-5
- Fix some logic errors wrt to caching of slideshows that
  may cause nautilus crashes

* Sat Mar 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-4
- Handle slideshow start times in the future correctly

* Wed Mar 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-3
- Fix mistranslations that cause gnome-about to crash 
  in some locales (el, mk)

* Tue Mar 20 2008 Soren Sandmann <sandmann@redhat.com> - 2.22.0-2
- Update randr code

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Sun Mar  2 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.92-3
- Update randr code with more display manufacturers.

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-2
- Fix a bug in the multires patch

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Sun Feb 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-8
- Support multi-resolution backgrounds

* Wed Feb 20 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.91-7
* Update randr code

* Tue Feb 19 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-6
- Fix a possible crash in the background code

* Fri Feb 15 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.91-5
* Update randr code

* Wed Feb 13 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.91-4
- Update randrwrap

* Wed Feb 13 2008 Ray Strode <rstrode@redhat.com> - 2.21.91-3
- Get rid of gnome-vfs BuildRequires

* Tue Feb 12 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.91-2
- Add monitor-db.[ch]

* Tue Feb 12 2008 Soren Sandmann <sandmann@redhat.com> 
- Update randrwrap

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Mon Feb 4 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.90-5
- Update randrwrap - add rotations.

* Thu Jan 29 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.90-3
- Update randrwrap.

* Thu Jan 29 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.90-3
- Update randrwrap.

* Tue Jan 29 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.5-2
- uncomment stuff from gnome-common in configure.in

* Tue Jan 29 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.5-2
- Don't buildrequire gtk-doc
- Install randrwrap.h

* Tue Jan 29 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.5-2
- Add randrwrap.[ch]

* Tue Jan 29 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.5-2
- BuildRequire gtk-doc >= 1.9

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (bug fixes and translation updates)

* Thu Sep 27 2007 Ray Strode <rstrode@redhat.com> - 2.20.0-3
- remove seemingly unneccessary dep on redhat-artwork

* Wed Sep 26 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Fix a memory leak

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92 (translation updates)

* Fri Aug 31 2007 Soren Sandmann <sandmann@redhat.com> - 2.19.90-7
- Plug a leak in the slideshow parser

* Wed Aug 29 2007 Soren Sandmann <sandmann@redhat.com> - 2.19.90-6
- Delete cache on URI switch. Various cleanups.

* Wed Aug 29 2007 Soren Sandmann <sandmann@redhat.com> - 2.19.90-5
- Fix unbounded caching. Bug 247943.

* Tue Aug 28 2007 Soren Sandmann <sandmann@redhat.com> - 2.19.90-4
- Change starttime format to be timezone relative.

* Fri Aug 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-3
- Try harder to get size information

* Fri Aug 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-2
- Fix a problem with transitions in thumbnails of slideshows

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-3
- Use %%find_lang for help files

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2
- Update license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Sun Jul  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3.1-1
- Update to 2.19.3.1

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Fri Mar 23 2007 Soren Sandmann <sandmann@redhat.com> - 2.18.0-4
- Remove debug spew - add file caching - delete totally_obscures function.

* Tue Mar 20 2007 Soren Sandmann <sandmann@redhat.com> - 2.18.0-3
- Fix a bug where only parts of the background pixmap would be drawn.

* Mon Mar 19 2007 Soren Sandmann <sandmann@redhat.com> - 2.18.0-2
- Add GnomeBG class.

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Sun Jan 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90
- Drop some long-obsolete images
- Clean up BuildRequires

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92
- Require pkgconfig in the -devel package

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15-90-1.fc6
- Update to 2.15.90
- Don't ship static libraries

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.2-1.1
- rebuild

* Tue May 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Mon Apr 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1.1-2
- Update to 2.14.1.1

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Tue Feb 28 2006 Karsten Hopp <karsten@redhat.de> 2.13.92-2
- BuildRequires: gnome-doc-utils

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Jan 28 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90

* Tue Jan 16 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-1
- Update to 2.13.5

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.4-1
- Update to 2.13.4

* Wed Dec 14 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.3-1
- Update to 2.13.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.2-1
- Update to 2.13.2

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 2.11.90-2
- rebuild for new cairo

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.90-1
- Update to 2.11.90

* Sat Jul  9 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.4-1
- Update to 2.11.4

* Mon May 23 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-5
- Let's try this gettext patch one more time--maybe, just
  maybe, I'll get it right this time (bug 155659).

* Wed May 16 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-4
- run gettext initialization routines on startup (bug 155659)
  (use right patch).

* Thu May  5 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-3
- Revert previous patch--it was wrong(bug 155659).

* Wed May  4 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-2
- run gettext initialization routines on startup (bug 155659).

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> - 2.10.0-1
- Update to upstream version 2.10.0

* Wed Mar  2 2005 Mark McLoughlin <markmc@redhat.com> 2.9.91-3
- Rebuild with gcc4

* Mon Feb 21 2005 Than Ngo <than@redhat.com> 2.9.91-2
- gnome-about only in GNOME-menu

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> 2.9.91-1
- Update to 2.9.91

* Fri Feb  4 2005 Matthias Clasen <mclasen@redhat.com> 2.9.90.1-1
- Update to 2.9.90.1

* Tue Oct 12 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0-3
- Add tamil translation

* Wed Sep 29 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0-2
- Add some new icons from upstream

* Tue Sep 21 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0-1
- Update to 2.8.0

* Mon Aug 30 2004 Mark McLoughlin <markmc@redhat.com> 2.7.92-1
- Update to 2.7.92

* Wed Aug 18 2004 Mark McLoughlin <markmc@redhat.com> 2.7.91-1
- Update to 2.7.91

* Wed Aug  4 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-1
- Update to 2.7.90

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 17 2004 Warren Togami <wtogami@redhat.com> 2.6.0.1-2
- #111123 BR scrollkeeper gettext, some minor cleanups

* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0.1-1
- Update to 2.6.0.1

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.5.91-1
- Update to 2.5.91

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Mark McLoughlin <markmc@redhat.com> 2.5.90-1
- Update to 2.5.90
- Remove hack to get rid of GNOME_COMPILE_WARNINGS and
  use --disable-compile-warnings instead.
- Package the (L)GPL/FDL and gnome-feedback docs

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.3-1
- Update to 2.5.3

* Wed Sep 10 2003 Jonathan Blandford <jrb@redhat.com> 2.4.0-1
- 2.4.0

* Wed Aug 27 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-1
- update to 2.3.7

* Thu Aug 14 2003 Alexander Larsson <alexl@redhat.com> 2.3.6.1-1
- update to gnome 2.3

* Mon Jul 28 2003 Havoc Pennington <hp@redhat.com> 2.2.2-2
- libtoolize
- rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 2.2.2-1
- 2.2.2
- remove now-upstream patch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 17 2003 Havoc Pennington <hp@redhat.com> 2.2.0.1-4
- fix mem corruption #84361

* Fri Feb 14 2003 Havoc Pennington <hp@redhat.com> 2.2.0.1-3
- nuke Xft buildreq

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 2.2.0.1-2
- require startup-notification 0.5, just for paranoia

* Wed Feb  5 2003 Alexander Larsson <alexl@redhat.com>
- 2.2.0.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Jonathan Blandford <jrb@redhat.com>
- require startup-notification

* Tue Jan 14 2003 Alexander Larsson <alexl@redhat.com> 2.1.90-2
- Change the fallback kde theme name from hicolor to crystalsvg.

* Thu Jan  9 2003 Havoc Pennington <hp@redhat.com> 2.1.90-1
- 2.1.90

* Sat Dec 14 2002 Havoc Pennington <hp@redhat.com>
- 2.1.4

* Tue Dec  3 2002 Havoc Pennington <hp@redhat.com>
- add gconftool-2 prereq

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- remove bad post (we no longer include a schemas file)

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- 2.1.3

* Wed Nov 13 2002 Havoc Pennington <hp@redhat.com>
- 2.1.2

* Wed Sep  4 2002 Havoc Pennington <hp@redhat.com>
- support a magic flag in icon theme to avoid using 
  prescaled icons

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- put in a schema so we default the the right icon theme
- fill in gnome-version.xml stuff #71445

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- 2.0.6 final for gnome 2.0.1

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.0.5

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- 2.0.3.90 cvs snap, should fix failure to launch symlink desktop
  files

* Wed Jun 26 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.2, fix missing po files

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- also obsolete gnome-core-devel
- require redhat-artwork and redhat-menus
- build require Xft/fontconfig

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- add post/postun ldconfig

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.5.22

* Fri May 31 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 31 2002 Havoc Pennington <hp@redhat.com>
- 1.5.21

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment
- build requires libgnome

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- 1.5.20
- provides gnome-core

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.5.18

* Tue Apr 16 2002 Havoc Pennington <hp@redhat.com>
- Initial build.
