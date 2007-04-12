%define	version		0.3.2
%define release		2

%define lib_major	0
%define lib_name	%mklibname %{name}-0.3_ %{lib_major}

%define __libtoolize	/bin/true
 
Summary:	An extension library to Xfce 
Name:		exo
Version:	%{version}
Release:	%mkrel %{release}
License:	GPL 
Group:		System/Libraries 
Source:		%{name}-%{version}.tar.bz2
URL:		http://www.os-cillation.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}beta2-buildroot
BuildRequires:	 gtk2-devel
BuildRequires:	 libxfcegui4-devel
BuildRequires:	 xfce-mcs-manager-devel
BuildRequires:	 startup-notification-devel
BuildRequires:	 python
BuildRequires:   perl(URI::Escape)
BuildRequires:   hal-devel
BuildRequires:   libnotify-devel
BuildRequires:   gnome-doc-utils

%description
This is libexo, an extension library to Xfce, developed by os-cillation. 
While Xfce comes with quite a few libraries that are targeted at 
desktop development, libexo is targeted at application development. 
 
%package	-n %{lib_name}
Summary:	An extension library to Xfce
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}

%description	-n %{lib_name}
This is libexo, an extension library to Xfce, developed by os-cillation. 
While Xfce comes with quite a few libraries that are targeted at 
desktop development, libexo is targeted at application development.
 
%package	-n %{lib_name}-devel
Summary:	Exo headers, static libraries and documentation
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-0.3-devel = %{version}-%{release}
Obsoletes:	libexo-0.2_0-devel
Provides:	libexo-0.2_0-devel
Provides:	exo-devel = %{version}-%{release}

%description -n %{lib_name}-devel
Exo headers, static libraries and documentation  

%package -n python-%{name}
Summary: Python bindings for the exo library
Group: Development/Python
BuildRequires: pygtk2.0-devel

%description -n python-%{name}
This package contains a module that allow monitoring of
files and directories from the Python language based on the support
of the libexo package.
 
%prep
%setup -q -n %{name}-%{version}

%build 
%configure2_5x --enable-gtk-doc --sysconfdir=%{_sysconfdir}/X11 --enable-hal --enable-gtk-doc --enable-xsltproc --enable-xml2po
                       
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

##rm unneeded file
rm -f $RPM_BUILD_ROOT/%{_libdir}/python2.4/site-packages/exo-0.3/_exo.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/xfce4/mcs-plugins/exo-preferred-applications-settings.*a

%find_lang lib%{name}-0.3
 
%clean
rm -rf $RPM_BUILD_ROOT

%post  -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%defattr(-,root,root,0755)
%doc AUTHORS README COPYING HACKING INSTALL TODO
%doc %{_datadir}/xfce4/doc/C
%doc %{_datadir}/xfce4/doc/ja
%doc %{_datadir}/xfce4/doc/fr/exo-preferred-applications.html
%doc %{_datadir}/xfce4/doc/fr/images/*
%config(noreplace) /%{_sysconfdir}/X11/xdg/xfce4/helpers.rc
%{_bindir}/exo*
%{_libdir}/xfce4/mcs-plugins/exo-preferred-applications-settings.so
%{_datadir}/applications/exo-preferred-applications.desktop
%{_datadir}/icons/hicolor/48x48/apps/preferences-desktop-default-applications.png
%{_datadir}/xfce4/helpers/*.desktop
%{_iconsdir}/hicolor/48x48/apps/*.png
%{_mandir}/man1/exo*
%{_datadir}/icons/hicolor/24x24/apps/preferences-desktop-default-applications.png
%{_datadir}/pixmaps/exo-0.3/exo-thumbnail-frame.png

%files -n %{lib_name}
%defattr(-,root,root,0755)
%{_libdir}/exo-helper-0.3
%{_libdir}/exo-compose-mail-0.3
%{_libdir}/lib*.so.*
%{_libdir}/exo-mount-notify-0.3

%files -n %{lib_name}-devel -f libexo-0.3.lang
%defattr(-,root,root,0755) 
%dir %{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gtk-doc/html/%{name}/* 
%{_libdir}/lib*.so 
%{_libdir}/lib*.*a
%{_libdir}/pkgconfig/exo-*0.3.pc

 
%{_includedir}/*

%files -n python-%{name}
%defattr(-, root, root)
%doc python/examples/README python/examples/ellipsizing.py python/examples/toolbars.py 
%{_datadir}/pygtk/2.0/defs/exo-0.3
%{_libdir}/python*/site-packages/exo-0.3 
%{_prefix}/lib/python*/site-packages/pyexo*
 


