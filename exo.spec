%define url_ver %(echo %{version} | cut -d. -f1,2)
%define major 0
%define apiversion 1
%define libname	%mklibname %{name}-%{apiversion}_ %{major}
%define develname %mklibname %{name} -d

Summary:	An extension library to Xfce desktop environment
Name:		exo
Version:	0.7.3
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
BuildRequires:	gtk2-devel
BuildRequires:	libxfce4util-devel >= 4.9.0
BuildRequires:	libxfce4ui-devel >= 4.9.1
BuildRequires:	gtk-doc
BuildRequires:	perl(URI::Escape)
%if %mdkver >= 201200
BuildConflicts:	hal-devel
%else
BuildRequires:	hal-devel
%endif
BuildRequires:	libnotify-devel
BuildRequires:	intltool
Obsoletes:	python-exo < 0.7.2

%description
This is libexo, an extension library to Xfce, developed by os-cillation.
While Xfce comes with quite a few libraries that are targeted at
desktop development, libexo is targeted at application development.

%package -n %{libname}
Summary:	An extension library to Xfce
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Main library for the libexo.

%package -n %{develname}
Summary:	Headers, static libraries and documentation for libexo
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}-%{apiversion}_ 0 -d

%description -n %{develname}
Headers, static libraries and documentation for libexo.

%prep
%setup -q

%build

%configure2_5x \
	--enable-gio-unix \
	--disable-static \
	--enable-gtk-doc

%make

%install
%makeinstall_std

# (tpg) already in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/helpers.rc

%find_lang %{name}-%{apiversion} %{name}.lang

%files -f %{name}.lang
%doc AUTHORS README ChangeLog TODO
%{_bindir}/exo*
%{_libdir}/xfce4/%{name}-%{apiversion}/exo-helper-%{apiversion}
%{_libdir}/xfce4/%{name}-%{apiversion}/exo-compose-mail-%{apiversion}
%{_datadir}/applications/*.desktop
%{_datadir}/xfce4/helpers/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_mandir}/man1/exo*
%{_datadir}/pixmaps/exo-%{apiversion}/exo-thumbnail-frame.png
%{_datadir}/gtk-doc/html/%{name}-%{apiversion}/*

%files -n %{libname}
%{_libdir}/*%{apiversion}.so.%{major}*

%files -n %{develname}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/exo-*%{apiversion}.pc
%{_includedir}/*
