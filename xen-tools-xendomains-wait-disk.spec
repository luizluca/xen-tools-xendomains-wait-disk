#
# spec file for package xen-tools-xendomains-wait-disk
#
# Copyright (c) 2017 Luiz Angelo Daros de Luca
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

%define wait_disk_servicename	xendomains-wait-disks
%define wait_disk_service	%{wait_disk_servicename}.service
Name:           xen-tools-xendomains-wait-disk
Version:        1.0
Release:        0
Summary:        Adds a new xendomains-wait-disks.service
License:        GPL-3.0+
Group:          System/Kernel
URL:            https://github.com/luizluca/xen-tools-xendomains-wait-disk
Source1:        %{wait_disk_servicename}.sh
Source2:        %{wait_disk_service}
Source10:       README.md
Source11:       LICENSE
BuildRequires:  bash
BuildRequires:  systemd-rpm-macros
BuildRequires:  xen-tools
Requires:       xen-tools
Supplements:    packageand(xen-tools:xen-tools-xendomains-wait-disk)
BuildArch:      noarch
%{?systemd_requires}

%description
This package adds a new service named xendomains-wait-disk.service,
that simply calls xendomains-wait-disk. xendomains-wait-disk script
loops checking for the presence of every disk used by domU that
xendomains.service will try to launch. The script returns when
all disks become available or xendomains-wait-disk.service expires.

xendomains-wait-disk.service has the same dependencies as
xendomains.service, but it adds itself as a Wanted service for xendomains.
If xendomains-wait-disk.service fails, xendomains.service is launched anyway.

%prep

%build

%install
mkdir -p %{buildroot}%{_libexecdir}/%{name}/bin
install -D -m 644 %{SOURCE1} %{buildroot}%{_libexecdir}/%{name}/bin/%{wait_disk_servicename}
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{wait_disk_service}
mkdir -p %{buildroot}%{_sbindir}
ln -s %{_sbindir}/service %{buildroot}%{_sbindir}/rc%{wait_disk_servicename}
cp %{SOURCE10} %{SOURCE11} %{_builddir}

%pre
%service_add_pre %{wait_disk_service}

%post
%service_add_post %{wait_disk_service}
systemctl enable %{wait_disk_service}

%preun
%service_del_preun %{wait_disk_service}

%postun
%service_del_postun %{wait_disk_service}
if [ "$1" -eq 0 ]; then
	systemctl disable %{wait_disk_service} || :
fi

%files
%{_libexecdir}/%{name}
%attr(755,root,root) %{_libexecdir}/%{name}/bin/%{wait_disk_servicename}
%{_unitdir}/%{wait_disk_service}
%{_sbindir}/rc%{wait_disk_servicename}
%doc README.md LICENSE

%changelog
