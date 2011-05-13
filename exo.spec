%define url_ver %(echo %{version} | cut -c 1-3)
%define major 0
%define apiversion 1
%define libname	%mklibname %{name}-%{apiversion}_ %{major}
%define develname %mklibname %{name} -d

Summary:	An extension library to Xfce desktop environment
Name:		exo
Version:	0.6.1
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.xfce.org
Source:		http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
BuildRequires:	gtk2-devel
BuildRequires:	libxfcegui4-devel >= 4.6.0
BuildRequires:	gtk-doc
BuildRequires:	perl(URI::Escape)
BuildRequires:	hal-devel
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

%build

%configure2_5x \
%if %mdkversion < 200900
	--sysconfdir=%{_sysconfdir}/X11 \
%endif
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

%find_lang %{name}-%{apiversion}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post
%{update_menus}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

%files -f %{name}-%{apiversion}.lang
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
%{_libdir}/lib*.*a
%{_libdir}/pkgconfig/exo-*%{apiversion}.pc
%{_includedir}/*

%files -n python-%{name}
%defattr(-,root,root)
%doc python/examples/README python/examples/ellipsizing.py python/examples/toolbars.py
%{_datadir}/pygtk/2.0/defs/exo*
%{_libdir}/python*/site-packages/exo*
%{py_sitedir}/pyexo*
