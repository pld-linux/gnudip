%include        /usr/lib/rpm/macros.perl
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
BuildRequires:	perl-devel
Requires:	/usr/sbibn/ndc
Prereq:		/sbin/chkconfig
URL:		http://gnudip.cheapnet.net/

%description
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

%package clients
Summary:	GnuDIP client
Group:		Networking/Daemons

%description clients
GnuDIP is a service designed for an ISP to give its customers a static
DNS name without having to give them their own IP address. This is the
command line client for GnuDIP.

%prep
%setup -q
%patch0 -p1 -b .gdips
%patch1 -p1 -b .gdipc
%patch2 -p1 -b .db
%patch3 -p1 -b .cgi

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/rc.d/init.d,%{_bindir},%{_sbindir},%{_libdir}/%{name}}
install -d $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/

install gnudip.conf $RPM_BUILD_ROOT%{_sysconfdir}
install gdips.pl $RPM_BUILD_ROOT%{_sbindir}
install gdipc.pl $RPM_BUILD_ROOT%{_bindir}
install gnudip-lib.pl $RPM_BUILD_ROOT%{_libdir}/%{name}
install gnudip2.cgi $RPM_BUILD_ROOT/home/services/httpd/cgi-bin
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}
install ${RPM_SOURCE_DIR}/gdips.init ${RPM_BUILD_ROOT}/etc/rc.d/init.d/gdips

%post
/sbin/chkconfig --add gdips
if [ -f /var/lock/subsys/gdips ]; then
        /etc/rc.d/init.d/gdips restart >&2
else
        echo "Run \"/etc/rc.d/init.d/gdips start\" to start gdips daemon."
fi
echo
echo "Now run %{_bindir}/gdips-configure to configure your gnudip server."
echo

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/gdips ]; then
                /etc/rc.d/init.d/gdips stop >&2
        fi
        /sbin/chkconfig --del gdips
fi

%post clients
echo
echo "Now run %{_bindir}/gdipc.pl -c to set up your configuration file.  You can"
echo "use -f name -c to specify a different filename to read and write the"
echo "configuration to."
echo

%files
%defattr(644,root,root,755)
%config %{_sysconfdir}/gnudip.conf
%config /etc/rc.d/init.d/gdips
%attr(755,root,root) %{_sbindir}/gdips.pl
%dir %{_libdir}/gnudip
%{_libdir}/gnudip/gnudip-lib.pl
/home/services/httpd/cgi-bin/gnudip2.cgi
%attr(755,root,root) %{_bindir}/gdips-configure
%attr(755,root,root) %{_bindir}/gdips-cleanup
%attr(755,root,root) %{_bindir}/gdips-upgrade
%doc README UPDATE README.mysql gnudip2.db ChangeLog dyn.example.com.zone COPYING

%files clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gdipc.pl
%doc README UPDATE ChangeLog COPYING

%clean
rm -rf $RPM_BUILD_ROOT
