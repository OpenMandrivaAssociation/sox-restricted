%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

%define	soxlib	st
%define	major	0
%define	libname	%mklibname %{soxlib} %{major}

Summary:	A general purpose sound file conversion tool
Name:		sox
Version:	13.0.0
Release:	%mkrel 6
License: 	LGPL
Group:		Sound
Url:		http://sox.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/sox/%{name}-%{version}.tar.bz2
#Patch0:		sox-13.0.0-fix-build-with-new-libflac.patch
#Patch1:		sox-13.0.0-flac-decoder-hack.patch
Patch2:		sox-13.0.0-new-flac.patch
BuildRequires:	oggvorbis-devel mad-devel gsm-devel libflac-devel libsndfile-devel
%if %build_plf
BuildRequires:	lame-devel
%endif

%description
SoX (Sound eXchange) is a sound file format converter for Linux,
UNIX and DOS PCs. The self-described 'Swiss Army knife of sound
tools,' SoX can convert between many different digitized sound
formats and perform simple sound manipulation functions,
including sound effects.

Install the sox package if you'd like to convert sound file formats
or manipulate some sounds.

%if %build_plf
This package is in PLF as it was build with lame encoder support, which is in PLF.
%endif

%package -n	%{libname}
Summary:	Libraries for SoX
Group:		System/Libraries

%description -n	%{libname}
Libraries for SoX.

%package -n	%{libname}-devel
Summary:	Development headers and libraries for libst
Group:		Development/C
Provides:	lib%{soxlib}-devel = %{version}-%{release}
Provides:	%{soxlib}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
Development headers and libraries for libst.

%prep
%setup -q
#%patch0 -p1 -b .newflac
#%patch1 -p1 -b .flac_decoder_hack
%patch2 -p1 -b .newflac
autoconf

%build
CFLAGS="%{optflags} -DHAVE_SYS_SOUNDCARD_H=1 -D_FILE_OFFSET_BITS=64 -fPIC -DPIC" \
%configure2_5x
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

rm -rf %{buildroot}%{_libdir}/*.la

%post   -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README NEWS AUTHORS
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libst.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/libst-config
%{_libdir}/libst.a
%{_libdir}/libst.so
%{_includedir}/*.h


