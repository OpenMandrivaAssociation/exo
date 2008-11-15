%define major 0
%define apiversion 0.3
%define libname	%mklibname %{name}-%{apiversion}_ %{major}
%define develname %mklibname %{name} -d

Summary:	An extension library to Xfce desktop environment
Name:		exo
Version:	0.3.92
Release:	%mkrel 2
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.xfce.org
Source:		%{name}-%{version}.tar.bz2
Patch2:		%{name}-0.3.2-iocharset.patch
Patch3:         %{name}-0.3.2-eject-volume.patch
Patch4:		%{name}-linkage_fix.diff
BuildRequires:	gtk2-devel
BuildRequires:	libxfcegui4-devel
BuildRequires:	gtk-doc
%py_requires -d
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
BuildRequires:	pygtk2.0-devel

%description -n python-%{name}
This package contains a module that allow monitoring of
files and directories from the Python language based on the support
of the libexo package.

%prep
%setup -q
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# (tpg) needed for patch 4
NOCONFIGURE=1 xdt-autogen

%configure2_5x \
%if %mdkversion < 200900
	--sysconfdir=%{_sysconfdir}/X11 \
%endif
	--enable-notifications \
	--enable-hal \
	--enable-python \
	--disable-static \
	--enable-gtk-doc

%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang lib%{name}-%{apiversion}

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

%files
%defattr(-,root,root)
%doc AUTHORS README HACKING ChangeLog TODO
%doc %{_datadir}/xfce4/doc/C
%doc %{_datadir}/xfce4/doc/ja
%doc %{_datadir}/xfce4/doc/fr/exo-preferred-applications.html
%doc %{_datadir}/xfce4/doc/fr/images/*
%if %mdkversion < 200900
%exclude %{_sysconfdir}/X11/xdg/xfce4/helpers.rc
%else
%exclude %{_sysconfdir}/xdg/xfce4/helpers.rc
%endif
%{_bindir}/exo*
%{_datadir}/applications/exo-preferred-applications.desktop
%{_datadir}/xfce4/helpers/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_mandir}/man1/exo*
%{_datadir}/pixmaps/exo-0.3/exo-thumbnail-frame.png
%{_datadir}/gtk-doc/html/%{name}/*

%files -n %{libname} -f lib%{name}-%{apiversion}.lang
%defattr(-,root,root)
%{_libdir}/exo-helper-0.3
%{_libdir}/exo-compose-mail-0.3
%{_libdir}/*%{apiversion}.so.%{major}*
%{_libdir}/exo-mount-notify-0.3

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_libdir}/pkgconfig/exo-*0.3.pc
%{_includedir}/*

%files -n python-%{name}
%defattr(-,root,root)
%doc python/examples/README python/examples/ellipsizing.py python/examples/toolbars.py
%{_datadir}/pygtk/2.0/defs/exo-0.3
%{_libdir}/python*/site-packages/exo-0.3
%{py_sitedir}/pyexo*
