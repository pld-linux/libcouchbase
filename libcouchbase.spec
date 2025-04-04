# TODO: system libs (snappy, jsoncpp, cbsasl?, cliopts?)
#
# Conditional build:
%bcond_with	hdrhistogram	# HdrHistogram for statistics recording

Summary:	Couchbase C Client library
Summary(pl.UTF-8):	Biblioteka kliencka C dla Couchbase
Name:		libcouchbase
Version:	3.3.15
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/couchbase/libcouchbase/releases
Source0:	https://github.com/couchbase/libcouchbase/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	229d56a88785e2ca82905eb07865aa02
URL:		https://github.com/couchbase/libcouchbase
%{?with_hdrhistogram:BuildRequires:	HdrHistogram_c-devel}
BuildRequires:	cmake >= 3.5.1
BuildRequires:	libevent-devel
BuildRequires:	libev-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libuv-devel
BuildRequires:	openssl-devel
BuildRequires:	systemtap-sdt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# dtrace script expects CPP to be cpp, not "gcc -E", so force it regardless of rpm version
# (autotools-based rpm<4.19 used to have "gcc -E", cmake builds for 4.19+ switched to cpp)
%define		__cpp	cpp

%description
This is the C client library for Couchbase
(<http://www.couchbase.com/>). It communicates with the cluster and
speaks the relevant protocols necessary to connect to the cluster and
execute data operations.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę kliencką C dla Couchbase
(<http://www.couchbase.com/>). Komunikuje się z klastrem i rozmawia
odpowiednimi protokołami, niezbędnymi do połączenia z klastrem i
wykonywania operacji na danych.

%package io-libev
Summary:	Couchbase I/O operations plugin using libev
Summary(pl.UTF-8):	Wtyczka operacji we/wy Couchbase wykorzystująca libev
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description io-libev
Couchbase I/O operations plugin using libev.

%description io-libev -l pl.UTF-8
Wtyczka operacji we/wy Couchbase wykorzystująca libev.

%package io-libevent
Summary:	Couchbase I/O operations plugin using libevent
Summary(pl.UTF-8):	Wtyczka operacji we/wy Couchbase wykorzystująca libevent
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description io-libevent
Couchbase I/O operations plugin using libevent.

%description io-libevent -l pl.UTF-8
Wtyczka operacji we/wy Couchbase wykorzystująca libevent.

%package io-libuv
Summary:	Couchbase I/O operations plugin using libuv
Summary(pl.UTF-8):	Wtyczka operacji we/wy Couchbase wykorzystująca libuv
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description io-libuv
Couchbase I/O operations plugin using libuv.

%description io-libuv -l pl.UTF-8
Wtyczka operacji we/wy Couchbase wykorzystująca libuv.

%package devel
Summary:	Header files for Couchbase library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Couchbase
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Couchbase library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Couchbase.

%prep
%setup -q

%{__sed} -i -e 's/ "4" / "5" /' doc/man/cbcrc.4

%build
install -d build
cd build
%cmake .. \
	%{?with_hdrhistogram:LCB_USE_HDR_HISTOGRAM=ON} \
	-DLCB_NO_MOCK=ON

# dtrace use is racy
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man5
%{__mv} $RPM_BUILD_ROOT%{_mandir}/{man4/cbcrc.4,man5/cbcrc.5}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.markdown RELEASE_NOTES.markdown
%attr(755,root,root) %{_bindir}/cbc
%attr(755,root,root) %{_bindir}/cbc-*
%attr(755,root,root) %{_libdir}/libcouchbase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcouchbase.so.8
%dir %{_libdir}/libcouchbase
%{_mandir}/man1/cbc.1*
%{_mandir}/man1/cbc-*.1*
%{_mandir}/man5/cbcrc.5*

%files io-libev
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcouchbase/libcouchbase_libev.so

%files io-libevent
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcouchbase/libcouchbase_libevent.so

%files io-libuv
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcouchbase/libcouchbase_libuv.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcouchbase.so
%{_includedir}/libcouchbase
%{_pkgconfigdir}/libcouchbase.pc
