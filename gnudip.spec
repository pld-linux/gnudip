Summary:	GnuDIP - static DNS name without static IP solution
Summary(pl.UTF-8):	GnuDIP - rozwiązanie problemu statycznej nazwy DNS bez statycznego IP
Name:		gnudip
Version:	2.1.2
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.cheapnet.net/pub/gnudip/%{name}-%{version}.tar.gz
# Source0-md5:	83c3c5cf40dd76d136de47370791ebd1
Source1:	gdips.init
Source2:	gdips-configure
Source3:	gdips-cleanup
Source4:	gdips-upgrade
Patch0:		%{name}-gdips.patch
Patch1:		%{name}-gdipc.patch
Patch2:		%{name}-db.patch
Patch3:		%{name}-cgi.patch
URL:		http://gnudip.cheapnet.net/
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov
Requires(post,preun):	/sbin/chkconfig
Requires:	/usr/sbin/ndc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GnuDIP is a service designed for an ISP to give its customers a static
DNS name without having to give them their own IP address. For those
who are familiar with ml.org this is a simple replacement. GnuDIP has
two main parts on the server side. First, the multi-threaded server
that listens on a port 3495 that accepts connections from client
applications and updates their hostname, and second, the web cgi that
is used as the administration tool and as the users tool to manage
their own account. Using the web cgi a user can set their desired
homepage in their settings and then set the special URL as the default
page for their browser so now every time they open their browser their
hostname will be automatically be updated without having to run any
other sort of client application and then they would be redirected to
the URL they set in their GnuDIP settings.

%description -l pl.UTF-8
GnuDIP jest usługą stworzoną dla ISP, aby dawać klientom statyczne
nazwy DNS bez potrzeby dawania im własnych adresów IP. Jest to prosty
zamiennik tego, czym było ml.org. GnuDIP ma dwie główne części po
stronie serwera. Pierwszą jest wielowątkowy serwer, słuchający na
porcie 3495 i przyjmujący połączenia od aplikacji klienckich, aby
uaktualnić ich nazwę hosta; drugą jest skrypt CGI, będący narzędziem
do administrowania oraz do zarządzania własnymi kontami przez
użytkowników. Przy użyciu tego CGI użytkownik może ustawić swoją
stronę domową, aby później ustawić specjalny URL jako domyślną stronę
w przeglądarce, dzięki czemu za każdym razem, kiedy uruchomi
przeglądarkę, będzie miał uaktualnioną nazwę hosta bez potrzeby
uruchamiania innych aplikacji klienckiej, a przeglądarka zostanie
przekierowana pod podany w ustawieniach URL.

%package clients
Summary:	GnuDIP client
Summary(pl.UTF-8):	Klient GnuDIP
Group:		Networking/Daemons

%description clients
GnuDIP is a service designed for an ISP to give its customers a static
DNS name without having to give them their own IP address. This is the
command line client for GnuDIP.

%description clients -l pl.UTF-8
GnuDIP jest usługą stworzoną dla ISP, aby dawać klientom statyczne
nazwy DNS bez potrzeby dawania im własnych adresów IP. To jest klient
GnuDIP działający z linii poleceń.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_bindir},%{_sbindir},%{_libdir}/%{name}}
install -d $RPM_BUILD_ROOT/home/services/httpd/cgi-bin

install gnudip.conf $RPM_BUILD_ROOT%{_sysconfdir}
install gdips.pl $RPM_BUILD_ROOT%{_sbindir}
install gdipc.pl $RPM_BUILD_ROOT%{_bindir}
install gnudip-lib.pl $RPM_BUILD_ROOT%{_libdir}/%{name}
install gnudip2.cgi $RPM_BUILD_ROOT/home/services/httpd/cgi-bin
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/gdips

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc README UPDATE README.mysql gnudip2.db ChangeLog dyn.example.com.zone
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnudip.conf
%attr(754,root,root) /etc/rc.d/init.d/gdips
%attr(755,root,root) %{_sbindir}/gdips.pl
%dir %{_libdir}/gnudip
%{_libdir}/gnudip/gnudip-lib.pl
%attr(755,root,root) /home/services/httpd/cgi-bin/gnudip2.cgi
%attr(755,root,root) %{_bindir}/gdips-configure
%attr(755,root,root) %{_bindir}/gdips-cleanup
%attr(755,root,root) %{_bindir}/gdips-upgrade

%files clients
%defattr(644,root,root,755)
%doc README UPDATE ChangeLog
%attr(755,root,root) %{_bindir}/gdipc.pl
