%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

######################
# Hardcode PLF build
%define build_plf 0
######################

%if %{build_plf}
%define distsuffix plf
%define extrarelsuffix plf
%endif

%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A general purpose sound file conversion tool
Name:		sox
Version:	14.4.0
Release:	3%{?extrarelsuffix}
License:	LGPLv2+
Group:		Sound
URL:		http://sox.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/sox/%{name}-%{version}.tar.gz
BuildRequires:	ffmpeg-devel
BuildRequires:	magic-devel
BuildRequires:	gsm-devel
BuildRequires:	id3tag-devel
BuildRequires:	ladspa-devel
BuildRequires:	libalsa-devel
BuildRequires:	libflac-devel
BuildRequires:	libtool-devel
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	libtheora-devel
BuildRequires:	libtool
BuildRequires:	libwavpack-devel
BuildRequires:	lpc10-devel
BuildRequires:	mad-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	libgomp-devel
%if %{build_plf}
BuildRequires:	lame-devel
BuildRequires:	libamrwb-devel
BuildRequires:	libamrnb-devel
%endif

%description
SoX (Sound eXchange) is a sound file format converter for Linux,
UNIX and DOS PCs. The self-described 'Swiss Army knife of sound
tools,' SoX can convert between many different digitized sound
formats and perform simple sound manipulation functions,
including sound effects.

Install the sox package if you'd like to convert sound file formats
or manipulate some sounds.

%if %{build_plf}
This package is in restricted as it was build with lame encoder
support, which is in restricted.
%endif

%package -n %{libname}
Summary:	Libraries for SoX
Group:		System/Libraries
Obsoletes:	%{mklibname %{name} 0} < %{EVRD}

%description -n %{libname}
Libraries for SoX.

%package -n %{develname}
Summary:	Development headers and libraries for libst
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development headers and libraries for SoX.

%prep
%setup -q
#autoreconf -fis

%build
export CFLAGS="%{optflags} -DHAVE_SYS_SOUNDCARD_H=1 -D_FILE_OFFSET_BITS=64 -fPIC -DPIC"

%configure2_5x \
	--with-ladspa-path=%{_includedir}
%make

%install
rm -rf %{buildroot}

%makeinstall_std

ln -sf play %{buildroot}%{_bindir}/rec

cat << EOF > %{buildroot}%{_bindir}/soxplay
#!/bin/sh

%{_bindir}/sox \$1 -t .au - > /dev/audio

EOF
chmod 755 %{buildroot}%{_bindir}/soxplay

ln -snf play %{buildroot}%{_bindir}/rec
ln -s play.1%{_extension} %{buildroot}%{_mandir}/man1/rec.1%{_extension}

