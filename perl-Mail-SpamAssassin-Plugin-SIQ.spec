Summary:	The SIQ plugin for SpamAssassin
Name:		perl-Mail-SpamAssassin-Plugin-SIQ
Version:	0
Release:	%mkrel 3
License:	Apache License
Group:		Development/Perl
URL:		http://people.apache.org/~dos/sa-plugins/3.1/
Source0:	http://people.apache.org/~dos/sa-plugins/3.1/SIQ.cf
Source1:	http://people.apache.org/~dos/sa-plugins/3.1/SIQ.pm
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  spamassassin-spamd >= 3.1.1
Requires:	spamassassin-spamd >= 3.1.1
BuildRequires:	perl-doc
BuildArch:	noarch

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
