%global HHD_VERSION 2.4.2

Requires:      hhd
Requires:      hhd-ui
Requires:      adjustor
Recommends:    gamescope-session-plus
Recommends:    gamescope-session-steam

Conflicts:     HandyGCCS
Conflicts:     inputplumber
Conflicts:     rogue-enemy
Conflicts:     lgcd

Obsoletes:     hhd = 1.3.6-2
Provides:      hhd-meta

BuildArch:     noarch
Name:          hhd-meta
Version:       %{HHD_VERSION}
Release:       1.copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Snapshot of the complete Handheld Daemon package

Source:        dummy-file.txt
Patch0:        0001-add-files-for-autostart.patch

%description
Full suite of Handheld Daemon (hhd) software, including the adjustor and UI.

%prep
mkdir -p %{name}-%{version}
%patch -P 0 -p1

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
install -m775 etc/xdg/autostart/hhd.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/hhd.desktop
mkdir -p %{buildroot}%{_libexecdir}/
install -m775 usr/libexec/enable-hhd %{buildroot}%{_libexecdir}/enable-hhd
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
install -m644 usr/share/polkit-1/actions/org.hhd.start.policy %{buildroot}%{_datadir}/polkit-1/actions/org.hhd.start.policy

%pre

%post
udevadm control --reload-rules
udevadm trigger

%files
%{_libexecdir}/enable-hhd
%{_sysconfdir}/xdg/autostart/hhd.desktop
%{_datadir}/polkit-1/actions/org.hhd.start.policy
