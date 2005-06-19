# $Id$
# Authority: dries
# Upstream: Martyn J. Pearce <fluffy$cpan,org>

%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

%define real_name Class-MethodMaker

Summary: Create generic methods for OO Perl
Name: perl-Class-MethodMaker
Version: 2.07
Release: 1
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Class-MethodMaker/

Source: http://www.cpan.org/modules/by-module/Class/Class-MethodMaker-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: perl, perl-Module-Build

%description
This package allows you to create generic methods for OO Perl.

%prep
%setup -n %{real_name}-%{version}

%build
# doesn't work with PREFIX
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS="vendor" DESTDIR="%{buildroot}"
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}"
#./configure --prefix=%{buildroot}
#%{__perl} Build.PL 
#./Build


%install
%{__rm} -rf %{buildroot}
#makeinstall
make install
#./Build install 

### Clean up buildroot
%{__rm} -rf %{buildroot}%{perl_archlib}/perllocal.pod \
		%{buildroot}%{perl_vendorarch}/auto/*{,/*{,/*}}/.packlist

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc README Changes
%doc %{_mandir}/man3/*
%dir %{perl_archlib}/Class/
%{perl_archlib}/Class/MethodMaker.pm
%{perl_archlib}/Class/MethodMaker/
%dir %{perl_archlib}/auto/Class/
%{perl_archlib}/auto/Class/MethodMaker/

%changelog
* Wed Jun  8 2005 Dries Verachtert <dries@ulyssis.org> - 2.07-1
- Updated to release 2.07.

* Wed Feb  2 2005 Dries Verachtert <dries@ulyssis.org> - 2.05-1
- Initial package.
