#############################################################################
#
# This is the spec file for the distribution specific RPM files
#
##############################################################################

##############################################################################
# Some common macro definitions
##############################################################################

# Required arguments
# gotrevision - Revision in BZR branch

%define mysql_vendor  Percona, Inc
%define redhatversion %(lsb_release -rs | awk -F. '{ print $1}')
%define community 1
%define mysqlversion 5.1.69
%define majorversion 14
%define minorversion 7
%define distribution  rhel%{redhatversion}
%define release       rel%{majorversion}.%{minorversion}.%{gotrevision}.%{distribution}

%define mysqld_user	mysql
%define mysqld_group	mysql
%define mysqldatadir	/var/lib/mysql
%define see_base For a description of MySQL see the base MySQL RPM or http://www.mysql.com

# ------------------------------------------------------------------------------
# Meta information, don't remove!
# ------------------------------------------------------------------------------
# norootforbuild

# ------------------------------------------------------------------------------
# On SuSE 9 no separate "debuginfo" package is built. To enable basic
# debugging on that platform, we don't strip binaries on SuSE 9. We
# disable the strip of binaries by redefining the RPM macro
# "__os_install_post" leaving out the script calls that normally does
# this. We do this in all cases, as on platforms where "debuginfo" is
# created, a script "find-debuginfo.sh" will be called that will do
# the strip anyway, part of separating the executable and debug
# information into separate files put into separate packages.
#
# Some references (shows more advanced conditional usage):
# http://www.redhat.com/archives/rpm-list/2001-November/msg00257.html
# http://www.redhat.com/archives/rpm-list/2003-February/msg00275.html
# http://www.redhat.com/archives/rhl-devel-list/2004-January/msg01546.html
# http://lists.opensuse.org/archive/opensuse-commit/2006-May/1171.html
# ------------------------------------------------------------------------------
%define __os_install_post /usr/lib/rpm/brp-compress

# ------------------------------------------------------------------------------
# We don't package all files installed into the build root by intention -
# See BUG#998 for details.
# ------------------------------------------------------------------------------
%define _unpackaged_files_terminate_build 0

# ------------------------------------------------------------------------------
# RPM build tools now automatically detects Perl module dependencies. This 
# detection gives problems as it is broken in some versions, and it also
# give unwanted dependencies from mandatory scripts in our package.
# Might not be possible to disable in all RPM tool versions, but here we
# try. We keep the "AutoReqProv: no" for the "test" sub package, as disabling
# here might fail, and that package has the most problems.
# See http://fedoraproject.org/wiki/Packaging/Perl#Filtering_Requires:_and_Provides
#     http://www.wideopen.com/archives/rpm-list/2002-October/msg00343.html
# ------------------------------------------------------------------------------
%undefine __perl_provides
%undefine __perl_requires

##############################################################################
# Command line handling
##############################################################################

# ----------------------------------------------------------------------
# use "rpmbuild --with yassl" or "rpm --define '_with_yassl 1'" (for RPM 3.x)
# to build with yaSSL support (off by default)
# ----------------------------------------------------------------------
%{?_with_yassl:%define YASSL_BUILD 1}
%{!?_with_yassl:%define YASSL_BUILD 0}

# ----------------------------------------------------------------------
# use "rpmbuild --without libgcc" or "rpm --define '_without_libgcc 1'" (for RPM 3.x)
# to include libgcc (as libmygcc) (on by default)
# ----------------------------------------------------------------------
%{!?_with_libgcc: %{!?_without_libgcc: %define WITH_LIBGCC 1}}
%{?_with_libgcc:%define WITH_LIBGCC 1}
%{?_without_libgcc:%define WITH_LIBGCC 0}


# On SuSE 9 no separate "debuginfo" package is built. To enable basic
# debugging on that platform, we don't strip binaries on SuSE 9. We
# disable the strip of binaries by redefining the RPM macro
# "__os_install_post" leaving out the script calls that normally does
# this. We do this in all cases, as on platforms where "debuginfo" is
# created, a script "find-debuginfo.sh" will be called that will do
# the strip anyway, part of separating the executable and debug
# information into separate files put into separate packages.
#
# Some references (shows more advanced conditional usage):
# http://www.redhat.com/archives/rpm-list/2001-November/msg00257.html
# http://www.redhat.com/archives/rpm-list/2003-February/msg00275.html
# http://www.redhat.com/archives/rhl-devel-list/2004-January/msg01546.html
# http://lists.opensuse.org/archive/opensuse-commit/2006-May/1171.html

%define __os_install_post /usr/lib/rpm/brp-compress

%define server_suffix  -rel%{majorversion}.%{minorversion}
%define package_suffix -51
%define ndbug_comment Percona Server (GPL), %{majorversion}.%{minorversion}, Revision %{gotrevision}
%define debug_comment Percona Server - Debug (GPL), %{majorversion}.%{minorversion}, Revision %{gotrevision}
%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug

%define BUILD_DEBUG 0

%define lic_type GNU GPL v2
%define lic_files COPYING README
%define src_dir Percona-Server-%{mysqlversion}%{server_suffix}

##############################################################################
# Main spec file section
##############################################################################

Name:		Percona-Server%{package_suffix}
Summary:	Percona-Server: a very fast and reliable SQL database server
Group:		Applications/Databases
Version:	%{mysqlversion}
Release:	%{release}
Distribution:	Red Hat Enterprise Linux %{redhatversion}
License:    GPL	version 2 http://www.gnu.org/licenses/gpl-2.0.html
Source:		Percona-Server-%{mysqlversion}%{server_suffix}.tar.gz
URL:		http://www.percona.com/
Packager:	%{mysql_vendor} Development Team <mysql-dev@percona.com>
Vendor:		%{mysql_vendor}
Provides:	msqlormysql MySQL-server Percona-XtraDB-server
BuildRequires:  gperf perl gcc-c++ ncurses-devel zlib-devel libtool automake autoconf time bison

# Think about what you use here since the first step is to
# run a rm -rf
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

# From the manual
%description
The Percona Server software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. Percona Server
is intended for mission-critical, heavy-load production systems.

