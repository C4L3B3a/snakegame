Name: snakegame
Version: 1.0.0
Release: 1%{?dist}
Summary: SnakeGame Developer Kit
License: MIT
Group: Games/Arcade
BuildArch: noarch
Requires: python3

%description
More of a developer kit for Python game developers. A simple snake game built on Python. Open source and easy to install. Includes telemetry, auto-updater, and support portal.

%install
mkdir -p %{buildroot}/usr/local/bin
cp %{_sourcedir}/snakegame-1.0.0/snakegame.py %{buildroot}/usr/local/bin/snakegame
chmod +x %{buildroot}/usr/local/bin/snakegame

%files
/usr/local/bin/snakegame

