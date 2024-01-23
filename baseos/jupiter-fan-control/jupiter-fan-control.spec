Name:           jupiter-fan-control
Version:        0.0.git.2027.5f33994e
Release:        1%{?dist}
Summary:        Steam Deck Fan Controller
License:    	MIT
URL:            https://github.com/ublue-os/bazzite

Source:        	https://gitlab.com/evlaV/%{name}/-/archive/main/%{name}-main.tar.gz
BuildArch:      noarch

Patch0:         fedora.patch
# Valve made a small typo (Thanks RodoMa92)
Patch1:         fan_fix.patch

Requires:       python3

BuildRequires:  systemd-rpm-macros

%description
SteamOS 3.0 Steam Deck Fan Controller

# Disable debug packages
%define debug_package %{nil}

%prep

%setup -n %{name}-main
%patch 0 -p0
%patch 1 -p0

cat << EOF >> %{_builddir}/96-jupiter-fan-control.preset
enable jupiter-fan-control.service
EOF

%build

%install
mkdir -p %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_presetdir}/
install -m 644 %{_builddir}/96-jupiter-fan-control.preset %{buildroot}%{_presetdir}/
cp -rv usr/share/* %{buildroot}%{_datadir}
cp -v usr/lib/systemd/system/jupiter-fan-control.service %{buildroot}%{_unitdir}/jupiter-fan-control.service

# Do post-installation
%post
udevadm control --reload-rules
udevadm trigger
%systemd_post jupiter-fan-control.service


# Do before uninstallation
%preun
%systemd_preun jupiter-fan-control.service

# Do after uninstallation
%postun
%systemd_postun_with_restart jupiter-fan-control.service

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%doc README.md
%{_datadir}/jupiter-fan-control/fancontrol.py
%{_datadir}/jupiter-fan-control/*-config.yaml
%{_datadir}/jupiter-fan-control/PID.py
%{_unitdir}/jupiter-fan-control.service
%{_presetdir}/96-jupiter-fan-control.preset

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
