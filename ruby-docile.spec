#
# Conditional build:
%bcond_without	doc	# ri/rdoc documentation

%define pkgname docile
Summary:	Docile turns any Ruby object into a DSL
Summary(pl.UTF-8):	Docile - przekształcanie obiektów języka Ruby do DSL-a
Name:		ruby-%{pkgname}
Version:	1.1.5
Release:	1
License:	MIT
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	5e5baf4ed5c4b1090914ccd30f2da075
Group:		Development/Languages
URL:		https://rubygems.org/gems/simplecov
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby >= 1:1.8.7
Requires:	ruby >= 1:1.8.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Docile turns any Ruby object into a DSL. Especially useful with the
Builder pattern.

%description -l pl.UTF-8
Docile przekształca obiekty języka Ruby do DSL-a. Przydatne
szczególnie wraz z wzorcem Builder.

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} -r ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_ridir},%{ruby_rdocdir}/%{name}-%{version}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}

cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

# install gemspec
install -d $RPM_BUILD_ROOT%{ruby_specdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY.md LICENSE README.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Docile
%endif