rm -rf %{buildroot}%{_libdir}/sox/*.{la,a}

%files
%doc ChangeLog README NEWS AUTHORS
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox*
%{_mandir}/man1/*
%{_mandir}/man7/*

%files -n %{libname}
%{_libdir}/libsox.so.%{major}*

%files -n %{develname}
%{_includedir}/*.h
%{_libdir}/libsox.a
%{_libdir}/libsox.so
%{_libdir}/pkgconfig/sox.pc
%{_mandir}/man3/*


%changelog
* Mon Jun 25 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 14.4.0-2
- Adjust Provides and Obsoletes
- Spec cleanup

* Fri Jun 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 14.4.0-1
+ Revision: 803426
- Update to 14.4.0
- Build for ffmpeg 0.11

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 14.3.2-2
+ Revision: 702750
- fix build

* Thu Sep 22 2011 Andrey Bondrov <abondrov@mandriva.org> 14.3.2-1
+ Revision: 700865
- New version: 14.3.2

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 14.3.0-3
+ Revision: 670004
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 14.3.0-2mdv2011.0
+ Revision: 607553
- rebuild

* Wed Jul 29 2009 Emmanuel Andry <eandry@mandriva.org> 14.3.0-1mdv2010.0
+ Revision: 404112
- New version 14.3.0
- drop p1 (merged upstream)
- BR libgomp-devel
- disable now unneeded autoreconf
- update files list

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - remove build workaround

* Wed Jan 28 2009 GÃ¶tz Waschk <waschk@mandriva.org> 14.2.0-4mdv2009.1
+ Revision: 334818
- use the right libltdl
- rebuild for new libltdl

  + Funda Wang <fwang@mandriva.org>
    - rebuild for new libtool

* Wed Jan 21 2009 Oden Eriksson <oeriksson@mandriva.com> 14.2.0-2mdv2009.1
+ Revision: 332215
- fix build deps
- fix build with -Werror=format-security (P0)

* Mon Nov 17 2008 Funda Wang <fwang@mandriva.org> 14.2.0-1mdv2009.1
+ Revision: 303879
- New version 14.2.0
- drop patches merged upstream

* Mon Oct 13 2008 GÃ¶tz Waschk <waschk@mandriva.org> 14.1.0-2mdv2009.1
+ Revision: 293118
- build with new ffmpeg

* Tue Aug 05 2008 Oden Eriksson <oeriksson@mandriva.com> 14.1.0-1mdv2009.0
+ Revision: 263848
- 14.1.0
- dropped the ffmpeg_fix patch, it's in there
- link against the external LPC10 library (P0)

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 14.0.1-3mdv2009.0
+ Revision: 232956
- added P0 to make it find ffmpeg headers

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Feb 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 14.0.1-1mdv2008.1
+ Revision: 173745
- new version

* Thu Jan 31 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 14.0.0-1mdv2008.1
+ Revision: 160825
- new version
- drop all flac patches
- drop old library name as there is a new one
- add lot of missing buildrequires
- compile with support for:
  o ALSA
  o Samplerate
  o LADSPA
- spec file clean
- fix file list

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Tue Mar 06 2007 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 13.0.0-6mdv2007.0
+ Revision: 133639
- obsolete sox-devel (fixes #29197)

* Sun Feb 18 2007 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 13.0.0-5mdv2007.1
+ Revision: 122478
- use flac patches from cvs (P2), obsoletes P0 & P1

* Fri Feb 16 2007 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 13.0.0-4mdv2007.1
+ Revision: 122017
- flac decoding seems broken, might be due to my flac patch, work around
  for now (P1)
- remove commented out code that was forgotten..

* Fri Feb 16 2007 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 13.0.0-3mdv2007.1
+ Revision: 121588
- fix build with new flac version (P0)
- drop useless dependencies
- fix libification
- revert some changes

* Tue Feb 13 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 13.0.0-2mdv2007.1
+ Revision: 120267
- add missing requires and provides
- move libst-config to the right place

* Tue Feb 13 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 13.0.0-1mdv2007.1
+ Revision: 120262
- new version
- fix buildrequires
- move libraries to its own package
- set %%multiarch on libst-config
- spec file clean

* Mon Dec 18 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 12.18.2-2mdv2007.1
+ Revision: 98466
- sync deps of sox-devel with the output of libst-config --libs

* Sun Dec 03 2006 Emmanuel Andry <eandry@mandriva.org> 12.18.2-1mdv2007.1
+ Revision: 90204
- New version 12.18.2
  drop patch0

* Sun Oct 29 2006 Anssi Hannula <anssi@mandriva.org> 12.18.1-3mdv2007.1
+ Revision: 73607
- fix configure parameters
- Import sox

* Wed Sep 13 2006 Giuseppe Ghibò <ghibo@mandriva.com> 12.18.1-2mdv2007.0
- Force -fPIC -DPIC in CFLAGS for X86-64 linkage.

* Tue May 09 2006 Olivier Thauvin <nanardon@mandriva.org> 12.18.1-1mdk
- 12.18.1

* Mon Dec 12 2005 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 12.17.9-1mdk
- New release 12.17.9
- drop P0 (fixed upstream)

* Wed Aug 24 2005 Oden Eriksson <oeriksson@mandriva.com> 12.17.8-1mdk
- 12.17.8 (Minor bugfixes)

* Wed Dec 22 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 12.17.7-1mdk
- 12.17.7

* Sun Nov 21 2004 Michael Scherer <misc@mandrake.org> 12.17.6-2mdk
- Add plf build

* Wed Nov 10 2004 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 12.17.6-1mdk
- 12.17.6
- merge Oden's changes which went to the wrong place:
	o drop P1, the CAN-2004-0557 fix is included
	o reorder patches, rediffed P0, P1
	o added the scripts
	o use system gsm lib (P2)

* Mon Nov 08 2004 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 12.17.4-5mdk
- fix license
- cosmetics

* Sat Oct 09 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 12.17.4-4mdk
- Patch1: security fix for CAN-2004-0557

* Thu Aug 26 2004 GÃ¶tz Waschk <waschk@linux-mandrake.com> 12.17.4-3mdk
- fix docs list
- patch to fix alsa build

