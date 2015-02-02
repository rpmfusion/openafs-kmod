# (un)define the next line to either build for the newest or all current kernels
%global buildforkernels newest

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

%define pre pre1
#define pre %nil

%define kmod_name openafs

# name should have a -kmod suffix
Name:           %{kmod_name}-kmod

Version:        1.6.10
Release:        %{?pre:0.}1%{?pre}%{?dist}.13
Summary:        Kernel module(s)

Group:          System Environment/Kernel

License:        IBM
URL:            http://www.openafs.org
%if %{?pre:1}
Source0:        http://dl.openafs.org/dl/candidate/%{version}%{pre}/%{kmod_name}-%{version}%{pre}-src.tar.bz2
%else
Source0:        http://dl.openafs.org/dl/%{version}/%{kmod_name}-%{version}-src.tar.bz2
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)



%global AkmodsBuildRequires %{_bindir}/kmodtool, pam-devel, ncurses-devel, flex, byacc, bison, automake
BuildRequires: %{AkmodsBuildRequires}

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

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
pushd %{kmod_name}-%{version}%{pre}
./regen.sh
popd

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
    chmod u+x ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{kmod_name}.ko
done

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Mon Feb 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.13
- Rebuilt for kernel

* Sat Jan 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.12
- Rebuilt for kernel

* Thu Dec 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.11
- Rebuilt for kernel

* Sat Dec 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.10
- Rebuilt for kernel

* Sun Nov 23 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.9
- Rebuilt for kernel

* Sun Nov 16 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.8
- Rebuilt for kernel

* Sun Nov 16 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.7
- Rebuilt for kernel

* Mon Nov 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.6
- Rebuilt for kernel

* Fri Oct 31 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.5
- Rebuilt for kernel

* Tue Oct 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.4
- Rebuilt for kernel

* Thu Oct 16 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.3
- Rebuilt for kernel

* Fri Oct 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.2
- Rebuilt for kernel

* Tue Oct 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.6.10-0.1pre1.1
- Rebuilt for kernel

* Tue Sep 23 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.10-0.1pre1
- Update to OpenAFS 1.6.10pre1

* Wed Apr 30 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.8-0.1pre2
- Update to OpenAFS 1.6.8pre2

* Tue Apr 22 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.7-1
- Update to OpenAFS 1.6.7 final

* Wed Jan 22 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.6-1
- Update to OpenAFS 1.6.6 final

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.6.6-0.pre1.4
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.6.6-0.pre1.3
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.6.6-0.pre1.2
- Rebuilt for current kernel

* Sun Dec 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.6.6-0.pre1.1
- Rebuilt for f20 final kernel

* Sat Nov 30 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.6-0.pre1
- Update to OpenAFS 1.6.6pre1

* Fri Oct 11 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.5.1-1
- Update to OpenAFS 1.6.5.1

* Wed Jul 24 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.5-1
- Update to OpenAFS 1.6.5

* Thu Jul 04 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.4-1
- Update to OpenAFS 1.6.4

* Tue Apr 30 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.2.1-1
- Update to OpenAFS 1.6.2.1
- Add patches to support kernel 3.9

* Sat Mar 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.2-3
- Add patches to support kernel 3.8

* Thu Feb 21 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.2-2
- Use newer tarball for 1.6.2 final

* Thu Feb 14 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.2-1
- Update to OpenAFS 1.6.2 final

* Tue Jan 22 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.2-0.pre3
- Update to OpenAFS 1.6.2 pre-release 3

* Wed Dec 26 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.2-0.pre2
- Update to OpenAFS 1.6.2 pre-release 2

* Tue Dec 11 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.2-0.pre1
- Update to OpenAFS 1.6.2 pre-release 1
- Remove upstreamed patches

* Sat Oct 06 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.1-4
- Rebuild for F-18 Beta. Debugging is now disabled in F-18 kernels.

* Wed Sep 19 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.1-3
- Add upstream patches for kernel 3.6

* Wed Aug 01 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.1-2
- Add upstream patches for kernel 3.5

* Wed Apr 04 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.1-1
- Update to OpenAFS 1.6.1 final

* Wed Mar 07 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.1-0.pre4
- Update to OpenAFS 1.6.1 pre-release 4

* Tue Feb 28 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.1-0.pre3
- Update to OpenAFS 1.6.1 pre-release 3

* Wed Feb 08 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.1-0.pre2
- Update to OpenAFS 1.6.1 pre-release 2

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.6.1-0.pre1.1
- Rebuild for UsrMove

* Fri Dec 30 2011 Ken Dreyer <ktdreyer@ktdreyer.com> 0:1.6.1-0.pre1
- Update to OpenAFS 1.6.1 pre-release 1

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-2.4
- Rebuild for F-16 kernel

* Tue Nov 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-2.3
- Rebuild for F-16 kernel

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-2.2
- Rebuild for F-16 kernel

* Sun Oct 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-2.1
- Rebuild for F-16 kernel

* Fri Oct 14 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-2
- rpmFusion Bug # 1938 Patch from Ken Dreyer
- correct akmod package build deps

* Tue Sep 06 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-1
- Update to OpenAFS 1.6.0 final

* Sat Sep 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-0.pre7.5
- rebuild for updated kernel

* Wed Aug 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-0.pre7.4
- rebuild for updated kernel

* Sun Jul 31 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-0.pre7.3
- rebuild for updated kernel

* Thu Jul 21 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-0.pre7
- Update to OpenAFS 1.6.0 pre-release 7

* Tue Jul 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.6.0-0.pre6.2
- Rebuild for updated kernel

* Wed Jun 15 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.6.0-0.pre6.1
- rebuild for updated kernel

* Wed Jun 08 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-0.pre6
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


