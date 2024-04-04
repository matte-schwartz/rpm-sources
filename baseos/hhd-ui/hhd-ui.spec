%global __os_install_post %{_rpmconfigdir}/brp-compress %{_rpmconfigdir}/brp-strip-none %{_rpmconfigdir}/brp-strip-static-archive

Name:           hhd-ui
Version:        2.2.0
Release:        2%{?dist}
Summary:        Configurator interface for Handheld Daemon.
License:        GPL-3.0-or-later
URL:            https://github.com/hhd-dev/hhd-ui
Source0:        %{URL}/archive/master.tar.gz
Source1:        hhd-ui.desktop

BuildArch:      x86_64

BuildRequires:  npm
BuildRequires:  fuse-devel
BuildRequires:  git
BuildRequires:  systemd-rpm-macros

Requires: desktop-file-utils
Requires: hhd
Requires: fuse

%description
Configurator interface for Handheld Daemon.

%prep
mkdir -p %{name}-%{version}
cd %{name}-%{version}
tar -xzf %{_sourcedir}/master.tar.gz --strip-components=1

%build
cd %{name}-%{version}
VERSION=$(cat package.json | grep -E '"version": "[0-9\.]+"' -o | grep -E "[0-9\.]+" -o)
sed -i "s|\"version\": \"1.0.0\"|\"version\": \"$VERSION\"|" "electron/package.json"
npm ci
npm run electron-build
cd electron
npm ci
npm run build
chmod +x dist/hhd-ui.AppImage

%install
mkdir -p %{buildroot}%{_bindir}
cp -a %{name}-%{version}/electron/dist/hhd-ui.AppImage %{buildroot}%{_bindir}/hhd-ui
install -Dm644 %{name}-%{version}/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm644 %{_sourcedir}/hhd-ui.desktop %{buildroot}/usr/share/applications/hhd-ui.desktop

%post
desktop-file-validate %{buildroot}/usr/share/applications/hhd-ui.desktop &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
desktop-file-validate %{buildroot}/usr/share/applications/hhd-ui.desktop &> /dev/null || :
update-desktop-database &> /dev/null || :

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/hhd-ui
%{_datadir}/applications/hhd-ui.desktop
