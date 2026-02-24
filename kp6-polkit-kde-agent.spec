#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.6.1
%define		qtver		5.15.2
%define		kpname		polkit-kde-agent

Summary:	Daemon providing a polkit authentication UI for KDE
Name:		kp6-%{kpname}
Version:	6.6.1
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-1-%{version}.tar.xz
# Source0-md5:	744e07404850d49d81c1e9b7c24c3cd2
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
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
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

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/polkit-kde-authentication-agent-1
/etc/xdg/autostart/polkit-kde-authentication-agent-1.desktop
%{_desktopdir}/org.kde.polkit-kde-authentication-agent-1.desktop
%{systemduserunitdir}/plasma-polkit-agent.service
%{_datadir}/knotifications6/polkit-kde-authentication-agent-1.notifyrc
