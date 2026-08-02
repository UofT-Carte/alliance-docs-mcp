---
title: "CephFS/en"
url: "https://docs.alliancecan.ca/wiki/CephFS/en"
category: "General"
last_modified: "2026-07-20T15:06:14Z"
page_id: 20857
display_title: "CephFS"
---

CephFS provides a common filesystem that can be shared amongst multiple OpenStack VM hosts. Access to the service is granted via requests to cloud@tech.alliancecan.ca.

This is a fairly technical procedure that assumes basic Linux skills for creating/editing files, setting permissions, and creating mount points. For assistance in setting up this service, write to cloud@tech.alliancecan.ca.

=Procedure=

==Request access to shares ==

If you do not already have a quota for the service, you will need to request this through cloud@tech.alliancecan.ca. In your request please provide the following:
* OpenStack project name
* amount of quota required (in GB)
* number of shares required

== OpenStack configuration: Create a CephFS share ==

; Create the share.
: In Project --> Share --> Shares, click on +Create Share.
: Share Name = enter a name that identifies your project (e.g. project-name-shareName)
: Share Protocol = CephFS
: Size = size you need for this share
: Share Type = cephfs (or cephfs-ec42 on SD4H/Juno)
: Availability Zone = nova
: Do not check Make visible for all (or Make visible to users from all projects on SD4H/Juno), otherwise the share will be accessible by all users in all projects.
: Click on the Create button.

; Create an access rule to generate access key.
: In Project --> Share --> Shares --> Actions column, select Manage Rules from the drop-down menu.
: Click on the +Add Rule button (right of the page).
: Access Type = cephx
: Access Level = select read-write or read-only (you can create multiple rules for either access level if required)
: Access To = select a key name that describes the key. This name is important because it will be used in the cephfs client configuration on the VM; on this page, we use MyCephFS-RW.

; Note the share details which you will need later.
: In Project --> Share --> Shares, click on the name of the share.
: In the Share Overview, note the three elements circled in red in the image above: Path, which will be used in the  mount command on the VM; the Access to, which will be the client name; and the Access Key that will let the VM's client connect.

== Attach the CephFS network to your VM ==

=== On Arbutus ===
On Arbutus, the cephFS network is already exposed to your VM; there is nothing to do here, go to the VM configuration section.

=== On SD4H/Juno ===
On SD4H/Juno, you need to explicitly attach the cephFS network to the VM.

;With the Web Gui
For each VM you need to attach, select Instance --> Action --> Attach interface  select the CephFS-Network, leave the Fixed IP Address box empty.

;With the Openstack client
List the servers and select the id of the server you need to attach to the CephFS

$ openstack  server list
+--------------------------------------+--------------+--------+-------------------------------------------+--------------------------+----------+
| ID                                   | Name         | Status | Networks                                  | Image                    | Flavor   |
+--------------------------------------+--------------+--------+-------------------------------------------+--------------------------+----------+
| 1b2a3c21-c1b4-42b8-9016-d96fc8406e04 | prune-dtn1   | ACTIVE | test_network=172.16.1.86, 198.168.189.3   | N/A (booted from volume) | ha4-15gb |
| 0c6df8ea-9d6a-43a9-8f8b-85eb64ca882b | prune-mgmt1  | ACTIVE | test_network=172.16.1.64                  | N/A (booted from volume) | ha4-15gb |
| 2b7ebdfa-ee58-4919-bd12-647a382ec9f6 | prune-login1 | ACTIVE | test_network=172.16.1.111, 198.168.189.82 | N/A (booted from volume) | ha4-15gb |
+--------------------------------------+--------------+--------+----------------------------------------------+--------------------------+----------+

Select the ID of the VM you want to attach, will pick the first one here and run

$ openstack  server add network 1b2a3c21-c1b4-42b8-9016-d96fc8406e04 CephFS-Network
$ openstack  server list
+--------------------------------------+--------------+--------+---------------------------------------------------------------------+--------------------------+----------+
| ID                                   | Name         | Status | Networks                                                            | Image                    | Flavor   |
+--------------------------------------+--------------+--------+---------------------------------------------------------------------+--------------------------+----------+
| 1b2a3c21-c1b4-42b8-9016-d96fc8406e04 | prune-dtn1   | ACTIVE | CephFS-Network=10.65.20.71; test_network=172.16.1.86, 198.168.189.3 | N/A (booted from volume) | ha4-15gb |
| 0c6df8ea-9d6a-43a9-8f8b-85eb64ca882b | prune-mgmt1  | ACTIVE | test_network=172.16.1.64                                            | N/A (booted from volume) | ha4-15gb |
| 2b7ebdfa-ee58-4919-bd12-647a382ec9f6 | prune-login1 | ACTIVE | test_network=172.16.1.111, 198.168.189.82                           | N/A (booted from volume) | ha4-15gb |
+--------------------------------------+--------------+--------+------------------------------------------------------------------------+--------------------------+----------+