Percona recommends that all production deployments be protected with a support
contract (http://www.percona.com/mysql-suppport/) to ensure the highest uptime,
be eligible for hot fixes, and boost your team's productivity.

##############################################################################
# Sub package definition
##############################################################################

%package -n Percona-Server-server%{package_suffix}
Summary:	%{ndbug_comment} for Red Hat Enterprise Linux %{redhatversion}
Group:		Applications/Databases
Requires:	Percona-Server-shared%{package_suffix} Percona-Server-client%{package_suffix} chkconfig coreutils shadow-utils grep procps
Provides:	msqlormysql mysql-server MySQL-server Percona-XtraDB-server
Conflicts:	Percona-SQL-server-50

%description -n Percona-Server-server%{package_suffix}
The Percona Server software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. Percona Server
is intended for mission-critical, heavy-load production systems.

Percona recommends that all production deployments be protected with a support
contract (http://www.percona.com/mysql-suppport/) to ensure the highest uptime,
be eligible for hot fixes, and boost your team's productivity.

This package includes the Percona Server with XtraDB binary 
as well as related utilities to run and administer Percona Server.

If you want to access and work with the database, you have to install
package "Percona-Server-client%{package_suffix}" as well!

# ------------------------------------------------------------------------------

%package -n Percona-Server-client%{package_suffix}
Summary: Percona-Server - Client
Group: Applications/Databases
Provides: mysql-client MySQL-client Percona-XtraDB-client mysql MySQL
Conflicts: Percona-SQL-client-50

%description -n Percona-Server-client%{package_suffix}
This package contains the standard Percona Server client and administration tools. 

%{see_base}


# ------------------------------------------------------------------------------

%package -n Percona-Server-test%{package_suffix}
Requires: mysql-client perl
Summary: Percona-Server - Test suite
Group: Applications/Databases
Provides: mysql-test MySQL-test Percona-XtraDB-test
Conflicts: Percona-SQL-test-50
AutoReqProv: no

%description -n Percona-Server-test%{package_suffix}
This package contains the Percona-Server regression test suite.

%{see_base}

# ------------------------------------------------------------------------------

%package -n Percona-Server-devel%{package_suffix}
Summary: Percona-Server - Development header files and libraries
Group: Applications/Databases
Provides: mysql-devel MySQL-devel Percona-XtraDB-devel
Conflicts: Percona-SQL-devel-50

%description -n Percona-Server-devel%{package_suffix}
This package contains the development header files and libraries
necessary to develop Percona Server client applications.

%{see_base}

# ------------------------------------------------------------------------------

%package -n Percona-Server-shared%{package_suffix}
Summary: Percona-Server - Shared libraries
Group: Applications/Databases
Provides: mysql-shared MySQL-shared Percona-XtraDB-shared mysql-libs
%if "%{redhatversion}" == "6"
Obsoletes: mysql-libs
%endif

%description -n Percona-Server-shared%{package_suffix}
This package contains the shared libraries (*.so*) which certain
languages and applications need to dynamically load and use MySQL.

# ------------------------------------------------------------------------------


##############################################################################
# 
##############################################################################

%prep

%setup -n %{src_dir}


##############################################################################
# The actual build
##############################################################################

%build

BuildMySQL() {
# Get flags from environment. RPM_OPT_FLAGS seems not to be set anywhere.
CFLAGS=${CFLAGS:-$RPM_OPT_FLAGS}
CXXFLAGS=${CXXFLAGS:-$RPM_OPT_FLAGS}
# Evaluate current setting of $DEBUG
if [ $DEBUG -gt 0 ] ; then
	OPT_COMMENT='--with-comment="%{debug_comment}"'
	OPT_DEBUG='--with-debug'
	CFLAGS=`echo   " $CFLAGS "   | \
	    sed -e 's/ -O[0-9]* / /' -e 's/ -unroll2 / /' -e 's/ -ip / /' \
	        -e 's/^ //' -e 's/ $//'`
	CXXFLAGS=`echo " $CXXFLAGS " | \
	    sed -e 's/ -O[0-9]* / /' -e 's/ -unroll2 / /' -e 's/ -ip / /' \
	        -e 's/^ //' -e 's/ $//'`
else
	OPT_COMMENT='--with-comment="%{ndbug_comment}"'
	OPT_DEBUG=''
fi

echo "BUILD =================="
echo $*

MAKE_J=-j`if [ -f /proc/cpuinfo ] ; then grep -c processor.* /proc/cpuinfo ; else echo 1 ; fi`
if [ $MAKE_J = -j0 ]
then
  MAKE_J=-j4
fi

MAKE_JFLAG="${MAKE_JFLAG:-$MAKE_J}"

# The --enable-assembler simply does nothing on systems that does not
# support assembler speedups.
sh -c  "CFLAGS=\"$CFLAGS\" \
	CXXFLAGS=\"$CXXFLAGS\" \
	AM_CPPFLAGS=\"$AM_CPPFLAGS\" \
	LDFLAGS=\"$LDFLAGS\" \
	./configure \
 	    $* \
	    --with-plugins=partition,archive,blackhole,csv,example,federated,innodb_plugin \
	    --enable-assembler \
	    --enable-local-infile \
            --with-mysqld-user=%{mysqld_user} \
            --with-unix-socket-path=/var/lib/mysql/mysql.sock \
	    --with-pic \
            -prefix=/usr \
	    --with-extra-charsets=complex \
	    --with-ssl=/usr \
            --exec-prefix=%{_exec_prefix} \
            --libexecdir=%{_sbindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --localstatedir=%{mysqldatadir} \
            --infodir=%{_infodir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
	    --enable-thread-safe-client \
        --enable-profiling \
%if %{?ndbug_comment:1}0
	    $OPT_COMMENT \
%endif
	    $OPT_DEBUG \
	    --with-readline \
	    ; make $MAKE_JFLAG"
}
# end of function definition "BuildMySQL"

BuildHandlerSocket() {
cd storage/HandlerSocket-Plugin-for-MySQL
./autogen.sh
CXX=${HS_CXX:-g++} ./configure --with-mysql-source=$RPM_BUILD_DIR/%{src_dir} \
	--with-mysql-bindir=$RPM_BUILD_DIR/%{src_dir}/scripts \
	--with-mysql-plugindir=%{_libdir}/mysql/plugin \
	--libdir=%{_libdir} \
	--prefix=%{_prefix}
make $MAKE_JFLAG
cd -
}

BuildUDF() {
cd UDF
CXX=${UDF_CXX:-g++} ./configure --includedir=$RPM_BUILD_DIR/%{src_dir}/include --libdir=%{_libdir}/mysql/plugin
make $MAKE_JFLAG all
cd -
}
# end of function definition "BuildHandlerSocket"

BuildServer() {
BuildMySQL "--enable-shared \
        --with-server-suffix='%{server_suffix}' \
		--without-embedded-server \
		--without-bench \
		--with-zlib-dir=bundled \
		--with-big-tables"

if [ -n "$MYSQL_CONFLOG_DEST" ] ; then
	cp -fp config.log "$MYSQL_CONFLOG_DEST"
fi

#if [ -f sql/.libs/mysqld ] ; then
#	nm --numeric-sort sql/.libs/mysqld > sql/mysqld.sym
#else
#	nm --numeric-sort sql/mysqld > sql/mysqld.sym
#fi
}
# end of function definition "BuildServer"

# For the debuginfo extraction stage, make a link there to avoid errors in the
# strip phase.
for f in lexyy.c pars0grm.c pars0grm.y pars0lex.l
do
    for d in innobase innodb_plugin
    do
        ln -s "pars/$f" "storage/$d/"
    done
done

RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/%{src_dir}

# Move the test suite to /usr/share/mysql
sed -i 's@[$][(]prefix[)]@\0/share@' mysql-test/Makefile.am \
    mysql-test/lib/My/SafeProcess/Makefile.am

# Clean up the BuildRoot first
[ "$RBR" != "/" ] && [ -d $RBR ] && rm -rf $RBR;
mkdir -p $RBR%{_libdir}/mysql $RBR%{_sbindir}

# Use gcc for C and C++ code (to avoid a dependency on libstdc++ and
# including exceptions into the code
if [ -z "$CXX" -a -z "$CC" ] ; then
	export CC="gcc" CXX="gcc"
fi

# Create the shared libs seperately to avoid a dependency for the client utilities
DEBUG=0
BuildMySQL "--enable-shared"

# Install shared libraries
cp -av libmysql/.libs/*.so*   $RBR/%{_libdir}
cp -av libmysql_r/.libs/*.so* $RBR/%{_libdir}

##############################################################################

# Include libgcc.a in the devel subpackage (BUG 4921)
%if %{WITH_LIBGCC}
libgcc=`$CC $CFLAGS --print-libgcc-file`
install -m 644 "$libgcc" $RBR%{_libdir}/mysql/libmygcc.a
%endif

##############################################################################

# Now create a debug server
%if %{BUILD_DEBUG}
DEBUG=1
make clean

( BuildServer )   # subshell, so that CFLAGS + CXXFLAGS are modified only locally

if [ "$MYSQL_RPMBUILD_TEST" != "no" ] ; then
	MTR_BUILD_THREAD=auto make $MAKE_JFLAG %{DEBUG_TEST_MODE}
fi

# Get the debug server and its .sym file from the build tree
#if [ -f sql/.libs/mysqld ] ; then
#	cp sql/.libs/mysqld $RBR%{_sbindir}/mysqld-debug
#else
#	cp sql/mysqld       $RBR%{_sbindir}/mysqld-debug
#fi
#cp libmysqld/libmysqld.a    $RBR%{_libdir}/mysql/libmysqld-debug.a
#cp sql/mysqld.sym           $RBR%{_libdir}/mysql/mysqld-debug.sym

%endif

# Now, the default server
DEBUG=0
make clean

BuildServer
BuildHandlerSocket
BuildUDF
if [ "$MYSQL_RPMBUILD_TEST" != "no" ] ; then
	MTR_BUILD_THREAD=auto make $MAKE_JFLAG %{NORMAL_TEST_MODE}
fi

# Now, build plugin 
#BUILDSO=0
#make clean

#BuildServer

#if [ "$MYSQL_RPMBUILD_TEST" != "no" ] ; then
#	MTR_BUILD_THREAD=auto make %{NORMAL_TEST_MODE}
#fi

# Move temporarily the saved files to the BUILD directory since the BUILDROOT
# dir will be cleaned at the start of the install phase
mkdir -p "$(dirname $RPM_BUILD_DIR/%{_libdir})"
mv $RBR%{_libdir} $RPM_BUILD_DIR/%{_libdir}

%install
RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/%{src_dir}

# Move back the libdir from BUILD dir to BUILDROOT
mkdir -p "$(dirname $RBR%{_libdir})"
mv $RPM_BUILD_DIR/%{_libdir} $RBR%{_libdir}

# Ensure that needed directories exists
install -d $RBR%{_sysconfdir}/{logrotate.d,init.d}
install -d $RBR%{mysqldatadir}/mysql
install -d $RBR%{_datadir}/mysql-test
install -d $RBR%{_datadir}/mysql/SELinux/RHEL4
install -d $RBR%{_includedir}
install -d $RBR%{_libdir}
install -d $RBR%{_mandir}
install -d $RBR%{_sbindir}
install -d $RBR%{_libdir}/mysql/plugin

make DESTDIR=$RBR benchdir_root=%{_datadir} install
cd storage/HandlerSocket-Plugin-for-MySQL
make DESTDIR=$RBR benchdir_root=%{_datadir} install
cd -
cd UDF
make DESTDIR=$RBR benchdir_root=%{_datadir} install
cd -

# install symbol files ( for stack trace resolution)
#install -m644 $MBD/sql/mysqld.sym $RBR%{_libdir}/mysql/mysqld.sym

# Install logrotate and autostart
install -m644 $MBD/support-files/mysql-log-rotate \
        $RBR%{_sysconfdir}/logrotate.d/mysql
install -m755 $MBD/support-files/mysql.server \
        $RBR%{_sysconfdir}/init.d/mysql

# in RPMs, it is unlikely that anybody should use "sql-bench"
rm -fr $RBR%{_datadir}/sql-bench

# Create a symlink "rcmysql", pointing to the init.script. SuSE users
# will appreciate that, as all services usually offer this.
ln -s %{_sysconfdir}/init.d/mysql $RBR%{_sbindir}/rcmysql

# Touch the place where the my.cnf config file and mysqlmanager.passwd
# (MySQL Instance Manager password file) might be located
# Just to make sure it's in the file list and marked as a config file
touch $RBR%{_sysconfdir}/my.cnf
touch $RBR%{_sysconfdir}/mysqlmanager.passwd

# Install SELinux files in datadir
install -m600 $MBD/support-files/RHEL4-SElinux/mysql.{fc,te} \
	$RBR%{_datadir}/mysql/SELinux/RHEL4

##############################################################################
#  Post processing actions, i.e. when installed
##############################################################################

%pre -n Percona-Server-server%{package_suffix}
# Check if we can safely upgrade.  An upgrade is only safe if it's from one
# of our RPMs in the same version family.

installed=`rpm -q --whatprovides mysql-server 2> /dev/null`
if [ $? -eq 0 -a -n "$installed" ]; then
  vendor=`rpm -q --queryformat='%{VENDOR}' "$installed" 2>&1`
  version=`rpm -q --queryformat='%{VERSION}' "$installed" 2>&1`
  myvendor='%{mysql_vendor}'
  myversion='%{mysqlversion}'

  old_family=`echo $version   | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`
  new_family=`echo $myversion | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`

  [ -z "$vendor" ] && vendor='<unknown>'
  [ -z "$old_family" ] && old_family="<unrecognized version $version>"
  [ -z "$new_family" ] && new_family="<bad package specification: version $myversion>"

  error_text=
#  if [ "$vendor" != "$myvendor" ]; then
#    error_text="$error_text
#The current MySQL server package is provided by a different
#vendor ($vendor) than $myvendor.  Some files may be installed
#to different locations, including log files and the service
#startup script in %{_sysconfdir}/init.d/.
#"
#  fi

  if [ "$old_family" != "$new_family" ]; then
    error_text="$error_text
Upgrading directly from MySQL $old_family to MySQL $new_family may not
be safe in all cases.  A manual dump and restore using mysqldump is
recommended.  It is important to review the MySQL manual's Upgrading
section for version-specific incompatibilities.
"
  fi

  if [ -n "$error_text" ]; then
    cat <<HERE >&2

******************************************************************
A MySQL  package ($installed) is installed.
$error_text
A manual upgrade is required.

- Ensure that you have a complete, working backup of your data and my.cnf
  files
- Shut down the MySQL server cleanly
- Remove the existing MySQL packages.  Usually this command will
  list the packages you should remove:
  rpm -qa | grep -i '^mysql-'

  You may choose to use 'rpm --nodeps -ev <package-name>' to remove
  the package which contains the mysqlclient shared library.  The
  library will be reinstalled by the Percona-shared-compat package.
- Install the new Percona Server packages supplied by $myvendor
- Ensure that the Percona Server is started
- Run the 'mysql_upgrade' program

This is a brief description of the upgrade process.  Important details
can be found in the MySQL manual, in the Upgrading section.
For additional details please visit Percona Documentation page
at http://www.percona.com/software/documentation/

******************************************************************
HERE
    exit 1
  fi
fi

# Shut down a previously installed server first
if [ -x %{_sysconfdir}/init.d/mysql ] ; then
	%{_sysconfdir}/init.d/mysql stop > /dev/null 2>&1
	echo "Giving mysqld 5 seconds to exit nicely"
	sleep 5
fi

%post -n Percona-Server-server%{package_suffix}
if [ X${PERCONA_DEBUG} == X1 ]; then
        set -x
fi

# There are users who deviate from the default file system layout.
# Check local settings to support them.
if [ -x %{_bindir}/my_print_defaults ]
then
  mysql_datadir=`%{_bindir}/my_print_defaults server mysqld | grep '^--datadir=' | sed -n 's/--datadir=//p'`
fi
if [ -z "$mysql_datadir" ]
then
  mysql_datadir=%{mysqldatadir}
fi

# ----------------------------------------------------------------------
# Make MySQL start/shutdown automatically when the machine does it.
# ----------------------------------------------------------------------
if [ -x /sbin/chkconfig ] ; then
	/sbin/chkconfig --add mysql
fi
#
# ----------------------------------------------------------------------
# Create a MySQL user and group. Do not report any problems if it already
# exists.
# ----------------------------------------------------------------------
groupadd -r %{mysqld_group} 2> /dev/null || true
useradd -M -r -d $mysql_datadir -s /bin/bash -c "Percona Server" -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true 
# The user may already exist, make sure it has the proper group nevertheless (BUG#12823)
usermod -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true

# ----------------------------------------------------------------------
# Initiate databases
# ----------------------------------------------------------------------
if [ $1 -eq 1 ]; then #clean installation
        mkdir -p $mysql_datadir/{mysql,test}
        %{_bindir}/mysql_install_db --rpm --user=%{mysqld_user}
fi
# ----------------------------------------------------------------------
# FIXME upgrade databases if needed would go here - but it cannot be
# automated yet
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Change permissions again to fix any new files.
# ----------------------------------------------------------------------
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir

# ----------------------------------------------------------------------
# Fix permissions for the permission database so that only the user
# can read them.
# ----------------------------------------------------------------------
chmod -R og-rw $mysql_datadir/mysql

# ----------------------------------------------------------------------
# install SELinux files - but don't override existing ones
# ----------------------------------------------------------------------
SETARGETDIR=/etc/selinux/targeted/src/policy
SEDOMPROG=$SETARGETDIR/domains/program
SECONPROG=$SETARGETDIR/file_contexts/program
if [ -f /etc/redhat-release ] && \
   (grep -q "Red Hat Enterprise Linux .. release 4" /etc/redhat-release \
    || grep -q "CentOS release 4" /etc/redhat-release) ; then
   echo
   echo
   echo 'Notes regarding SELinux on this platform:'
   echo '========================================='
   echo
   echo 'The default policy might cause server startup to fail because it is '
   echo 'not allowed to access critical files. In this case, please update '
   echo 'your installation. '
   echo
   echo 'The default policy might also cause inavailability of SSL related '
   echo 'features because the server is not allowed to access /dev/random '
   echo 'and /dev/urandom. If this is a problem, please do the following: '
   echo 
   echo '  1) install selinux-policy-targeted-sources from your OS vendor'
   echo '  2) add the following two lines to '$SEDOMPROG/mysqld.te':'
   echo '       allow mysqld_t random_device_t:chr_file read;'
   echo '       allow mysqld_t urandom_device_t:chr_file read;'
   echo '  3) cd to '$SETARGETDIR' and issue the following command:'
   echo '       make load'
   echo
   echo
fi

if [ -x sbin/restorecon ] ; then
	sbin/restorecon -R var/lib/mysql
fi

# Restart in the same way that mysqld will be started normally.
if [ -x %{_sysconfdir}/init.d/mysql ] ; then
	%{_sysconfdir}/init.d/mysql start
	echo "Giving mysqld 2 seconds to start"
	sleep 2
fi

echo "Percona Server is distributed with several useful UDF (User Defined Function) from Maatkit."
echo "Run the following commands to create these functions:"
echo "mysql -e \"CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'\""
echo "mysql -e \"CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'\""
echo "mysql -e \"CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'\""
echo "See http://code.google.com/p/maatkit/source/browse/trunk/udf for more details"

# Allow mysqld_safe to start mysqld and print a message before we exit
sleep 2

%preun -n Percona-Server-server%{package_suffix}
if [ $1 = 0 ] ; then
	# Stop MySQL before uninstalling it
	if [ -x %{_sysconfdir}/init.d/mysql ] ; then
		%{_sysconfdir}/init.d/mysql stop > /dev/null
		# Don't start it automatically anymore
		if [ -x /sbin/chkconfig ] ; then
			/sbin/chkconfig --del mysql
		fi
	fi
fi

# We do not remove the mysql user since it may still own a lot of
# database files.

# ----------------------------------------------------------------------
# Clean up the BuildRoot after build is done
# ----------------------------------------------------------------------
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

##############################################################################
#  Files section
##############################################################################

%files -n Percona-Server-server%{package_suffix}
%defattr(-,root,root,0755)

%doc %{lic_files}
%doc support-files/my-*.cnf

%doc %attr(644, root, root) %{_infodir}/mysql.info*
%doc %attr(644, root, man) %{_mandir}/man1/innochecksum.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisam_ftdump.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisamchk.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisamlog.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisampack.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_convert_table_format.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_fix_extensions.1*
%doc %attr(644, root, man) %{_mandir}/man8/mysqld.8*
%doc %attr(644, root, man) %{_mandir}/man1/mysqld_multi.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqld_safe.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_fix_privilege_tables.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_install_db.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_secure_installation.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_setpermission.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_upgrade.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlhotcopy.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlman.1*
%doc %attr(644, root, man) %{_mandir}/man8/mysqlmanager.8*
%doc %attr(644, root, man) %{_mandir}/man1/mysql.server.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqltest.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_tzinfo_to_sql.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_zap.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlbug.1*
%doc %attr(644, root, man) %{_mandir}/man1/perror.1*
%doc %attr(644, root, man) %{_mandir}/man1/replace.1*
%doc %attr(644, root, man) %{_mandir}/man1/resolve_stack_dump.1*
%doc %attr(644, root, man) %{_mandir}/man1/resolveip.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqldumpslow.1*

%ghost %config(noreplace,missingok) %{_sysconfdir}/my.cnf
%ghost %config(noreplace,missingok) %{_sysconfdir}/mysqlmanager.passwd

%attr(755, root, root) %{_bindir}/innochecksum
%attr(755, root, root) %{_bindir}/myisam_ftdump
%attr(755, root, root) %{_bindir}/myisamchk
%attr(755, root, root) %{_bindir}/myisamlog
%attr(755, root, root) %{_bindir}/myisampack
%attr(755, root, root) %{_bindir}/mysql_convert_table_format
%attr(755, root, root) %{_bindir}/mysql_fix_extensions
%attr(755, root, root) %{_bindir}/mysql_fix_privilege_tables
%attr(755, root, root) %{_bindir}/mysql_install_db
%attr(755, root, root) %{_bindir}/mysql_secure_installation
%attr(755, root, root) %{_bindir}/mysql_setpermission
%attr(755, root, root) %{_bindir}/mysql_tzinfo_to_sql
%attr(755, root, root) %{_bindir}/mysql_upgrade
%attr(755, root, root) %{_bindir}/mysql_zap
%attr(755, root, root) %{_bindir}/mysqlbug
%attr(755, root, root) %{_bindir}/mysqld_multi
%attr(755, root, root) %{_bindir}/mysqld_safe
%attr(755, root, root) %{_bindir}/mysqldumpslow
%attr(755, root, root) %{_bindir}/mysqlhotcopy
%attr(755, root, root) %{_bindir}/mysqltest
%attr(755, root, root) %{_bindir}/perror
%attr(755, root, root) %{_bindir}/replace
%attr(755, root, root) %{_bindir}/resolve_stack_dump
%attr(755, root, root) %{_bindir}/resolveip

%attr(755, root, root) %{_sbindir}/mysqld
%if %{BUILD_DEBUG}
%attr(755, root, root) %{_sbindir}/mysqld-debug
%endif
%attr(755, root, root) %{_sbindir}/mysqlmanager
%attr(755, root, root) %{_sbindir}/rcmysql
#%attr(644, root, root) %{_libdir}/mysql/mysqld.sym
%if %{BUILD_DEBUG}
#%attr(644, root, root) %{_libdir}/mysql/mysqld-debug.sym
%endif

%attr(644, root, root) %config(noreplace,missingok) %{_sysconfdir}/logrotate.d/mysql
%attr(755, root, root) %{_sysconfdir}/init.d/mysql

%attr(755, root, root) %{_datadir}/mysql/

%attr(644, root, root) %{_libdir}/mysql/plugin/*

%files -n Percona-Server-client%{package_suffix}
%defattr(-, root, root, 0755)
%attr(755, root, root) %{_bindir}/msql2mysql
%attr(755, root, root) %{_bindir}/mysql
%attr(755, root, root) %{_bindir}/my_print_defaults
%attr(755, root, root) %{_bindir}/mysql_find_rows
%attr(755, root, root) %{_bindir}/mysql_waitpid
%attr(755, root, root) %{_bindir}/mysqlaccess
%attr(755, root, root) %{_bindir}/mysqladmin
%attr(755, root, root) %{_bindir}/mysqlbinlog
%attr(755, root, root) %{_bindir}/mysqlcheck
%attr(755, root, root) %{_bindir}/mysqldump
%attr(755, root, root) %{_bindir}/mysqlimport
%attr(755, root, root) %{_bindir}/mysqlshow
%attr(755, root, root) %{_bindir}/mysqlslap
%attr(755, root, root) %{_bindir}/hsclient

%doc %attr(644, root, man) %{_mandir}/man1/msql2mysql.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql.1*
%doc %attr(644, root, man) %{_mandir}/man1/my_print_defaults.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_find_rows.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_waitpid.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlaccess.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqladmin.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlbinlog.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlcheck.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqldump.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlimport.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlshow.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlslap.1*

%post -n Percona-Server-shared%{package_suffix}
/sbin/ldconfig

%postun -n Percona-Server-shared%{package_suffix}
/sbin/ldconfig


%files -n Percona-Server-devel%{package_suffix}
%defattr(-, root, root, 0755)
%doc %attr(644, root, man) %{_mandir}/man1/comp_err.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_config.1*
%attr(755, root, root) %{_bindir}/mysql_config
%dir %attr(755, root, root) %{_libdir}/mysql
%{_includedir}/mysql
%{_includedir}/handlersocket
%{_datadir}/aclocal/mysql.m4
%{_libdir}/mysql/libdbug.a
%{_libdir}/mysql/libheap.a
%if %{WITH_LIBGCC}
%{_libdir}/mysql/libmygcc.a
%endif
%{_libdir}/mysql/libmyisam.a
%{_libdir}/mysql/libmyisammrg.a
%{_libdir}/mysql/libmysqlclient.a
%{_libdir}/mysql/libmysqlclient.la
%{_libdir}/mysql/libmysqlclient_r.a
%{_libdir}/mysql/libmysqlclient_r.la
%{_libdir}/mysql/libmystrings.a
%{_libdir}/mysql/libmysys.a
%{_libdir}/mysql/libvio.a
%{_libdir}/mysql/libz.a
%{_libdir}/mysql/libz.la
%{_libdir}/libhsclient.a
%{_libdir}/libhsclient.la

%{_libdir}/*.so
%{_libdir}/mysql/*.so

%files -n Percona-Server-shared%{package_suffix}
%defattr(-, root, root, 0755)
# Shared libraries (omit for architectures that don't support them)
%{_libdir}/*.so.*
%{_libdir}/mysql/*.so.*

%files -n Percona-Server-test%{package_suffix}
%defattr(-, root, root, 0755)
/usr/share/mysql-test/*
%attr(755, root, root) %{_bindir}/mysql_client_test
%doc %attr(644, root, man) %{_mandir}/man1/mysql_client_test.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql-stress-test.pl.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql-test-run.pl.1*

##############################################################################
# The spec file changelog only includes changes made to the spec file
# itself - note that they must be ordered by date (important when
# merging BK trees)
##############################################################################
%changelog
* Wed May 22 2010 Aleksandr Kuzminsky <aleksandr.kuzminsky@percona.com>

Percona Server Release 11.0

* Mon Mar 22 2010 Aleksandr Kuzminsky <aleksandr.kuzminsky@percona.com>

XtraDB Release 10

* Thu Feb 11 2010 Aleksandr Kuzminsky <aleksandr.kuzminsky@percona.com>

Package name changed to Percona-XtraDB

* Tue Jan 05 2010 Aleksandr Kuzminsky <aleksandr.kuzminsky@percona.com>

- Corrected emails
- -m64 is removed from CFLAGS

* Tue Apr 21 2009 Aleksandr Kuzminsky <aleksandr.kuzminsky@percona.com>

- Adoption for XtraDB Storage Engine

* Fri Nov 07 2008 Joerg Bruehe <joerg@mysql.com>

- Modify CFLAGS and CXXFLAGS such that a debug build is not optimized.
  This should cover both gcc and icc flags.  Fixes bug#40546.

* Mon Aug 18 2008 Joerg Bruehe <joerg@mysql.com>

- Get rid of the "warning: Installed (but unpackaged) file(s) found:"
  Some generated files aren't needed in RPMs:
  - the "sql-bench/" subdirectory
  Some files were missing:
  - /usr/share/aclocal/mysql.m4  ("devel" subpackage)
  - Manuals for embedded tests   ("test" subpackage)
  - Manual "mysqlbug" ("server" subpackage)
  - Manual "mysql_find_rows" ("client" subpackage)

* Wed Jun 11 2008 Kent Boortz <kent@mysql.com>

- Removed the Example storage engine, it is not to be in products
 
* Fri Apr 04 2008 Daniel Fischer <df@mysql.com>

- Added Cluster+InnoDB product

* Mon Mar 31 2008 Kent Boortz <kent@mysql.com>

- Made the "Federated" storage engine an option

* Tue Mar 11 2008 Joerg Bruehe <joerg@mysql.com>

- Cleanup: Remove manual file "mysql_tableinfo.1".

* Mon Feb 18 2008 Timothy Smith <tim@mysql.com>

- Require a manual upgrade if the alread-installed mysql-server is
  from another vendor, or is of a different major version.

* Fri Dec 14 2007 Joerg Bruehe <joerg@mysql.com>

- Add the "%doc" directive for all man pages and other documentation;
  also, some re-ordering to reduce differences between spec files.

* Fri Dec 14 2007 Joerg Bruehe <joerg@mysql.com>

- Added "client/mysqlslap" (bug#32077)
 
* Wed Oct 31 2007 Joerg Bruehe <joerg@mysql.com>
 
- Explicitly handle InnoDB using its own variable and "--with"/"--without"
  options, because the "configure" default is "yes".
  Also, fix the specification of "community" to include "partitioning".
 
* Mon Sep 03 2007 Kent Boortz <kent@mysql.com>

- Let libmygcc be included unless "--without libgcc" is given.

* Sun Sep 02 2007 Kent Boortz <kent@mysql.com>

- Changed SSL flag given to configure to "--with-ssl"
- Removed symbolic link "safe_mysqld"
- Removed script and man page for "mysql_explain_log"
- Removed scripts "mysql_tableinfo" and "mysql_upgrade_shell"
- Removed "comp_err" from list to install
- Removed duplicates of "libndbclient.a" and "libndbclient.la"

* Tue Jul 17 2007 Joerg Bruehe <joerg@mysql.com>

- Add the man page for "mysql-stress-test.pl" to the "test" RPM
  (consistency in fixing bug#21023, the script is handled by "Makefile.am")

* Wed Jul 11 2007 Daniel Fischer <df@mysql.com>

- Change the way broken SELinux policies on RHEL4 and CentOS 4
  are handled to be more likely to actually work

* Thu Jun 05 2007 kent Boortz <kent@mysql.com>

- Enabled the CSV engine in all builds

* Thu May  3 2007 Mads Martin Joergensen <mmj@mysql.com>

- Spring cleanup

* Thu Apr 19 2007 Mads Martin Joergensen <mmj@mysql.com>

- If sbin/restorecon exists then run it

* Wed Apr 18 2007 Kent Boortz <kent@mysql.com>

- Packed unpacked files

   /usr/sbin/ndb_cpcd
   /usr/bin/mysql_upgrade_shell
   /usr/bin/innochecksum
   /usr/share/man/man1/ndb_cpcd.1.gz
   /usr/share/man/man1/innochecksum.1.gz
   /usr/share/man/man1/mysql_fix_extensions.1.gz
   /usr/share/man/man1/mysql_secure_installation.1.gz
   /usr/share/man/man1/mysql_tableinfo.1.gz
   /usr/share/man/man1/mysql_waitpid.1.gz

- Commands currently not installed but that has man pages

   /usr/share/man/man1/make_win_bin_dist.1.gz
   /usr/share/man/man1/make_win_src_distribution.1.gz
   /usr/share/man/man1/mysql-stress-test.pl.1.gz
   /usr/share/man/man1/ndb_print_backup_file.1.gz
   /usr/share/man/man1/ndb_print_schema_file.1.gz
   /usr/share/man/man1/ndb_print_sys_file.1.gz

* Thu Mar 22 2007 Joerg Bruehe <joerg@mysql.com>

- Add "comment" options to the test runs, for better log analysis.

* Wed Mar 21 2007 Joerg Bruehe <joerg@mysql.com>

- Add even more man pages.

* Fri Mar 16 2007 Joerg Bruehe <joerg@mysql.com>

- Build the server twice, once as "mysqld-debug" and once as "mysqld";
  test them both, and include them in the resulting file.
- Consequences of the fix for bug#20166:
  Remove "mysql_create_system_tables",
  new "mysql_fix_privilege_tables.sql" is included implicitly.

* Wed Mar 14 2007 Daniel Fischer <df@mysql.com>

- Adjust compile options some more and change naming of community
  cluster RPMs to explicitly say 'cluster'.

* Mon Mar 12 2007 Daniel Fischer <df@mysql.com>

- Adjust compile options and other settings for 5.0 community builds.

* Fri Mar 02 2007 Joerg Bruehe <joerg@mysql.com>

- Add several man pages which are now created.

* Mon Jan 29 2007 Mads Martin Joergensen <mmj@mysql.com>

- Make sure SELinux works correctly. Files from Colin Charles.

* Fri Jan 05 2007 Kent Boortz <kent@mysql.com>

- Add CFLAGS to gcc call with --print-libgcc-file, to make sure the
  correct "libgcc.a" path is returned for the 32/64 bit architecture.

* Tue Dec 19 2006 Joerg Bruehe <joerg@mysql.com>

- The man page for "mysqld" is now in section 8.

* Thu Dec 14 2006 Joerg Bruehe <joerg@mysql.com>

- Include the new man pages for "my_print_defaults" and "mysql_tzinfo_to_sql"
  in the server RPM.
- The "mysqlmanager" man page was relocated to section 8, reflect that.

* Fri Nov 17 2006 Mads Martin Joergensen <mmj@mysql.com>

- Really fix obsoletes/provides for community -> this
- Make it possible to not run test by setting
  MYSQL_RPMBUILD_TEST to "no"

* Wed Nov 15 2006 Joerg Bruehe <joerg@mysql.com>

- Switch from "make test*" to explicit calls of the test suite,
  so that "report features" can be used.

* Wed Nov 15 2006 Kent Boortz <kent@mysql.com>

- Added "--with cluster" and "--define cluster{_gpl}"

* Tue Oct 24 2006 Mads Martin Joergensen <mmj@mysql.com>

- Shared need to Provide/Obsolete mysql-shared

* Mon Oct 23 2006 Mads Martin Joergensen <mmj@mysql.com>

- Run sbin/restorecon after db init (Bug#12676)

* Thu Jul 06 2006 Joerg Bruehe <joerg@mysql.com>

- Correct a typing error in my previous change.

* Tue Jul 04 2006 Joerg Bruehe <joerg@mysql.com>

- Use the Perl script to run the tests, because it will automatically check
  whether the server is configured with SSL.

* Wed Jun 28 2006 Joerg Bruehe <joerg@mysql.com>

- Revert all previous attempts to call "mysql_upgrade" during RPM upgrade,
  there are some more aspects which need to be solved before this is possible.
  For now, just ensure the binary "mysql_upgrade" is delivered and installed.

* Wed Jun 28 2006 Joerg Bruehe <joerg@mysql.com>

- Move "mysqldumpslow" from the client RPM to the server RPM (bug#20216).

* Wed Jun 21 2006 Joerg Bruehe <joerg@mysql.com>

- To run "mysql_upgrade", we need a running server;
  start it in isolation and skip password checks.

* Sat May 23 2006 Kent Boortz <kent@mysql.com>

- Always compile for PIC, position independent code.

* Fri Apr 28 2006 Kent Boortz <kent@mysql.com>

- Install and run "mysql_upgrade"

* Sat Apr 01 2006 Kent Boortz <kent@mysql.com>

- Allow to override $LDFLAGS

* Fri Jan 06 2006 Lenz Grimmer <lenz@mysql.com>

- added a MySQL-test subpackage (BUG#16070)

* Tue Dec 27 2005 Joerg Bruehe <joerg@mysql.com>

- Some minor alignment with the 4.1 version

* Wed Dec 14 2005 Rodrigo Novo <rodrigo@mysql.com>

- Cosmetic changes: source code location & rpm packager
- Protect "nm -D" against libtool weirdness
- Add libz.a & libz.la to the list of files for subpackage -devel
- moved --with-zlib-dir=bundled out of BuildMySQL, as it doesn't makes
  sense for the shared package

* Tue Nov 22 2005 Joerg Bruehe <joerg@mysql.com>

- Extend the file existence check for "init.d/mysql" on un-install
  to also guard the call to "insserv"/"chkconfig".

* Wed Nov 16 2005 Lenz Grimmer <lenz@mysql.com>

- added mysql_client_test to the "client" subpackage (BUG#14546)

* Tue Nov 15 2005 Lenz Grimmer <lenz@mysql.com>

- changed default definitions to build a standard GPL release when not
  defining anything else
- install the shared libs more elegantly by using "make install"

* Wed Oct 19 2005 Kent Boortz <kent@mysql.com>

- Made yaSSL support an option (off by default)

* Wed Oct 19 2005 Kent Boortz <kent@mysql.com>

- Enabled yaSSL support

* Thu Oct 13 2005 Lenz Grimmer <lenz@mysql.com>

- added a usermod call to assign a potential existing mysql user to the
  correct user group (BUG#12823)
- added a separate macro "mysqld_group" to be able to define the
  user group of the mysql user seperately, if desired.

* Fri Oct 1 2005 Kent Boortz <kent@mysql.com>

- Copy the config.log file to location outside
  the build tree

* Fri Sep 30 2005 Lenz Grimmer <lenz@mysql.com>

- don't use install-strip to install the binaries (strip segfaults on
  icc-compiled binaries on IA64)

* Thu Sep 22 2005 Lenz Grimmer <lenz@mysql.com>

- allow overriding the CFLAGS (needed for Intel icc compiles)
- replace the CPPFLAGS=-DBIG_TABLES with "--with-big-tables" configure option

* Fri Aug 19 2005 Joerg Bruehe <joerg@mysql.com>

- Protect against failing tests.

* Thu Aug 04 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed the creation of the mysql user group account in the postinstall
  section (BUG 12348)

* Fri Jul 29 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed external RPM Requirements to better suit the target distribution
  (BUG 12233)

* Fri Jul 15 2005 Lenz Grimmer <lenz@mysql.com>

- create a "mysql" user group and assign the mysql user account to that group
  in the server postinstall section. (BUG 10984)

* Wed Jun 01 2005 Lenz Grimmer <lenz@mysql.com>

- use "mysqldatadir" variable instead of hard-coding the path multiple times
- use the "mysqld_user" variable on all occasions a user name is referenced
- removed (incomplete) Brazilian translations
- removed redundant release tags from the subpackage descriptions

* Fri May 27 2005 Lenz Grimmer <lenz@mysql.com>

- fixed file list (removed libnisam.a and libmerge.a from the devel subpackage)
- force running the test suite

* Wed Apr 20 2005 Lenz Grimmer <lenz@mysql.com>

- Enabled the "blackhole" storage engine for the Max RPM

* Wed Apr 13 2005 Lenz Grimmer <lenz@mysql.com>

- removed the MySQL manual files (html/ps/texi) - they have been removed
  from the MySQL sources and are now available seperately.

* Mon Apr 4 2005 Petr Chardin <petr@mysql.com>

- old mysqlmanager, mysqlmanagerc and mysqlmanager-pwger renamed into
  mysqltestmanager, mysqltestmanager and mysqltestmanager-pwgen respectively

* Fri Mar 18 2005 Lenz Grimmer <lenz@mysql.com>

- Disabled RAID in the Max binaries once and for all (it has finally been
  removed from the source tree)

* Sun Feb 20 2005 Petr Chardin <petr@mysql.com>

- Install MySQL Instance Manager together with mysqld, touch mysqlmanager
  password file

* Mon Feb 14 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed the compilation comments and moved them into the separate build sections
  for Max and Standard

* Mon Feb 7 2005 Tomas Ulin <tomas@mysql.com>

- enabled the "Ndbcluster" storage engine for the max binary
- added extra make install in ndb subdir after Max build to get ndb binaries
- added packages for ndbcluster storage engine

* Fri Jan 14 2005 Lenz Grimmer <lenz@mysql.com>

- replaced obsoleted "BuildPrereq" with "BuildRequires" instead

* Thu Jan 13 2005 Lenz Grimmer <lenz@mysql.com>

- enabled the "Federated" storage engine for the max binary

* Tue Jan 04 2005 Petr Chardin <petr@mysql.com>

- ISAM and merge storage engines were purged. As well as appropriate
  tools and manpages (isamchk and isamlog)

* Thu Dec 31 2004 Lenz Grimmer <lenz@mysql.com>

- enabled the "Archive" storage engine for the max binary
- enabled the "CSV" storage engine for the max binary
- enabled the "Example" storage engine for the max binary

* Thu Aug 26 2004 Lenz Grimmer <lenz@mysql.com>

- MySQL-Max now requires MySQL-server instead of MySQL (BUG 3860)

* Fri Aug 20 2004 Lenz Grimmer <lenz@mysql.com>

- do not link statically on IA64/AMD64 as these systems do not have
  a patched glibc installed

* Tue Aug 10 2004 Lenz Grimmer <lenz@mysql.com>

- Added libmygcc.a to the devel subpackage (required to link applications
  against the the embedded server libmysqld.a) (BUG 4921)

* Mon Aug 09 2004 Lenz Grimmer <lenz@mysql.com>

- Added EXCEPTIONS-CLIENT to the "devel" package

* Thu Jul 29 2004 Lenz Grimmer <lenz@mysql.com>

- disabled OpenSSL in the Max binaries again (the RPM packages were the
  only exception to this anyway) (BUG 1043)

* Wed Jun 30 2004 Lenz Grimmer <lenz@mysql.com>

- fixed server postinstall (mysql_install_db was called with the wrong
  parameter)

* Thu Jun 24 2004 Lenz Grimmer <lenz@mysql.com>

- added mysql_tzinfo_to_sql to the server subpackage
- run "make clean" instead of "make distclean"

* Mon Apr 05 2004 Lenz Grimmer <lenz@mysql.com>

- added ncurses-devel to the build prerequisites (BUG 3377)

* Thu Feb 12 2004 Lenz Grimmer <lenz@mysql.com>

- when using gcc, _always_ use CXX=gcc 
- replaced Copyright with License field (Copyright is obsolete)

* Tue Feb 03 2004 Lenz Grimmer <lenz@mysql.com>

- added myisam_ftdump to the Server package

* Tue Jan 13 2004 Lenz Grimmer <lenz@mysql.com>

- link the mysql client against libreadline instead of libedit (BUG 2289)

* Mon Dec 22 2003 Lenz Grimmer <lenz@mysql.com>

- marked /etc/logrotate.d/mysql as a config file (BUG 2156)

* Fri Dec 13 2003 Lenz Grimmer <lenz@mysql.com>

- fixed file permissions (BUG 1672)

* Thu Dec 11 2003 Lenz Grimmer <lenz@mysql.com>

- made testing for gcc3 a bit more robust

* Fri Dec 05 2003 Lenz Grimmer <lenz@mysql.com>

- added missing file mysql_create_system_tables to the server subpackage

* Fri Nov 21 2003 Lenz Grimmer <lenz@mysql.com>

- removed dependency on MySQL-client from the MySQL-devel subpackage
  as it is not really required. (BUG 1610)

* Fri Aug 29 2003 Lenz Grimmer <lenz@mysql.com>

- Fixed BUG 1162 (removed macro names from the changelog)
- Really fixed BUG 998 (disable the checking for installed but
  unpackaged files)

* Tue Aug 05 2003 Lenz Grimmer <lenz@mysql.com>

- Fixed BUG 959 (libmysqld not being compiled properly)
- Fixed BUG 998 (RPM build errors): added missing files to the
  distribution (mysql_fix_extensions, mysql_tableinfo, mysqldumpslow,
  mysql_fix_privilege_tables.1), removed "-n" from install section.

* Wed Jul 09 2003 Lenz Grimmer <lenz@mysql.com>

- removed the GIF Icon (file was not included in the sources anyway)
- removed unused variable shared_lib_version
- do not run automake before building the standard binary
  (should not be necessary)
- add server suffix '-standard' to standard binary (to be in line
  with the binary tarball distributions)
- Use more RPM macros (_exec_prefix, _sbindir, _libdir, _sysconfdir,
  _datadir, _includedir) throughout the spec file.
- allow overriding CC and CXX (required when building with other compilers)

* Fri May 16 2003 Lenz Grimmer <lenz@mysql.com>

- re-enabled RAID again

* Wed Apr 30 2003 Lenz Grimmer <lenz@mysql.com>

- disabled MyISAM RAID (--with-raid) - it throws an assertion which
  needs to be investigated first.

* Mon Mar 10 2003 Lenz Grimmer <lenz@mysql.com>

- added missing file mysql_secure_installation to server subpackage
  (BUG 141)

* Tue Feb 11 2003 Lenz Grimmer <lenz@mysql.com>

- re-added missing pre- and post(un)install scripts to server subpackage
- added config file /etc/my.cnf to the file list (just for completeness)
- make sure to create the datadir with 755 permissions

* Mon Jan 27 2003 Lenz Grimmer <lenz@mysql.com>

- removed unused CC and CXX variables
- CFLAGS and CXXFLAGS should honor RPM_OPT_FLAGS

* Fri Jan 24 2003 Lenz Grimmer <lenz@mysql.com>

- renamed package "MySQL" to "MySQL-server"
- fixed Copyright tag
- added mysql_waitpid to client subpackage (required for mysql-test-run)

* Wed Nov 27 2002 Lenz Grimmer <lenz@mysql.com>

- moved init script from /etc/rc.d/init.d to /etc/init.d (the majority of 
  Linux distributions now support this scheme as proposed by the LSB either
  directly or via a compatibility symlink)
- Use new "restart" init script action instead of starting and stopping
  separately
- Be more flexible in activating the automatic bootup - use insserv (on
  older SuSE versions) or chkconfig (Red Hat, newer SuSE versions and
  others) to create the respective symlinks

* Wed Sep 25 2002 Lenz Grimmer <lenz@mysql.com>

- MySQL-Max now requires MySQL >= 4.0 to avoid version mismatches
  (mixing 3.23 and 4.0 packages)

* Fri Aug 09 2002 Lenz Grimmer <lenz@mysql.com>
 
- Turn off OpenSSL in MySQL-Max for now until it works properly again
- enable RAID for the Max binary instead
- added compatibility link: safe_mysqld -> mysqld_safe to ease the
  transition from 3.23

* Thu Jul 18 2002 Lenz Grimmer <lenz@mysql.com>

- Reworked the build steps a little bit: the Max binary is supposed
  to include OpenSSL, which cannot be linked statically, thus trying
	to statically link against a special glibc is futile anyway
- because of this, it is not required to make yet another build run
  just to compile the shared libs (saves a lot of time)
- updated package description of the Max subpackage
- clean up the BuildRoot directory afterwards

* Mon Jul 15 2002 Lenz Grimmer <lenz@mysql.com>

- Updated Packager information
- Fixed the build options: the regular package is supposed to
  include InnoDB and linked statically, while the Max package
	should include BDB and SSL support

* Fri May 03 2002 Lenz Grimmer <lenz@mysql.com>

- Use more RPM macros (e.g. infodir, mandir) to make the spec
  file more portable
- reorganized the installation of documentation files: let RPM
  take care of this
- reorganized the file list: actually install man pages along
  with the binaries of the respective subpackage
- do not include libmysqld.a in the devel subpackage as well, if we
  have a special "embedded" subpackage
- reworked the package descriptions

* Mon Oct  8 2001 Monty

- Added embedded server as a separate RPM

* Fri Apr 13 2001 Monty

- Added mysqld-max to the distribution

* Tue Jan 2  2001  Monty

- Added mysql-test to the bench package

* Fri Aug 18 2000 Tim Smith <tim@mysql.com>

- Added separate libmysql_r directory; now both a threaded
  and non-threaded library is shipped.

* Wed Sep 28 1999 David Axmark <davida@mysql.com>

- Added the support-files/my-example.cnf to the docs directory.

- Removed devel dependency on base since it is about client
  development.

* Wed Sep 8 1999 David Axmark <davida@mysql.com>

- Cleaned up some for 3.23.

* Thu Jul 1 1999 David Axmark <davida@mysql.com>

- Added support for shared libraries in a separate sub
  package. Original fix by David Fox (dsfox@cogsci.ucsd.edu)

- The --enable-assembler switch is now automatically disables on
  platforms there assembler code is unavailable. This should allow
  building this RPM on non i386 systems.

* Mon Feb 22 1999 David Axmark <david@detron.se>

- Removed unportable cc switches from the spec file. The defaults can
  now be overridden with environment variables. This feature is used
  to compile the official RPM with optimal (but compiler version
  specific) switches.

- Removed the repetitive description parts for the sub rpms. Maybe add
  again if RPM gets a multiline macro capability.

- Added support for a pt_BR translation. Translation contributed by
  Jorge Godoy <jorge@bestway.com.br>.

* Wed Nov 4 1998 David Axmark <david@detron.se>

- A lot of changes in all the rpm and install scripts. This may even
  be a working RPM :-)

* Sun Aug 16 1998 David Axmark <david@detron.se>

- A developers changelog for MySQL is available in the source RPM. And
  there is a history of major user visible changed in the Reference
  Manual.  Only RPM specific changes will be documented here.
