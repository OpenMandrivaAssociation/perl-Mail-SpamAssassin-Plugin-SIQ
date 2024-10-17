Summary:	The SIQ plugin for SpamAssassin
Name:		perl-Mail-SpamAssassin-Plugin-SIQ
Version:	0
Release:	9
License:	Apache License
Group:		Development/Perl
URL:		https://people.apache.org/~dos/sa-plugins/3.1/
Source0:	http://people.apache.org/~dos/sa-plugins/3.1/SIQ.cf
Source1:	http://people.apache.org/~dos/sa-plugins/3.1/SIQ.pm
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  spamassassin-spamd >= 3.1.1
Requires:	spamassassin-spamd >= 3.1.1
BuildRequires:	perl-doc
BuildArch:	noarch
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
This plugin queries for reputation data, based on domain & IP pairs, from a
reputation service provider using the IETF ASRG draft SIQ protocol:

http://www.ietf.org/internet-drafts/draft-irtf-asrg-iar-howe-siq-02.txt

A number of eval functions are provided for writing eval-type rules against
the reputation data returned by the reputation service queried.

A pseudo-header is also provided for testing of the optional text area in an
SIQ response.

%prep

%setup -q -T -c -n %{name}-%{version}

cp %{SOURCE0} SIQ.cf
cp %{SOURCE1} SIQ.pm

# make it portable
perl -pi -e "s|/etc/mail/spamassassin/SIQ\.pm|%{perl_vendorlib}/Mail/SpamAssassin/Plugin/SIQ.pm|g" SIQ.cf

%build

perldoc SIQ.pm > Mail::SpamAssassin::Plugin::SIQ.3pm

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -d %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin
install -d %{buildroot}%{_mandir}/man3

install -m0644 SIQ.cf %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 SIQ.pm %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin/
install -m0644 Mail::SpamAssassin::Plugin::SIQ.3pm %{buildroot}%{_mandir}/man3/

%post
if [ -f %{_var}/lock/subsys/spamd ]; then
    %{_initrddir}/spamd restart 1>&2;
fi
    
%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/spamd ]; then
        %{_initrddir}/spamd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/spamassassin/SIQ.cf
%{perl_vendorlib}/Mail/SpamAssassin/Plugin/SIQ.pm
%{_mandir}/man3/Mail::SpamAssassin::Plugin::SIQ.3pm*


%changelog
* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0-7mdv2010.0
+ Revision: 430495
- rebuild

* Thu Jul 31 2008 Thierry Vignaud <tv@mandriva.org> 0-6mdv2009.0
+ Revision: 257748
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0-5mdv2009.0
+ Revision: 245819
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0-3mdv2008.1
+ Revision: 140691
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Jul 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0-3mdv2008.0
+ Revision: 46365
- misc fixes


* Sun Dec 17 2006 Oden Eriksson <oeriksson@mandriva.com> 0-3mdv2007.0
+ Revision: 98303
- bunzip the sources
- make it backportable (drop the patch)

* Sat Nov 25 2006 Emmanuel Andry <eandry@mandriva.org> 0-2mdv2007.1
+ Revision: 87292
- patch to fix perl module path
- Import perl-Mail-SpamAssassin-Plugin-SIQ

* Fri May 19 2006 Oden Eriksson <oeriksson@mandriva.com> 0-1mdk
- initial Mandriva package