We can see that the CephFS network is attached to the first VM.

== VM configuration: install and configure CephFS client ==

=== Required packages for the Red Hat Enterprise Linux family (RHEL, CentOS, Fedora, Rocky, Alma ) ===
Check the available releases at https://download.ceph.com/ and look for recent rpm-* directories.
As of June 2026, tentacle is the latest stable release.
The compatible distributions (distros) are listed at https://download.ceph.com/rpm-tentacle/.

==== Add the Ceph software repository ====
Depending on the version of Enterprise Linux you are running, add the follwowing file:

==== Install relevant repositories for access to ceph client packages ====
Install the Extra Packages for Enterprise Linux (EPEL) repository:
 sudo dnf install epel-release

If you are running el10 you need to temporarily disable the default cryptographic policy due to how the Ceph packages are signed:
 sudo update-crypto-policies --set LEGACY

Import the Ceph project's public key needed to verify the cryptographic signatures on the software packages:
  sudo rpm --import 'https://download.ceph.com/keys/release.asc'

You can now install the ceph lib, cephfs client and other dependencies:
 sudo dnf install -y libcephfs2 python3-cephfs ceph-common python3-ceph-argparse

If you disabled the default cryptographic policy, you should restore the default cryptographic policy
  sudo update-crypto-policies --set DEFAULT

=== Required packages for the Debian family (Debian, Ubuntu, Mint, etc.) ===
You can get the repository once you have figured out your distro {codename} with lsb_release -sc

sudo apt-add-repository 'deb https://download.ceph.com/debian-tentacle/ {codename} main'

If the previous command gave an error, revert it with the following command and go to the next step:

sudo add-apt-repository -r 'deb https://download.ceph.com/debian-tentacle/ {codename} main'

You can now install the ceph lib, cephfs client and other dependencies:

 sudo apt-get install -y libcephfs2 python3-cephfs ceph-common python3-ceph-argparse

=== Configure ceph client ===

Once the client is installed, you can create a ceph.conf file.
Note the different mon host for the different cloud.

You can find the monitor information in the share details Path field that will be used to mount the volume. If the value of the web page is different than what is seen here, it means that the wiki page is out of date.

You also need to put your client name and secret in the ceph.keyring file

Again, the access key and client name (here MyCephFS-RW) are found under the access rules on your project web page.
Look for Project --> Share --> Shares, then click on the name of the share.

; Retrieve the connection information from the share page for your connection:
: Open up the share details by clicking on the name of the share in the Shares page.
: Copy the portion of the Path of the share that starts with : which we will use to mount the filesystem (for example :/volumes/_nogroup/f6cb8f06-f0a4-4b88-b261-f8bd6b03582c, is used here).

;Mount the filesystem
:Create a mount point directory somewhere in your host (/cephfs, is used here)

 mkdir /cephfs

:You can use the ceph driver to permanently mount your CephFS device by adding the following in the VM fstab

Notice the non-standard : before the device path. It is not a typo!
The mount options are different on different systems.
The namespace option is required for SD4H/Juno, while other options are performance tweaks.  The nofail option ensures that the system will boot even in the unlikely case that the CephFS service is down or unreachable.

You can also do the mount directly from the command line:

sudo mount -t ceph :/volumes/_nogroup/f6cb8f06-f0a4-4b88-b261-f8bd6b03582c /cephfs/ -o name=MyCephFS-RW

sudo mount -t ceph :/volumes/_nogroup/f6cb8f06-f0a4-4b88-b261-f8bd6b03582c /cephfs/ -o name=MyCephFS-RW,mds_namespace=cephfs_4_2,x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw

CephFS can also be mounted directly in user space via ceph-fuse.

Install the ceph-fuse lib

sudo dnf install ceph-fuse

Let the fuse mount be accessible in userspace by uncommenting  user_allow_other in the fuse.conf file.

You can now mount cephFS in a user’s home:

mkdir ~/my_cephfs
ceph-fuse my_cephfs/ --id=MyCephFS-RW --conf=~/ceph.conf --keyring=~/ceph.keyring   --client-mountpoint=/volumes/_nogroup/f6cb8f06-f0a4-4b88-b261-f8bd6b03582c

Note that the client name is here the --id. The ceph.conf and ceph.keyring content are exactly the same as for the ceph kernel mount.

=Notes=

A particular share can have more than one user key provisioned for it. This allows a more granular access to the filesystem, for example, if you needed some hosts to only access the filesystem in a read-only capacity. If you have multiple keys for a share, you can add the extra keys to your host and modify the above mounting procedure. This service is not available to hosts outside of the OpenStack cluster.