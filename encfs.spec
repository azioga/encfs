%define major	4
%define libname %mklibname %{name} %{major}

Summary: 	Encrypted pass-through filesystem for Linux
Name:		encfs
Version:	1.5.2
Release:	%mkrel 6
License:	GPLv3+
Group:		File tools
Source0:	%{name}-%{version}.tgz
# (fc) 1.5.2-3mdv fix build with latest gcc 
Patch0:		encfs-1.5.2-fixbuild.patch
Patch1:		encfs-1.5.2-fix-linkage.patch
URL: 		http://www.arg0.net/encfs
Requires:	fuse >= 2.3
Requires:	kmod(fuse)
Requires:	openssl >= 0.9.7
BuildRequires:	rlog-devel >= 1.3, fuse-devel >= 2.5, openssl-devel >= 0.9.7
BuildRequires:	chrpath
BuildRequires:	boost-devel
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
%patch0 -p1 -b .fixbuild
%patch1 -p0 -b .link

%build
%configure2_5x --disable-rpath --with-boost-serialization=boost_serialization-mt --with-boost-system=boost_system-mt --with-boost-libdir=%{_libdir}
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
