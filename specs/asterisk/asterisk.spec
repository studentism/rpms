# $Id$

# The user and group names
%define uname asterisk
%define gname asterisk

# For pre-versions
%define prever RC1

Summary: The Asterisk PBX and telephony application and toolkit
Name: asterisk
Version: 1.0
Release: %{?prever:0.%{prever}.}2
License: GPL
Group: Applications/Internet
URL: http://www.asterisk.org/
Source0: ftp://ftp.asterisk.org/pub/telephony/asterisk/asterisk-%{version}%{?prever:-%{prever}}.tar.gz
Source1: asterisk.init
Patch: asterisk-1.0-RC1-cdr.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: openssl, zlib, perl, speex, zaptel
Requires: gtk+, mysql, newt, ncurses, postgresql-libs
BuildRequires: openssl-devel, zlib-devel, perl, bison, speex-devel, zaptel
BuildRequires: gtk+-devel, mysql-devel, newt-devel, ncurses-devel
BuildRequires: postgresql-devel, doxygen

%description
Asterisk is an Open Source PBX and telephony development platform that
can both replace a conventional PBX and act as a platform for developing
custom telephony applications for delivering dynamic content over a
telephone similarly to how one can deliver dynamic content through a
web browser using CGI and a web server.
 
Asterisk talks to a variety of telephony hardware including BRI, PRI,
POTS, and IP telephony clients using the Inter-Asterisk eXchange
protocol (e.g. gnophone or miniphone).


%package devel
Summary: Header files and development documentation for Asterisk
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package contains the header files needed to compile modules for Asterisk
as well as the developer documentation generated by doxygen.


%prep
%setup -n asterisk-%{version}%{?prever:-%{prever}}
%patch -p0 -b .cdr


%build
# Replace /var/run by /var/run/asterisk since we don't run as root
#perl -pi -e 's|ASTVARRUNDIR=\$(INSTALL_PREFIX)/var/run|ASTVARRUNDIR=\$(INSTALL_PREFIX)/var/run/%{name}|g' Makefile
%{__make} PROC="%{_arch}" OPTIMIZE="%{optflags}" 
make progdocs


%install
%{__rm} -rf %{buildroot}
make install INSTALL_PREFIX=%{buildroot}
install -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/asterisk

# Override wrong absolute links
%{__rm} -f %{buildroot}%{_localstatedir}/lib/asterisk/sounds/vm && \
    %{__ln_s} -f ../../../spool/asterisk/vm \
                 %{buildroot}%{_localstatedir}/lib/asterisk/sounds/vm
%{__rm} -f %{buildroot}%{_localstatedir}/lib/asterisk/sounds/voicemail && \
    %{__ln_s} -f ../../../spool/asterisk/voicemail \
                 %{buildroot}%{_localstatedir}/lib/asterisk/sounds/voicemail
%{__rm} -f %{buildroot}%{_localstatedir}/spool/asterisk/vm && \
    %{__ln_s} -f voicemail/default \
                 %{buildroot}%{_localstatedir}/spool/asterisk/vm

# Install all sample config files
for file in configs/*.*; do
    %{__install} -m 0640 $file \
        %{buildroot}%{_sysconfdir}/asterisk/`basename $file .sample`
done

# We need that directory, see above
%{__mkdir_p} %{buildroot}%{_localstatedir}/run/asterisk

# Fix the safe_asterix script, to be run as non-root
%{__perl} -pi.orig -e 's|(asterisk \${ASTARGS})|%{_sbindir}/$1|g' \
    %{buildroot}%{_sbindir}/safe_asterisk

# Install demo sounds
for file in sounds/demo-*; do
    install -m 644 $file %{buildroot}%{_localstatedir}/lib/asterisk/sounds/
done
for file in sounds/*.mp3; do
    install -m 644 $file %{buildroot}%{_localstatedir}/lib/asterisk/mohmp3/
done


%clean
%{__rm} -rf %{buildroot}


%pre
# Add the "asterisk" user
/usr/sbin/useradd -c "Asterisk PBX" -G tty -s /sbin/nologin -r \
    -d "%{_localstatedir}/lib/asterisk" %{uname} 2>/dev/null || :

%post
# Register the asterisk service
/sbin/chkconfig --add asterisk
# Fix the permission on tty9
/bin/chmod g+r /dev/tty9

%preun
if [ $1 -eq 0 ]; then
    /sbin/service asterisk stop >/dev/null 2>&1
    /sbin/chkconfig --del asterisk
fi


%files
%defattr(-, root, root, 0755)
%doc BUGS ChangeLog CREDITS HARDWARE LICENSE README SECURITY doc/*.txt configs/
%doc sounds.txt
%attr(750, %{uname}, %{gname}) %dir %{_sysconfdir}/asterisk
%attr(640, %{uname}, %{gname}) %config(noreplace) %{_sysconfdir}/asterisk/*.conf
%attr(640, %{uname}, %{gname}) %config(noreplace) %{_sysconfdir}/asterisk/*.adsi
%{_initrddir}/asterisk
%{_libdir}/asterisk
%{_sbindir}/*
%attr(-  , %{uname}, %{gname}) %{_localstatedir}/lib/asterisk
%attr(750, %{uname}, %{gname}) %{_localstatedir}/run/asterisk
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/log/asterisk
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/spool/asterisk
                                    %{_localstatedir}/spool/asterisk/vm
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/spool/asterisk/voicemail
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/spool/asterisk/voicemail/default


%files devel
%doc doc/api/html/*
%{_includedir}/asterisk


%changelog
* Thu Jul 29 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC1.2
- Added Areski's cdr patch.

* Mon Jul 26 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC1.1
- Update to 1.0-RC1.

* Thu Feb  5 2004 Matthias Saou <http://freshrpms.net> 0.7.2-1
- Update to 0.7.2.

* Tue Dec  2 2003 Matthias Saou <http://freshrpms.net>
- Updated to today's CVS code.
- Added asterisk-addons (cdr_addon_mysql).

* Tue Nov  4 2003 Matthias Saou <http://freshrpms.net>
- Added CVS release support.
- Changed ownership of the config directory to asterisk user.

* Fri Sep 19 2003 Matthias Saou <http://freshrpms.net>
- Initial RPM release.

