Name:           steam-powerbuttond
Version:        0.0.git.1794.b5ad0f5
Release:        1%{?dist}
Summary:        Steam Deck power button daemon

License:        BSD
URL:            https://github.com/ShadowBlip/steam-powerbuttond

BuildRequires:  systemd-rpm-macros
BuildRequires:  libevdev-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  git

Requires:       libevdev

Provides:       steam-powerbuttond
Provides:       powerbuttond
Obsoletes:      powerbuttond

%description
Steam Deck power button daemon

# Disable debug packages
%define debug_package %{nil}

%prep
cd %{_builddir}

cat << EOF >> %{_builddir}/98-steam-powerbuttond.preset
enable steam-powerbuttond.service
EOF

git clone %{url} %{_builddir}/steam-powerbuttond
cd %{_builddir}/steam-powerbuttond
# stupid fedora workaround
sed -i 's|/usr/bin/env python|/usr/bin/env python3|g' steam-powerbuttond
sed -i 's|/usr/local/bin|/usr/bin|g' steam-powerbuttond.service

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_presetdir}/
install -D -m 755 %{_builddir}/steam-powerbuttond/steam-powerbuttond %{buildroot}%{_bindir}/steam-powerbuttond
install -m 644 %{_builddir}/98-steam-powerbuttond.preset %{buildroot}%{_presetdir}/
install -m 644 %{_builddir}/steam-powerbuttond/steam-powerbuttond.service %{buildroot}%{_unitdir}/steam-powerbuttond.service

%post
udevadm control --reload-rules
udevadm trigger
%systemd_post steam-powerbuttond.service

%preun
%systemd_preun steam-powerbuttond.service

%files
%{_bindir}/steam-powerbuttond
%{_unitdir}/steam-powerbuttond.service
%{_presetdir}/98-steam-powerbuttond.preset

%changelog
%autochangelog
