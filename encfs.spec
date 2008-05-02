%define name 	encfs
%define version 1.4.2
%define release 1
%define major	4
%define libname %mklibname %{name} %{major}

Summary: 	Encrypted pass-through filesystem for Linux
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
License:	GPLv3+
Group:		File tools
Source:		%{name}-%{version}.tgz
URL: 		http://arg0.net/wiki/encfs
Requires:	fuse >= 2.3
Requires:	dkms-fuse >= 2.3
Requires:	openssl >= 0.9.7
BuildRequires:	rlog-devel >= 1.3, fuse-devel >= 2.5, openssl-devel >= 0.9.7
BuildRequires:	chrpath
BuildRequires:	boost-devel
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
%setup -q

%build
%configure2_5x --disable-rpath --with-boost-serialization=boost_serialization-mt
%make SED=/usr/bin/sed

%install
rm -fr %buildroot
%makeinstall_std
%find_lang %name

chrpath -d $RPM_BUILD_ROOT%{_bindir}/{encfs,encfsctl}

# unneeded files
rm -f $RPM_BUILD_ROOT%{_libdir}/libencfs.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libencfs.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_bindir}/*
%{_mandir}/man?/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libencfs.so.%{major}*
