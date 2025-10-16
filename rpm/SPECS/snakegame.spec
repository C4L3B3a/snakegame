Name: snakegame
Version: 1.0.0
Release: 1%{?dist}
Summary: SnakeGame Developer Kit
License: MIT
Group: Games/Arcade
BuildArch: noarch
Requires: python3

%description
A developer kit for Python game developers. Includes telemetry, auto-updater, and support portal.

%install
mkdir -p %{buildroot}/usr/local/bin
cp %{_sourcedir}/snakegame.py %{buildroot}/usr/local/bin/snakegame
chmod +x %{buildroot}/usr/local/bin/snakegame

%files
/usr/local/bin/snakegame
