Summary:	Internet Relay Chat Services
Summary(pl.UTF-8):	Usługi dla sieci IRC
Name:		atheme
Version:	2.1.1
Release:	1
License:	BSD-like or any GPL-compatible
Group:		Daemons
Source0:	http://www.atheme.net/releases/%{name}-%{version}.tar.gz
# Source0-md5:	5ef988f6dd81b7d7e535b343f9874be6
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.atheme.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(atheme)
Provides:	user(atheme)
Obsoletes:	ircservices
Obsoletes:	ircservices-hybrid
Obsoletes:	ircservices-ptlink
Obsoletes:	ircservices6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/atheme

%description
Atheme IRC Services is a package of services for IRC networks.

%description -l pl.UTF-8
Atheme IRC Services to pakiet z usługami dla sieci IRC (Internet Relay
Chat).

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
CFLAGS="%{rpmcflags} %{?debug:-DDEBUGMODE}"
%configure \
	--enable-fhs-paths \
	--bindir=%{_sbindir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/ircservices,%{_var}/log/ircservices,%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_localstatedir}/languages} \
	$RPM_BUILD_ROOT%{_var}/log/atheme/

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atheme
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/atheme

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -f -g 217 atheme
%useradd -g atheme -d /var/lib/atheme -u 217 -c "Atheme IRC services account" -s /bin/true atheme

%post
/sbin/chkconfig --add atheme
%service %{name} restart "Atheme IRC Services"

%preun
if [ "$1" = 0 ]; then
	%service %{name} stop
	/sbin/chkconfig --del atheme
fi

%postun
if [ "$1" = "0" ]; then
	%userremove atheme
	%groupremove atheme
fi

%files
%defattr(644,root,root,755)
%doc README doc/*
%attr(755,root,root) %{_sbindir}/*
%attr(750,root,atheme) %dir %{_sysconfdir}
%attr(660,atheme,atheme) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(754,root,root) /etc/rc.d/init.d/atheme
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/atheme
%dir %{_var}/log/atheme
%attr(770,root,atheme) %dir %{_var}/log/atheme
%attr(770,root,atheme) %dir %{_localstatedir}
%dir %{_libdir}/atheme
%dir %{_libdir}/atheme/backend
%attr(755,root,root) %{_libdir}/atheme/backend/*.so
%dir %{_libdir}/atheme/crypto
%attr(755,root,root) %{_libdir}/atheme/crypto/*.so
%dir %{_libdir}/atheme/modules
%dir %{_libdir}/atheme/modules/chanserv
%attr(755,root,root) %{_libdir}/atheme/modules/chanserv/*.so
%dir %{_libdir}/atheme/modules/global
%attr(755,root,root) %{_libdir}/atheme/modules/global/*.so
%dir %{_libdir}/atheme/modules/memoserv
%attr(755,root,root) %{_libdir}/atheme/modules/memoserv/*.so
%dir %{_libdir}/atheme/modules/nickserv
%attr(755,root,root) %{_libdir}/atheme/modules/nickserv/*.so
%dir %{_libdir}/atheme/modules/operserv
%attr(755,root,root) %{_libdir}/atheme/modules/operserv/*.so
%dir %{_libdir}/atheme/modules/saslserv
%attr(755,root,root) %{_libdir}/atheme/modules/saslserv/*.so
%dir %{_libdir}/atheme/modules/xmlrpc
%attr(755,root,root) %{_libdir}/atheme/modules/xmlrpc/*.so
%dir %{_libdir}/atheme/protocol
%attr(755,root,root) %{_libdir}/atheme/protocol/*.so
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/help
%dir %{_datadir}/%{name}/help/cservice
%{_datadir}/%{name}/help/cservice/*
%dir %{_datadir}/%{name}/help/gservice
%{_datadir}/%{name}/help/gservice/*
%{_datadir}/%{name}/help/help
%dir %{_datadir}/%{name}/help/memoserv
%{_datadir}/%{name}/help/memoserv/*
%dir %{_datadir}/%{name}/help/nickserv
%{_datadir}/%{name}/help/nickserv/*
%dir %{_datadir}/%{name}/help/oservice
%{_datadir}/%{name}/help/oservice/*
%dir %{_datadir}/%{name}/help/saslserv
%{_datadir}/%{name}/help/saslserv/*
%dir %{_datadir}/%{name}/help/userserv
%{_datadir}/%{name}/help/userserv/*
