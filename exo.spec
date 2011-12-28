%define url_ver %(echo %{version} | cut -d. -f1,2)
%define major 0
%define apiversion 1
%define libname	%mklibname %{name}-%{apiversion}_ %{major}
%define develname %mklibname %{name} -d

Summary:	An extension library to Xfce desktop environment
Name:		exo
Version:	0.6.2
Release:	%mkrel 5
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
Patch0:		exo-0.6.2-fix-glib-linking.patch
Patch1:		exo-0.6.2-fix-lm-linking.patch
BuildRequires:	gtk2-devel
BuildRequires:	libxfcegui4-devel >= 4.6.0
BuildRequires:	gtk-doc
BuildRequires:	perl(URI::Escape)
%if %mdkver >= 201200
BuildConflicts:	hal-devel
%else
BuildRequires:	hal-devel
%endif
BuildRequires:	libnotify-devel
BuildRequires:	intltool
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%package -n python-%{name}
Summary:	Python bindings for the exo library
Group:		Development/Python
%py_requires -d
BuildRequires:	pygtk2.0-devel

%description -n python-%{name}
This package contains a module that allow monitoring of
files and directories from the Python language based on the support
of the libexo package.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# (tpg) needed for both patches
NOCONFIGURE=1 xdt-autogen

%configure2_5x \
	--enable-gio-unix \
	--enable-python \
	--disable-static \
	--enable-gtk-doc

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# (tpg) already in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/helpers.rc

# (tpg) drop static libraries
rm -rf %{buildroot}%{libdir}/*.a
rm -rf %{buildroot}%{libdir}/*.la

%find_lang %{name}-%{apiversion} %{name}.lang

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
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
%defattr(-,root,root)
%{_libdir}/*%{apiversion}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/exo-*%{apiversion}.pc
%{_includedir}/*

%files -n python-%{name}
%defattr(-,root,root)
%doc python/examples/README python/examples/ellipsizing.py python/examples/toolbars.py
%{_datadir}/pygtk/2.0/defs/exo*
%{_libdir}/python*/site-packages/exo*
%{py_sitedir}/pyexo*
