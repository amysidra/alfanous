%global pybasever %(%{__python} -c "import sys ; print(sys.version[:3])")
%global python_sitelib  %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:    alfanous
Summary: Alfanous is a search engine API provide the simple and advanced search in the Holy Qur'an and more features.
Version: alfanous.version
Release: alfanous.release%{?dist}
License: AGPL3
Url:     http://www.alfanous.org
#Source0: alfanous-alfanous.version.tar.gz
Source1: alfanous.xml
Group:   Quran/Tools
BuildRequires: python python-setuptools python-configobj unzip ImageMagick
Requires:      python python-configobj python-alfanous python-jinja2 islamic-menus
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
BuildRequires: python-pyside-devel pyside-tools pyparsing python-babel babel qt-devel
Requires:      python-pyside pyparsing
%endif
%if 0%{?suse_version}
BuildRequires: python-pyside-devel python-pyside-tools python-pyparsing python-Babel libqt4-linguist
Requires:      python-pyside python-pyparsing
%endif
BuildArch:     noarch

%description
Alfanous is a search engine API provide the simple and advanced search in the Holy Qur'an and more features.

%package firefox-toolbar
Summary:    Firefox Toolbar for Alfanous.
Group:      Quran/Tools
Requires:   firefox

%description firefox-toolbar
Firefox Toolbar for Alfanous.

%package firefox-searchplugins
Summary:    Firefox Searchplugins for Alfanous.
Group:      Quran/Tools
Requires:   firefox

%description firefox-searchplugins
Firefox Searchplugins for Alfanous.

%package -n python-alfanous
Summary:    Alfanous python library.
Group:      python/library
Requires:   python

%description -n python-alfanous
Alfanous python library.

%prep
#%setup -q
rm -rf   %{_builddir}/alfanous-alfanous.version
mkdir -p %{_builddir}/alfanous-alfanous.version
cd ../..
cp -r `cat list.txt`  %{_builddir}/alfanous-alfanous.version
%if 0%{?suse_version}
perl -pi -w -e 's|lrelease-qt4|lrelease|g;' Makefile
%endif

%build
cd alfanous-alfanous.version
make build

%install
cd alfanous-alfanous.version
make install_desktop DESTDIR=%{buildroot}

# Install icon
for res in 16x16 22x22 24x24 32x32 36x36 48x48 64x64 72x72 96x96; do \
  %{__mkdir_p} %{buildroot}/%{_datadir}/icons/hicolor/${res}/apps
  convert -size 121x119 %{buildroot}%{_datadir}/pixmaps/AlFanous.png -resize ${res} %{buildroot}%{_datadir}/icons/hicolor/${res}/apps/AlFanous.png
done;

#Install firefox toolbar
perl -pi -e 's/>18.0a1/>20.*/g' interfaces/toolbars/firefox/install.rdf
install -d -m 755 %{buildroot}%{_datadir}/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}/alfanousQSE@gmail.com
cp -r interfaces/toolbars/firefox/* %{buildroot}%{_datadir}/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}/alfanousQSE@gmail.com

#Install firefox searchplugins
install -d -m 755 %{buildroot}%{_libdir}/firefox/searchplugins
install -D -m 644 %{SOURCE1} %{buildroot}%{_libdir}/firefox/searchplugins

# move fonts to alfanous folder
mkdir -p %{buildroot}%{_datadir}/fonts/alfanous
mv %{buildroot}%{_datadir}/fonts/*.ttf %{buildroot}%{_datadir}/fonts/alfanous

# fix pyside not found error
perl -pi -w -e 's|pyside||g;' %{buildroot}%{python_sitelib}/alfanousDesktop-%{version}-py%{pybasever}.egg-info/requires.txt

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/alfanous*
%{_datadir}/applications/alfanous.desktop
%{_datadir}/pixmaps/AlFanous.png
%{_datadir}/icons/hicolor/*/apps/AlFanous.png
%{_datadir}/fonts/alfanous
%if 0%{?suse_version}
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/*
%dir %{_datadir}/icons/hicolor/*/apps
%endif

%files firefox-toolbar
%defattr(-,root,root)
%{_datadir}/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}/alfanousQSE@gmail.com
%if 0%{?suse_version}
%dir %{_datadir}/mozilla
%dir %{_datadir}/mozilla/extensions
%dir %{_datadir}/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}
%endif

%files firefox-searchplugins
%defattr(-,root,root)
%{_libdir}/firefox/searchplugins/alfanous.xml
%if 0%{?suse_version}
%dir %{_libdir}/firefox
%dir %{_libdir}/firefox/searchplugins
%endif

%files -n python-alfanous
%defattr(-,root,root)
%{python_sitelib}/alfanous*

%changelog
* Tue Mar 03 2015 Muhammad Shaban <Mr.Muhammad@outlook.com> 0.7.10-3
- update

* Sun Jan 04 2015 Muhammad Shaban <Mr.Muhammad@outlook.com> 0.7.02-6
- fix errors when use (make dist_rpm)

* Sun Jan 04 2015 Muhammad Shaban <Mr.Muhammad@outlook.com> 0.7.02-5
- fix pyside not found error

* Thu Jan 01 2015 Muhammad Shaban <Mr.Muhammad@outlook.com> 0.7.02-4
- update
- exchange PyQt4 with PySide
- fix desktop file errors

* Sun Feb 10 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> 0.7-4
- split alfanous package to alfanous & python-alfanous

* Sat Feb 09 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> 0.7-3
- remove packages chrome-toolbar & chromium-toolbar not working

* Thu Feb 07 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> 0.7-2
- add new packages firefox-toolbar & firefox-searchplugins
- add new packages chrome-toolbar & chromium-toolbar

* Mon Feb 04 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> 0.7-1
- Initial Build
