# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}

Name:		mod_http2
Version:	1.15.7
Release:	8%{?dist}.3
Summary:	module implementing HTTP/2 for Apache 2
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://icing.github.io/mod_h2/
Source0:	https://github.com/icing/mod_h2/releases/download/v%{version}/mod_http2-%{version}.tar.gz
Patch1:		mod_http2-1.15.7-CVE-2020-9490.patch
Patch2:		mod_http2-1.15.7-CVE-2020-11993.patch
Patch3:		mod_http2-1.15.7-CVE-2021-33193.patch
Patch4:		mod_http2-1.15.7-CVE-2021-44224.patch
Patch5:		mod_http2-1.15.7-SNI.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2176209
Patch6:		mod_http2-1.15.7-CVE-2023-25690.patch

BuildRequires:	pkgconfig, httpd-devel >= 2.4.20, libnghttp2-devel >= 1.7.0, openssl-devel >= 1.0.2
Requires:	httpd-mmn = %{_httpd_mmn}
Conflicts:      httpd < 2.4.37-55

%description
The mod_h2 Apache httpd module implements the HTTP2 protocol (h2+h2c) on
top of libnghttp2 for httpd 2.4 servers.

%prep
%setup -q
%patch1 -p1 -b .CVE-2020-9490
%patch2 -p1 -b .CVE-2020-11993
%patch3 -p1 -b .CVE-2021-33193
%patch4 -p1 -b .CVE-2021-44224
%patch5 -p1 -b .SNI
%patch6 -p1 -b .CVE-2023-25690

%build
%configure
make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/etc/httpd/share/doc/

# create configuration
mkdir -p %{buildroot}%{_httpd_modconfdir}
echo "LoadModule http2_module modules/mod_http2.so" > %{buildroot}%{_httpd_modconfdir}/10-h2.conf
echo "LoadModule proxy_http2_module modules/mod_proxy_http2.so" > %{buildroot}%{_httpd_modconfdir}/10-proxy_h2.conf

%check
make check

%files
%doc README README.md ChangeLog AUTHORS
%license LICENSE
%config(noreplace) %{_httpd_modconfdir}/10-h2.conf
%config(noreplace) %{_httpd_modconfdir}/10-proxy_h2.conf
%{_httpd_moddir}/mod_http2.so
%{_httpd_moddir}/mod_proxy_http2.so

%changelog
* Sat Mar 18 2023 Luboš Uhliarik <luhliari@redhat.com> - 1.15.7-8.3
- Resolves: #2177748 - CVE-2023-25690 httpd:2.4/httpd: HTTP request splitting
  with mod_rewrite and mod_proxy

* Thu Dec 08 2022 Luboš Uhliarik <luhliari@redhat.com> - 1.15.7-7
- Resolves: #2095650 - Dependency from mod_http2 on httpd broken

* Tue Nov 01 2022 Tomas Korbar <tkorbar@redhat.com> - 1.15.7-6
- Backport SNI feature refactor
- Resolves: rhbz#2137257

* Mon Jan 24 2022 Luboš Uhliarik <luhliari@redhat.com> - 1.15.7-5
- Resolves: #2035030 - CVE-2021-44224 httpd:2.4/httpd: possible NULL dereference
  or SSRF in forward proxy configurations

* Thu Jan 06 2022 Luboš Uhliarik <luhliari@redhat.com> - 1.15.7-4
- Resolves: #1966728 - CVE-2021-33193 httpd:2.4/mod_http2: httpd:
  Request splitting via HTTP/2 method injection and mod_proxy

* Fri Oct 30 2020 Lubos Uhliarik <luhliari@redhat.com> - 1.15.7-3
- Resolves: #1869077 - CVE-2020-11993 httpd:2.4/mod_http2: httpd:
  mod_http2 concurrent pool usage

* Mon Aug 17 2020 Lubos Uhliarik <luhliari@redhat.com> - 1.15.7-2
- Resolves: #1869073 - CVE-2020-9490 httpd:2.4/mod_http2: httpd: 
  Push diary crash on specifically crafted HTTP/2 header

* Tue Apr 14 2020 Lubos Uhliarik <luhliari@redhat.com> - 1.15.7-1
- new version 1.15.7
- Resolves: #1814236 - RFE: mod_http2 rebase 
- Resolves: #1747289 - CVE-2019-10082 httpd:2.4/mod_http2: httpd: 
  read-after-free in h2 connection shutdown
- Resolves: #1696099 - CVE-2019-0197 httpd:2.4/mod_http2: httpd: 
  mod_http2: possible crash on late upgrade
- Resolves: #1696094 - CVE-2019-0196 httpd:2.4/mod_http2: httpd:
  mod_http2: read-after-free on a string compare
- Resolves: #1677591 - CVE-2018-17189 httpd:2.4/mod_http2: httpd: 
  mod_http2: DoS via slow, unneeded request bodies

* Thu Aug 29 2019 Lubos Uhliarik <luhliari@redhat.com> - 1.11.3-3
- Resolves: #1744999 - CVE-2019-9511 httpd:2.4/mod_http2: HTTP/2: large amount
  of data request leads to denial of service
- Resolves: #1745086 - CVE-2019-9516 httpd:2.4/mod_http2: HTTP/2: 0-length
  headers leads to denial of service
- Resolves: #1745154 - CVE-2019-9517 httpd:2.4/mod_http2: HTTP/2: request for
  large response leads to denial of service

* Thu Apr  4 2019 Joe Orton <jorton@redhat.com> - 1.11.3-2
- update release (#1695587)

* Tue Oct 16 2018 Lubos Uhliarik <luhliari@redhat.com> - 1.11.3-1
- new version 1.11.3
- Resolves: #1633401 - CVE-2018-11763 mod_http2: httpd:  DoS for HTTP/2
  connections by continuous SETTINGS

* Wed May  2 2018 Joe Orton <jorton@redhat.com> - 1.10.20-1
- update to 1.10.20

* Wed Apr 18 2018 Joe Orton <jorton@redhat.com> - 1.10.18-1
- update to 1.10.18

* Thu Mar 29 2018 Joe Orton <jorton@redhat.com> - 1.10.16-1
- update to 1.10.16 (CVE-2018-1302)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov  7 2017 Joe Orton <jorton@redhat.com> - 1.10.13-1
- update to 1.10.13

* Fri Oct 20 2017 Joe Orton <jorton@redhat.com> - 1.10.12-1
- update to 1.10.12

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Joe Orton <jorton@redhat.com> - 1.10.10-1
- update to 1.10.10

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul  6 2017 Joe Orton <jorton@redhat.com> - 1.10.7-1
- update to 1.10.7

* Mon Jun 12 2017 Joe Orton <jorton@redhat.com> - 1.10.6-1
- update to 1.10.6

* Tue May 16 2017 Joe Orton <jorton@redhat.com> - 1.10.5-1
- update to 1.10.5

* Mon Apr 10 2017 Luboš Uhliarik <luhliari@redhat.com> - 1.10.1-1
- Initial import (#1440780).
