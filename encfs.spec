# FIXME: Build dies in a massive shower of boost problems without both
# of these - AdamW 2008/07
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

%define major	4
%define libname %mklibname %{name} %{major}

Summary: 	Encrypted pass-through filesystem for Linux
Name:		encfs
Version:	1.5.2
Release:	%mkrel 1
License:	GPLv3+
Group:		File tools
Source0:	%{name}-%{version}.tgz
Patch0:         encfs-1.5-boost.patch
URL: 		http://arg0.net/wiki/encfs
Requires:	fuse >= 2.3
Requires:	kmod(fuse)
Requires:	openssl >= 0.9.7
BuildRequires:	rlog-devel >= 1.3, fuse-devel >= 2.5, openssl-devel >= 0.9.7
BuildRequires:	chrpath
BuildRequires:	boost-devel
# for boost-system patch - need the ax_boost_system.m4 file from this
# for the patch to work - AdamW 2008/07
BuildRequires:	autoconf-archive
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
EncFS implements an encrypted pass-through filesystem in userspace using
FUSE. File names and contents are encrypted using OpenSSL.

%package -n 	%{libname}
Summary:	Libraries for encfs
Group:		System/Libraries

%description -n	%{libname}
Libraries for encfs.

%prep
%setup -q -n %{name}-1.5
%patch0 -p0 -b .boost

%build
# needed for boost-system.patch - AdamW 2008/07
cp /usr/share/aclocal/ax_boost_system.m4 m4-local/
autoreconf

%configure2_5x --disable-rpath --with-boost-serialization=boost_serialization-mt --with-boost-system=boost_system-mt
%make SED=/usr/bin/sed

%install
rm -fr %{buildroot}
%makeinstall_std
%find_lang %{name}

chrpath -d %{buildroot}%{_bindir}/{encfs,encfsctl}

# unneeded files
rm -f %{buildroot}%{_libdir}/libencfs.la
rm -f %{buildroot}%{_libdir}/libencfs.so

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_bindir}/*
%{_mandir}/man?/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libencfs.so.%{major}*
