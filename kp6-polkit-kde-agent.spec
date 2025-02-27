#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.3.2
%define		qtver		5.15.2
%define		kpname		polkit-kde-agent

Summary:	Daemon providing a polkit authentication UI for KDE
Name:		kp6-%{kpname}
Version:	6.3.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-1-%{version}.tar.xz
# Source0-md5:	5bdd87252dc6713f4b9ebd44e2caaf4e
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-kcrash-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	ninja
BuildRequires:	polkit-qt6-1-gui-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Daemon providing a polkit authentication UI for KDE.

%prep
%setup -q -n %{kpname}-1-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/polkit-kde-authentication-agent-1
/etc/xdg/autostart/polkit-kde-authentication-agent-1.desktop
%{_desktopdir}/org.kde.polkit-kde-authentication-agent-1.desktop
%{systemduserunitdir}/plasma-polkit-agent.service
%{_datadir}/knotifications6/policykit1-kde.notifyrc
