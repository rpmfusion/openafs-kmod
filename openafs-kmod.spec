# (un)define the next line to either build for the newest or all current kernels
%define buildforkernels newest
#define buildforkernels current
#define buildforkernels akmods

# Define the OpenAFS sysname
%ifarch %{ix86} 
%define sysname i386_linux26
%endif
%ifarch ppc
%define sysname ppc_linux26
%endif
%ifarch ppc64
%define sysname ppc64_linux26
%endif
%ifarch x86_64
%define sysname amd64_linux26
%endif

%define kmod_name openafs

%define pre pre6

# name should have a -kmod suffix
Name:           %{kmod_name}-kmod

Version:        1.6.0
Release:        0.%{pre}%{?dist}
Summary:        Kernel module(s)

Group:          System Environment/Kernel

License:        IBM
URL:            http://www.openafs.org
Source0:        http://www.openafs.org/dl/openafs/%{version}/%{kmod_name}-%{version}%{pre}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{_bindir}/kmodtool
BuildRequires:  pam-devel, ncurses-devel, flex, byacc, bison, automake

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
This package provides %{kmod_name} kernel modules.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

# apply patches and do other stuff here
#pushd %{kmod_name}-%{version}%{pre}
#popd

for kernel_version in %{?kernel_versions} ; do
    cp -a %{kmod_name}-%{version}%{pre} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}
    %{configure} --with-afs-sysname=%{sysname} --enable-kernel-module \
        --disable-linux-syscall-probing  \
        --with-linux-kernel-headers="${kernel_version##*__}"
    make MPS=MP only_libafs
    popd   
done


%install
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do

    install -d -m 755 ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install -m 755 _kmod_build_${kernel_version%%___*}/src/libafs/MODLOAD-${kernel_version%%___*}-MP/libafs.ko \
        ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{kmod_name}.ko
done

chmod u+x ${RPM_BUILD_ROOT}/lib/modules/*/extra/*/*

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Jun 08 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0.0.pre6
- Update to OpenAFS 1.6.0 pre-release 6

* Sat Jun 04 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.6.0-0.pre4.3
- rebuild for updated kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.6.0-0.pre4.2
- rebuild for updated kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.6.0-0.pre4.1
- rebuild for F15 release kernel

* Thu Apr 14 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-0.pre4
- Update to OpenAFS 1.6.0 pre-release 4
- Applied 0001-Linux-2.6.39-deal-with-BKL-removal.patch and
  0002-Linux-2.6.39-replace-path_lookup-with-kern_path.patch
  to get the kmod to build on current F15 kernels.

* Tue Jan 11 2011 Jack Neely <jjneely@ncsu.edu> 0:1.4.14-1
- Build 1.4.14

* Fri Jun 11 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.12.1-2
- Build in devel branch for rawhide

* Thu May 27 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.12.1-1
- Build for F-13
- Port forward to 1.4.12.1

* Sat May 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.12-1.7
- rebuild for new kernel

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.12-1.6
- rebuild for new kernel

* Thu Apr 22 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.12-1.5
- rebuild for new kernel

* Mon Apr 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.12-1.4
- rebuild for new kernel

* Sat Apr 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.12-1.3
- rebuild for new kernel

* Sat Apr 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.12-1.2
- rebuild for new kernel

* Mon Mar 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.12-1.1
- rebuild for new kernel

* Mon Mar 15 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.12-1
- Update to OpenAFS 1.4.12

* Fri Mar 05 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.9
- rebuild for new kernel

* Mon Mar 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.8
- rebuild for new kernel

* Sun Feb 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.7
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.6
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.5
- rebuild for new kernel

* Thu Feb 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.4
- rebuild for new kernel

* Wed Feb 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.3
- rebuild for new kernel

* Sat Jan 30 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.2
- rebuild for new kernel

* Wed Jan 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.11-6.1
- rebuild for new kernel

* Mon Jan 11 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.11-6
- Build with --disable-linux-syscall-probing to fix compile issues
  on PPC.  Syscall probing is useless on modern linux kernels

* Wed Jan 06 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.11-5
- Correct AFS sysname for the ppc64 arch

* Tue Jan 05 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.11-4
- add buildrequires for bison

* Mon Nov 02 2009 Jack Neely <jjneely@ncsu.edu> 0:1.4.11-3
- remove the repo macro

* Tue Sep 08 2009 Jack Neely <jjneely@ncsu.edu> 0:1.4.11-2
- release bump

* Thu Sep 03 2009 Jack Neely <jjneely@ncsu.edu> 1.4.11-1
- port to kmod v2

* Tue Jun 02 2009 Jack Neely <jjneely@ncsu.edu> 1.4.10
- Setup for Fedora 11 in prep for RHEL 6
- Apply the dprint patch
- Apply the kmodule26 patch to better rename the ko to openafs rather
  than libafs.  This is from the OpenAFS stock packages

* Fri May 18 2007 Jack Neely <jjneely@ncsu.edu> 1.4.4-3
- Rebuild for kernel 2.6.18-8.1.4.el5

* Thu Mar 15 2007 Jack Neely <jjneely@ncsu.edu> 1.4.3-0.3RC
- Build for RHEL 5 using the latest 1.4.3 release canidate 3

* Wed Jun 28 2006 Jack Neely <jjneely@ncsu.edu> 1.4.1-4
- Repackaging using latest FC kernel module proposal.


