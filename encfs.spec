%define major	6
%define libname %mklibname %{name} %{major}

Summary: 	Encrypted pass-through filesystem for Linux
Name:		encfs
Version:	1.7.4
Release:	6
License:	GPLv3+
Group:		File tools
Source0:	http://encfs.googlecode.com/files/%{name}-%{version}.tgz
URL: 		http://www.arg0.net/encfs
Requires:	fuse >= 2.6
Requires:	kmod(fuse)
Requires:	openssl >= 0.9.7
BuildRequires:	rlog-devel >= 1.3
BuildRequires:	fuse-devel >= 2.6
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	chrpath
BuildRequires:	boost-devel >= 1.34
BuildRequires:	autoconf-archive

%description
EncFS implements an encrypted pass-through filesystem in userspace using
FUSE. File names and contents are encrypted using OpenSSL.

%package -n 	%{libname}
Summary:	Libraries for encfs
Group:		System/Libraries

%description -n	%{libname}
Libraries for encfs.

%prep
%setup -q -n %{name}-%{version}

%build
%configure2_5x --disable-rpath --with-boost-libdir=%{_libdir}
%make SED=/usr/bin/sed

%install
%makeinstall_std

%find_lang %{name}

chrpath -d %{buildroot}%{_bindir}/{encfs,encfsctl}

# unneeded files
rm -f %{buildroot}%{_libdir}/libencfs.la
rm -f %{buildroot}%{_libdir}/libencfs.so

%files -f %{name}.lang
%doc README AUTHORS ChangeLog
%{_bindir}/*
%{_mandir}/man?/*

%files -n %{libname}
%{_libdir}/libencfs.so.%{major}*


