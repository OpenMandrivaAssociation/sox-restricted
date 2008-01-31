%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A general purpose sound file conversion tool
Name:		sox
Version:	14.0.0
Release:	%mkrel 1
License:	LGPLv2+
Group:		Sound
Url:		http://sox.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/sox/%{name}-%{version}.tar.bz2
BuildRequires:	libalsa-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	mad-devel
BuildRequires:	gsm-devel
BuildRequires:	libflac-devel
BuildRequires:	libsndfile-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	ladspa-devel
BuildRequires:	libltdl-devel
%if %build_plf
BuildRequires:	lame-devel
BuildRequires:	libamrwb-devel
BuildRequires:	libamrnb-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n %{libname}
Summary:	Libraries for SoX
Group:		System/Libraries
Obsoletes:	%mklibname st 0

%description -n	%{libname}
Libraries for SoX.

%package -n %{develname}
Summary:	Development headers and libraries for libst
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%mklibname st 0 -d
Obsoletes:	%mklibname st 0 -d

%description -n	%{develname}
Development headers and libraries for SoX.

%prep
%setup -q

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

rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/sox/*.{la,a}

%post -n %{libname} -p /sbin/ldconfig

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
%{_mandir}/man7/*
%{_libdir}/%{name}/*.so*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libsfx.so.%{major}*
%{_libdir}/libsox.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libsfx.a
%{_libdir}/libsfx.so
%{_libdir}/libsox.a
%{_libdir}/libsox.so
%{_includedir}/*.h
%{_mandir}/man3/*
