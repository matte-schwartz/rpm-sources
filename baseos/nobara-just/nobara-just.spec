Name:           nobara-just
Packager:       nobara
Vendor:         nobara
Version:        0.2
Release:        1%{?dist}
Summary:        nobara just integration
License:        MIT
URL:            https://github.com/ublue-os/config

BuildArch:      noarch
Requires:       just

Source0:        nobara-just.sh
Source1:        00-nobara-base.just
Source2:        85-nobara-image.just
Source3:        nojust
Source4:       nogum
Source5:       header.just
Source6:       nojust.sh
Source7:       libcolors.sh
Source8:       libformatting.sh
Source9:       libfunctions.sh

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^nobara%-", ""); print(t)}

%description
Adds nobara just integration for easier setup

%prep
%setup -q -c -T

%build

mkdir -p -m0755  %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}
install -Dm755 %{SOURCE0}  %{buildroot}%{_sysconfdir}/profile.d/nobara-just.sh
cp %{SOURCE1} %{SOURCE2} %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}

# Create justfile which contains all .just files included in this package
# Apply header first due to default not working in included justfiles
cp %{SOURCE5} "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
for justfile in %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/*.just; do
	echo "import \"%{_datadir}/%{VENDOR}/%{sub_name}/$(basename ${justfile})\"" >> "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
done

# Add global "nojust" script to run just with --unstable
mkdir -p -m0755  %{buildroot}%{_bindir}
install -Dm755 %{SOURCE3} %{buildroot}%{_bindir}/nojust
install -Dm755 %{SOURCE4} %{buildroot}%{_bindir}/nogum

# Add bash library for use in just
mkdir -p -m0755 %{buildroot}/%{_exec_prefix}/lib/nojust/
install -Dm644 %{SOURCE6} %{buildroot}/%{_exec_prefix}/lib/nojust
install -Dm644 %{SOURCE7} %{buildroot}/%{_exec_prefix}/lib/nojust
install -Dm644 %{SOURCE8} %{buildroot}/%{_exec_prefix}/lib/nojust
install -Dm644 %{SOURCE9} %{buildroot}/%{_exec_prefix}/lib/nojust


%files
%dir %attr(0755,root,root) %{_datadir}/%{VENDOR}/%{sub_name}
%attr(0755,root,root) %{_sysconfdir}/profile.d/nobara-just.sh
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/*.just
%attr(0644,root,root) %{_datadir}/%{VENDOR}/justfile
%attr(0755,root,root) %{_bindir}/nojust
%attr(0755,root,root) %{_bindir}/nogum
%attr(0644,root,root) %{_exec_prefix}/lib/nojust/nojust.sh
%attr(0644,root,root) %{_exec_prefix}/lib/nojust/lib*.sh

%post
# Generate nojust bash completion
just --completions bash | sed -E 's/([\(_" ])just/\1nojust/g' > %{_datadir}/bash-completion/completions/nojust
chmod 644 %{_datadir}/bash-completion/completions/nojust

%changelog
* Mon Jan 29 2024 Matthew Schwartz <njtransit215@gmail.com> - 0.1
- Initial package import from Bazzite (thanks!)
