%define url_ver %(echo %{version} | cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define major 0
%define api 2
%define libname %mklibname %{name} %{api} %{major}
%define oldlibname %mklibname %{name} 2 0
%define develname %mklibname %{name} -d


Summary:	An extension library to Xfce desktop environment
Name:		exo
Version:	4.20.0
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		https://www.xfce.org
Source0:	http://archive.xfce.org/src/xfce/exo/%{url_ver}/%{name}-%{version}.tar.bz2

BuildRequires:	intltool
BuildRequires:	gtk-doc
BuildRequires:	gtk-doc-mkpdf
BuildRequires:	intltool
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxfce4util-1.0)
BuildRequires:	pkgconfig(libxfce4ui-2)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	perl(URI::Escape)
BuildRequires:	perl(URI::file)
BuildRequires:	perl(URI::URL)
BuildRequires:  xfce4-dev-tools
BuildRequires:	glibc-static-devel

%description
This is libexo, an extension library to Xfce, developed by os-cillation.
While Xfce comes with quite a few libraries that are targeted at
desktop development, libexo is targeted at application development.

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README* ChangeLog NEWS
%{_bindir}/exo*
#{_iconsdir}/hicolor/*/*/*.png
%{_mandir}/man1/exo*
%dir %{_datadir}/pixmaps/exo/
%{_datadir}/pixmaps/exo/exo-thumbnail-frame.png
#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	An extension library to Xfce
Group:		System/Libraries
Requires:	%{name} >= %{version}
%rename %{oldlibname}

%description -n %{libname}
Main library for the libexo.

%files -n %{libname}
%license COPYING.LIB
%{_libdir}/libexo-%{api}.so.%{major}{,.*}

#---------------------------------------------------------------------------

%package -n %{develname}
Summary:	Headers, static libraries and documentation for libexo
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}exo1_0-devel
Conflicts:	%{name} < 0.7.0

%description -n %{develname}
Headers, static libraries and documentation for libexo.

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/exo-%{api}/
%{_libdir}/libexo-%{api}.so
%{_libdir}/pkgconfig/exo-%{api}.pc
%{_includedir}/exo-%{api}/

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

# (tpg) already in %{_real_vendor}-xfce-config package
#rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/helpers.rc

# don't ship .la
find %{buildroot} -name "*.la" -delete

# locales
%find_lang %{name}
