%define name gnudip
%define version 2.1.2
%define release 4
%define sourcefile gnudip-2.1.2.tar.gz

Summary:	GnuDIP
Name:		gnudip
Version:	2.1.2
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.cheapnet.net/pub/gnudip/%{name}-%{version}.tar.gz
Source1:	gdips.init
Source2:	gdips-configure
Source3:	gdips-cleanup
Source4:	gdips-upgrade
Patch0:		%{name}-gdips.patch
Patch1:		%{name}-gdipc.patch
Patch2:		%{name}-db.patch
Patch3:		%{name}-cgi.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArchitectures:	noarch
URL:		http://gnudip.cheapnet.net/

%description
Summary: GnuDIP server and client

%package client
Summary:	GnuDIP client
Group:		Networking/Daemons
Requires:	perl perl-MD5

%description client
GnuDIP is a service designed for an ISP to give its customers a static
DNS name without having to give them their own IP address. This is the
command line client for GnuDIP.

%package server
Summary:	GnuDIP server
Group:		Networking/Daemons
Requires:	perl perl-MD5 MySQL-client /usr/sbin/ndc
Prereq:		/sbin/chkconfig

%description server
GnuDIP is a service desiged for an ISP to give its customers a static
DNS name without having to give them their own IP address. For those
who are familiar with ml.org this is a simple replacement. GnuDIP has
2 main parts on the server side. 1, the multi-threaded server that
listens on a port 3495 that accepts connections from client
applications and updates their hostname, and 2 the web cgi that is
used as the administration tool and as the users tool to manage their
own account. Using the web cgi a user can set their desired homepage
in their settings and then set the special URL as the default page for
their browser so now every time they open their browser their hostname
will be automatically be updated without having to run any other sort
of client application and then they would be redirected to the URL
they set in their GnuDIP settings.

%prep
%setup -q
%patch0 -p1 -b .gdips
%patch1 -p1 -b .gdipc
%patch2 -p1 -b .db
%patch3 -p1 -b .cgi

%build

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 640 -o root gnudip.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/
install -D -m 750 -o root gdips.pl ${RPM_BUILD_ROOT}%{_sbindir}/
install -D -m 750 -o root gdipc.pl ${RPM_BUILD_ROOT}%{_bindir}/
install -D -o root gnudip-lib.pl ${RPM_BUILD_ROOT}%{_libdir}/gnudip/
#install -D -m 750 -o www-data -g www-data gnudip2.cgi ${RPM_BUILD_ROOT}/usr/lib/cgi-bin/
install -D -m 755 -o root gnudip2.cgi ${RPM_BUILD_ROOT}/home/httpd/cgi-bin/
install -D -m 750 -o root ${RPM_SOURCE_DIR}/gdips-configure ${RPM_BUILD_ROOT}%{_bindir}/
install -D -m 750 -o root ${RPM_SOURCE_DIR}/gdips-cleanup ${RPM_BUILD_ROOT}%{_bindir}/
install -D -m 750 -o root ${RPM_SOURCE_DIR}/gdips-upgrade ${RPM_BUILD_ROOT}%{_bindir}/
install -D -m 755 -o root ${RPM_SOURCE_DIR}/gdips.init ${RPM_BUILD_ROOT}/etc/rc.d/init.d/gdips

%post client
echo ""
echo Now run %{_bindir}/gdipc.pl -c to set up your configuration file.  You can
echo use -f name -c to specify a different filename to read and write the
echo configuration to.
echo ""

%post server
chkconfig --add gdips
echo ""
echo Now run %{_bindir}/gdips-configure to configure your gnudip server.
echo ""

%preun server
if [ $1 = 0 ]; then
  chkconfig --del gdips
fi

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gdipc.pl
%doc README UPDATE ChangeLog COPYING

%files server
%defattr(644,root,root,755)
%config %{_sysconfdir}/gnudip.conf
%config /etc/rc.d/init.d/gdips
%attr(755,root,root) %{_sbindir}/gdips.pl
%dir %{_libdir}/gnudip
%{_libdir}/gnudip/gnudip-lib.pl
/home/httpd/cgi-bin/gnudip2.cgi
%attr(755,root,root) %{_bindir}/gdips-configure
%attr(755,root,root) %{_bindir}/gdips-cleanup
%attr(755,root,root) %{_bindir}/gdips-upgrade
%doc README UPDATE README.mysql gnudip2.db ChangeLog dyn.example.com.zone COPYING

%clean
rm -rf $RPM_BUILD_ROOT
