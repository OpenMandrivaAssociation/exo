%define url_ver %(echo %{version} | cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define major 0
%define api 1
%define libname %mklibname %{name} %{api} %{major}
%define develname %mklibname %{name} -d

%define api2 2
%define lib2name %mklibname %{name} %{api2} %{major}

Summary:	An extension library to Xfce desktop environment
Name:		exo
Version:	0.12.2
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/exo/%{url_ver}/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxfce4util-1.0) >= 4.12.0
BuildRequires:	pkgconfig(libxfce4ui-1) >= 4.12.0
BuildRequires:	pkgconfig(libxfce4ui-2)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	perl(URI::Escape)
BuildRequires:	perl(URI::file)
BuildRequires:	perl(URI::URL)
BuildRequires:	intltool

%description
This is libexo, an extension library to Xfce, developed by os-cillation.
While Xfce comes with quite a few libraries that are targeted at
desktop development, libexo is targeted at application development.

%package -n %{libname}
Summary:	An extension library to Xfce
Group:		System/Libraries
Requires:	%{name} >= %{version}
#Added 01/2012 (wally)
Obsoletes:	%{_lib}%{name}-1_0 < 0.7.0

%description -n %{libname}
Main library for the libexo.

%package -n %{lib2name}
Summary:        An extension library to Xfce
Group:          System/Libraries
Requires:       %{name} >= %{version}

%description -n %{lib2name}
Main library for the libexo

%package -n %{develname}
Summary:	Headers, static libraries and documentation for libexo
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{lib2name} = %{version}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}exo1_0-devel
Conflicts:	%{name} < 0.7.0

%description -n %{develname}
Headers, static libraries and documentation for libexo.

%prep
%setup -q

%build
%configure \
	--disable-static

%make

%install
%makeinstall_std

# (tpg) already in %{_real_vendor}-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/helpers.rc

# don't ship .la
find %{buildroot} -name "*.la" -delete

%find_lang %{name}-%{api}

%files -f %{name}-%{api}.lang
%doc AUTHORS README ChangeLog TODO
%{_bindir}/exo*
%{_libdir}/xfce4/%{name}-%{api}/exo-helper-%{api}
%{_libdir}/xfce4/%{name}-%{api}/exo-compose-mail-%{api}
%{_datadir}/applications/*.desktop
%{_datadir}/xfce4/helpers/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_mandir}/man1/exo*
%{_datadir}/pixmaps/exo-%{api}/exo-thumbnail-frame.png

%files -n %{libname}
%{_libdir}/lib%{name}-%{api}.so.%{major}*

%files -n %{lib2name}
%{_libdir}/lib%{name}-%{api2}.so.%{major}*

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/%{name}-%{api}/
%{_libdir}/lib%{name}-%{api}.so
%{_libdir}/lib%{name}-%{api2}.so
%{_libdir}/pkgconfig/%{name}-%{api}.pc
%{_libdir}/pkgconfig/%{name}-%{api2}.pc
%{_includedir}/*
