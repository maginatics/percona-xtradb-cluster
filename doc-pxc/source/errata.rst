.. _Errata:

====================================
 Percona XtraDB Cluster Errata (as of 5.5.34)
====================================

Known Issues
-------------

Following are issues which may impact you while running PXC:
 - wsrep_causal_reads being ON can introduce temporary stalls due to MDL lock conflicts.
 - bug :bug:`1226185`: percona-xtrabackup-20 may get installed as a dependency instead of latest percona-xtrabackup during a fresh install due to certain yum issues. Workaround is documented here - https://bugs.launchpad.net/percona-xtradb-cluster/+bug/1226185/comments/2.
 - bug :bug:`1192834`: Joiner may crash after SST from donor with compaction enabled. Workaround is to disable the index compaction (compact under [xtrabackup]), if enabled. This crash requires specific configuration, hence you may not be affected. Also, this doesn't require any fix from PXC, but Xtrabackup with the fix included should do.
 - bug :bug:`1217426`: When empty test directory is present on donor, it is not created on joiner, so when tables are created after SST on donor, the joiner later on will fail with inconsistency. Workaround is to either drop the test database or populate it with a table before SST. This is currently a limitation of Xtrabackup itself, hence, needs to be fixed there.
 - bug :bug:`1098566`: :variable:`innodb_data_home_dir` is not supported. Depends on bug :bug:`1164945` for the fix.
 - For Debian/Ubuntu users: |Percona XtraDB Cluster| :rn:`5.5.33-23.7.6` onwards has a new dependency, the ``socat`` package. If the ``socat`` is not previously installed, ``percona-xtradb-cluster-server-5.5`` may be held back. In order to upgrade, you need to either install ``socat`` before running the ``apt-get upgrade`` or with the following command: ``apt-get install percona-xtradb-cluster-server-5.5``. For *Ubuntu* users the ``socat`` package is in the universe repository, so the repository will have to be enabled in order to install the package.


Also make sure to check limitations page :ref:`here <limitations>`. You can also review this `milestone <https://launchpad.net/percona-xtradb-cluster/+milestone/future-5.5>`_ for features/bugfixes to be included in future releases (ie. releases after the upcoming/recent release).

Major changes
--------------- 

 - An earlier incompatibility introduced in PXC 5.5.33 has been fixed. The newer xtrabackup SST is added as wsrep_sst_xtrabackup-v2 and can be enabled ``wsrep_sst_method=xtrabackup-v2``. wsrep_sst_xtrabackup-v2 is not compatible with wsrep_sst_xtrabackup. The default is xtrabackup (for compatibility reasons). Since, newer features are added only to xtrabackup-v2, it is recommended to use xtrabackup-v2 (to use new features) and use xtrabackup only when older nodes are present. Also note that, it is required to set wsrep_sst_method only on joiner, the donor is informed by galera about this on the other end. Also, note that, xtrabackup (not -v2) supports all the major options `here <http://www.percona.com/doc/percona-xtradb-cluster/manual/xtrabackup_sst.html>`_, any changes will be otherwise noted along with the option.

Incompatibilities
-------------------

Following are incompatibilities between PXC 5.5.33 (and higher) and older versions:
 - wsrep_sst_donor now supports comma separated list of nodes as a consequence of bug :bug:`1129512`. This only affects if you use this option as a list. This is not compatible with nodes running older PXC, hence **entire** cluster will be affected as far as SST is concerned, since donor nodes won't recognise the request from joiner nodes if former are not upgraded. Minimal workaround is to upgrade Galera package or to not use this new feature (wsrep_sst_donor with single node can still be used). However, upgrading the full PXC is strongly recommended, however, just upgrading PXC galera package will do for this.
