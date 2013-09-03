.. _yum-repo:

===========================================
 Percona :program:`yum` Repository
===========================================

The |Percona| :program:`yum` repository supports popular *RPM*-based operating systems, including the *Amazon Linux AMI*.

The easiest way to install the *Percona Yum* repository is to install an *RPM* that configures :program:`yum` and installs the `Percona GPG key <https://www.percona.com/downloads/RPM-GPG-KEY-percona>`_. Installation can also be done manually.

Automatic Installation
=======================

Execute the following command as a ``root`` user, replacing ``x86_64`` with ``i386`` if you are not running a 64-bit operating system: ::

  $ rpm -Uhv http://www.percona.com/downloads/percona-release/percona-release-0.0-1.x86_64.rpm

The RPMs for the automatic installation are available at http://www.percona.com/downloads/percona-release/ and include source code.

You should see some output such as the following: ::

  Retrieving http://www.percona.com/downloads/percona-release/percona-release-0.0-1.x86_64.rpm
  Preparing...                ########################################### [100%]
     1:percona-release        ########################################### [100%]

The RPMs for the automatic installation are available at http://www.percona.com/downloads/percona-release/ and include source code.

Install XtraDB Cluster
=======================

Following command will install Cluster packages: ::

  $ yum install Percona-XtraDB-Cluster-server Percona-XtraDB-Cluster-client xtrabackup

Percona `yum` Experimental repository
=====================================

Percona offers fresh beta builds from the experimental repository. To subscribe to the experimental repository, install the experimental *RPM*: ::

  rpm -Uhv http://repo.percona.com/testing/centos/6/os/noarch/percona-testing-0.0-1.noarch.rpm

.. note:: 
 This repository works for both RHEL/CentOS 5 and RHEL/CentOS 6