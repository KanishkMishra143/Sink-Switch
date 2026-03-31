Name:           sink-switch
Version:        1.1
Release:        1%{?dist}
Summary:        Simple audio sink switcher for PulseAudio/PipeWire

License:        MIT
URL:            https://github.com/KanishkMishra143/sink-switch
Source0:        https://github.com/KanishkMishra143/sink-switch/archive/refs/tags/v1.1.tar.gz

BuildArch:      noarch
Requires:       bash, pulseaudio-utils, libnotify, python3, python3-gobject, gtk4, libadwaita

%description
A simple Bash script and GTK GUI to switch between available audio output sinks dynamically using pactl.
Supports notifications, cycling, setting by name, and more.

%prep
%setup -q

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 sink-switch.sh %{buildroot}%{_bindir}/sink-switch
install -m 0755 sink-switch-gui.py %{buildroot}%{_bindir}/sink-switch-gui.py

%files
%license LICENSE
%doc README.md
%{_bindir}/sink-switch
%{_bindir}/sink-switch-gui.py

%changelog
* Tue Mar 31 2026 Kanishk Mishra <kanishk.mishra012@adgitmdelhi.ac.in> - 1.1-1
- Added GTK GUI and shared configuration support
