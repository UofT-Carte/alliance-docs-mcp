---
title: "Arbutus Migration Guide/en"
url: "https://docs.alliancecan.ca/wiki/Arbutus_Migration_Guide/en"
category: "User Guide"
last_modified: "2026-06-23T14:17:29Z"
page_id: 9289
display_title: "Arbutus Migration Guide"
---

This document describes how to migrate virtual machine (VM) instances from the legacy (that is, old) Arbutus Cloud to the new Arbutus Cloud. Because you know your workload best, we recommend that you migrate your instances yourself, according to your own application requirements and schedule.

Migration is necessary for all cloud resources (e.g., instances, storage volumes, object storage containers, networks, keys, etc.) currently on the legacy Arbutus Cloud because it will be decommissioned in 2026. The deadline for both RAS and RAC projects to migrate to the new Arbutus Cloud is August 31, 2026.

This document explains different migration methods. You and your research team need to select the approach(es) appropriate for your research project and specific circumstances.

Once you have read this document, you may have questions or you may wish to review your migration plan with an Arbutus Cloud team member. If so, please write to cloud@tech.alliancecan.ca.

= Planning your cloud migration =

To plan your migration, you should be able to answer the following questions about the resources you currently have on the legacy Arbutus Cloud:

* Which resources need migration? Not all resources have to be migrated. For example, if a volume or an instance is no longer needed, it could be deleted instead. Create a list of all resources which require migration.
* Are your instances ephemeral or volume-backed? Volume-backed instances boot from a volume (i.e., /dev/vda) and can have other volumes (e.g., /dev/vdb, etc.) attached. Ephemeral instances do not boot from a volume. Identify the instances that are volume-backed and those that are ephemeral.
* Are your volumes under 150 GB? Identify volumes over 150 GB because they should be migrated using Globus.
* Have you used an automated deployment system (e.g., Terraform, Ansible) on the legacy Arbutus Cloud? If so, the same automation tools should be used for the migration.
* Do you have custom DNS entries? If so, they will need to be updated because the new Arbutus Cloud uses different floating IP address ranges.
* Do you use the OpenStack dashboard or the OpenStack Command Line Interface (CLI) to manage your Arbutus Cloud resources? Simple migrations can be done via the Web user interface, but complex migrations may require CLI access.
* Do all users who need access have an active account with the Alliance? Remember that account sharing is strictly forbidden. Any person who requires an account should apply on CCDB.
* Depending on the scope of the migration, an outage of a couple of hours to a couple of days may occur. How will you manage this outage? Who needs to be informed?
* If your resources were obtained via the rapid access service, you must submit a migration request to cloud@tech.alliancecan.ca.

Once you have answered these questions, you will be ready to plan your cloud migration.

= Basic information =
To access the OpenStack dashboard, URLs are

Legacy Arbutus Cloud: https://arbutus.cloud.computecanada.ca

New Arbutus Cloud: https://arbutus.alliancecan.ca/

Firefox and Chrome browsers are supported. Safari and Edge may work, but they have not been tested.

Your Arbutus Cloud project (tenant), network, and router will be pre-created for you in the new Arbutus Cloud. You will have access to the same projects as you had on the legacy Arbutus Cloud. However, since  the new Arbutus Cloud has a different floating IP range, new security groups (OpenStack’s firewall rules) may be required.

= Preparing the migration environment =

IMPORTANT: Before you begin, back up any critical data. While the Arbutus Cloud has redundant storage systems, no backups or copies of instances are made by our teams. Project owners are responsible for creating backups which may be necessary for the migration.
# Use your account credentials to log into the URLs for both clouds and download the RC files under Project -> API Access -> Download OpenStack RC File. These files are to set environment variables used by the OpenStack command-line tools.
# Copy the OpenStack RC files to the host you will be using for the migration and follow the instructions in Changing the RC file in the new Arbutus cloud below.
# Test the RC file(s) to confirm you can access your projects in both clouds:
## Activate an RC file by sourcing it (source opensrc.sh) in a shell session. Only one RC file can be active in a given shell session at a time.
## Test your configuration by running openstack volume list).
# Migrate SSH keys:
## From the legacy Arbutus Horizon dashboard, navigate to Compute -> Key Pairs. Click on the name of the key pair you want and copy the public key value.
## From the new Arbutus Horizon dashboard, navigate to Compute -> Key Pairs. Click on Import Public Key, name your key pair and paste it in the public key for the legacy Arbutus Cloud.
## Your key pair should now be imported into the new Arbutus Cloud. Repeat the above steps for as many keys as you need.
## You can also generate new key pairs or import them with openstack keypair create --public-key  .
# Migrate security groups and rules:
## On the legacy Arbutus Cloud, go to Network -> Security Groups; note the existing security groups and their associated rules.
## On the new Arbutus Cloud, go to Network -> Security Groups; re-create the security groups and their associated rules as needed.
## Do not delete any of the Egress security rules for IPv4 and IPv6 created by default. Deleting these rules can cause your instances to fail to retrieve configuration data from the OpenStack metadata service, along with a host of other issues.
## Security groups and rules can also be created via the CLI as follows. This example is for HTTP port 80 only; modify it according to your requirements. openstack security group create  openstack security group rule create --proto tcp --remote-ip 0.0.0.0/0 --dst-port 80
## To view rules via the CLI,
##* run openstack security group list to list the available security groups.
##* run openstack security group rule list to view the rules for the group.
# Plan an outage window. Generally, shutting down services and then shutting down the instance is the best way to avoid corrupt or inconsistent data after the migration. Smaller volumes can be copied over fairly quickly; e.g., a 10GB volume will copy over in less than 5 minutes, but larger volumes (e.g., 100GB) can take 30 to 40 minutes. Plan for this. Additionally, floating IP addresses will change, so ensure the TTL of your DNS records is set to a small value so that the changes propagate as quickly as possible.

= Changing the RC file in the new Arbutus cloud =
After downloading a new RC file from the new Arbutus cloud, you have to modify the file by adding the following lines:

export OS_AUTH_TYPE=v3websso
export OS_IDENTITY_PROVIDER=atmosphere
export OS_PROTOCOL=openid
export OS_PROJECT_DOMAIN_NAME=default

Also, remove the lines containing

export OS_USER_DOMAIN_NAME="atmosphere"
if [ -z "$OS_USER_DOMAIN_NAME" ]; then unset OS_USER_DOMAIN_NAME; fi

and remove

echo "Please enter your OpenStack Password for project $OS_PROJECT_NAME as user $OS_USERNAME: "
read -sr OS_PASSWORD_INPUT
export OS_PASSWORD=$OS_PASSWORD_INPUT

The final RC file should contain lines that look like these:

export OS_AUTH_URL=https://identity.arbutus.alliancecan.ca/
export OS_PROJECT_ID=xIDx
export OS_PROJECT_NAME=" xIDx "
export OS_PROJECT_DOMAIN_ID=" xIDx "
unset OS_TENANT_ID
unset OS_TENANT_NAME
export OS_USERNAME=" xIDx "
export OS_REGION_NAME="RegionOne"
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_TYPE=v3websso
export OS_IDENTITY_PROVIDER=atmosphere
export OS_PROTOCOL=openid
export OS_PROJECT_DOMAIN_NAME=default

Now, create a virtual environment to install the OpenStack Client and other necessary packages.

$ python3 -m venv openstack
$ source openstack/bin/activate
$ pip install python-openstackclient  keystoneauth-websso python-manilaclient

= Migration scenarios =
There are three general migration scenarios to consider.
* Manual or orchestrated migration
* Migrating volume-backed instances
* Migrating ephemeral instances
Depending on your current setup, you may use any or all of these scenarios.

== Manual or orchestrated migration ==

In this scenario, new instances and volumes are created in the new Arbutus Cloud with the same specifications as those of the legacy Arbutus Cloud. Necessary files and data are copied over from the old instances and volumes. The general approach is:

# If you are using customized images, copy the Glance images from the legacy cloud to the new cloud. You may also simply start with a fresh base image in the new cloud.
# Install and configure services on the instance (or instances).
# Copy data from the old instances to the new instances; see methods to copy data below.
# Assign floating IP addresses to the new instances and update DNS.
# Decommission the old instances and delete old volumes.

These steps can be done manually or orchestrated via various configuration management tools such as Ansible, Terraform, or Heat. The use of such tools is beyond the scope of this document, but if you were already using orchestration tools on the legacy Arbutus cloud, they should work with the new cloud as well.

== Migrating volume-backed instances ==

Volume-backed instances, as their name implies, have a persistent volume attached to them containing the operating system and any required data. Best practice is to use separate volumes for the operating system and for data.

=== Migration using Glance images ===

This method is recommended for volumes less than 150GB in size. For volumes larger than that, the approach described in Manual or orchestrated migration above is preferred.

# Open two SSH sessions to the volume-backed instance you plan to migrate.
# In one session, source the OpenStack RC file for the legacy cloud. In the other session, source the OpenStack RC file for the new cloud. Use of the screen command is recommended in case of SSH disconnections. To install the screen package, run dnf install screen
# On the legacy cloud instance, install the OpenStack CLI in a root shell:

dnf install epel-release
dnf install python-devel python-pip gcc
pip install python-openstackclient

#  In the legacy cloud web user interface, shut down the instance and detach the volume.If the volume is for booting an instance, delete the instance, but keep the volume.Create an image of the desired volume (Volumes -> Volumes and Upload to Image from the drop-down menu).Make sure to select RAW as the disk format.
#  The command line can also be used to do this:
openstack image create --volume   --privateThis command runs in the background and may take some time. Once the image is created, it will show up under Compute -> Images with the name you specified in the previous step. You can obtain the id of the image by clicking on its name. Eventually the command line will show the status go from saving to active; this may take an hour or longer, depending on the size of your volume.
openstack image show
#  In the legacy cloud session, download the image (replace the  and  with real values).
openstack image save --file
#  In the new cloud session on the migration host, upload the image (replace  with the name from the previous step;  can be anything.)
openstack image create --private --file
#  You can now create a volume from the uploaded image. In the new cloud web UI, navigate to Compute -> Images. The uploaded image from the previous step should be there. In the drop-down menu for the image, select the option Create Volume and the volume will be created from the image. The created volume can then be attached to instances or used to boot a new instance.
#  Once you have migrated and validated your instances and volumes, and once all associated DNS records are updated, please delete your old instances and volumes on the legacy cloud.

=== Alternative method: Migrating a volume-backed instance using Linux 'dd' ===

# Launch an instance on the legacy cloud with the smallest flavor possible (p1-1.5gb). Let’s call this the temporary migration host. The instructions below assume you choose AlmaLinux 9, but any Linux distribution with Python and Pip available should work.
# Log into the instance via SSH and install the OpenStack CLI in a root shell.

dnf install epel-release
dnf install python-devel python-pip gcc
pip install python-openstackclient

#  To verify if it is installed, try executing OpenStack on the command line. For further instructions, including installing the OpenStack CLI on systems other than AlmaLinux, see https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html.
# Copy your OpenStack RC file from the new cloud to the temporary migration host and source it. Verify that you can connect to the OpenStack API on the new cloud by running openstack image list.
# Delete the instance to be moved, but do NOT delete the volume it is attached to. The volume is now free to be attached to the temporary migration host we created.
# In the legacy cloud web UI, go to Volumes -> Volumes. From the drop-down menu select Manage Attachments and attach the volume to the temporary migration host. Take note of the device to which the volume is attached (typically /dev/vdb or /dev/vdc).
# Using the dd utility, create an image from the disk identified in the previous step. In the following example, we've named it volumemigrate. When the command completes, you will receive output showing the details of the image that was created.
 dd if=/dev/vdb | openstack image create --private --container-format bare --disk-format raw "volumemigrate"
#  In the new cloud web UI, go to Compute -> Images. The image can now be used to launch instances. If you want the data to be persistent, make sure to create a new volume when launching the instance.
#  Once you have migrated and validated your volumes and instances, and once any associated DNS records are updated, please delete your old instances and volumes on the legacy cloud.

=== Migrating large volumes using Linux 'dd' ===
Image-based methods are not recommended for large volumes. Instead, we recommend copying over your data to new volumes on Arbutus using rsync or a similar file copy tool wherever possible. In cases where this is not possible (e.g., for a bootable volume), the dd command can be used to make an identical copy on the new cloud of a volume from the legacy cloud.

As always, back up any important data prior to performing these steps.

# Create a temporary instance on the legacy cloud (p1-1.5gb should be fine) and do the same on the new cloud.
# Assign both of the above floating IPs that you can SSH into.
# Install the following packages on the temporary legacy instance:

dnf install epel-release
dnf install pv
dnf install screen

#  On the temporary new instance, run chmod u+s /bin/dd
# Copy the SSH private key you use to login as the user on the temporary new  instance to the temporary legacy instance.
# Make sure SSH security rules allow the temporary legacy instance to SSH into the temporary new instance.
# For each volume you want to move from legacy to new Arbutus:
## Create an empty volume of the same size on the new cloud and mark it as bootable if it's a boot volume.
## Attach the above volume to the temporary instance on the new cloud.
## Attach the volume you want to copy from the legacy cloud to the temporary legacy instance. Note: you may need to delete the instance it is currently attached to. Do NOT delete the volume.
# On the temporary legacy instance, execute the commands below. This assumes that the source volume on the legacy cloud is attached to the temporary legacy instance as /dev/vdb, the volume size is 96G, the SSH key being used to log into the temporary instance is key.pem, and the destination volume on Arbutus Cloud is attached to the temporary Arbutus Cloud instance as /dev/vdb. Also, replace xxx.xx.xx.xx by the actual IP address of the Arbutus instance you will be connecting to. The screen command is used in case you get disconnected from your SSH session.

screen
sudo dd bs=16M if=/dev/vdb | pv -s 96G | ssh -i key.pem user@xxx.xx.xx.xx "sudo dd bs=16M of=/dev/vdb"

Once the process is complete, you will have an exact copy of the volume from the legacy cloud on the new cloud, which you can then use to launch instances on the new cloud.

== Migrating ephemeral instances ==

An ephemeral instance is an instance without a backing volume.

=== Migration using Glance images and volume snapshots ===

See the Migration using Glance images section above.

=== Alternative method: Migrating an ephemeral instance using Linux 'dd' ===

See the Alternative method: Migrating a volume-backed instance using Linux 'dd' section above.

= Copying data =

Here are two recommended approaches for copying data between instances running in the two clouds. The most appropriate method depends on the size of the data volumes in your tenant.

== Large data volumes: Globus ==
For very large volumes (e.g., greater than 5TB) Globus is recommended.

There are several steps that need to be taken in order to make this work. The simplest method is to use the Globus Connect Personal client with a Globus Plus subscription. Following is a list of steps required:
# Request a Globus Connect Personal Plus subscription:
## Send an email to globus@tech.alliancecan.ca with your information and ask to be added to the Globus Plus subscription.
## When you receive the Plus invitation, follow the included instructions.
# On each cloud instance involved in the data transfer, enable Globus Connect Personal:
## Read the relevant guides for Globus Connect Personal: Personal Computers and https://www.globus.org/globus-connect-personal
## Install Globus Connect Personal on each instance, using the proper guide. The guide for Linux is https://docs.globus.org/how-to/globus-connect-personal-linux/.
## Adjust instances’ configuration to enable communication with the Globus Service:
### Ensure each VM has an external IP address.
### Ensure firewall rules on your VMs permit communication on the necessary ports.  See also Security groups.
### The user running Globus Connect Personal must have access to data on the instances’ storage systems.
## Run Globus Connect Personal as a background process in the user space.
## As a Globus Connect Personal Plus subscriber (enabled in step 1), create a shared endpoint on one or both VMs.
# Using any Globus Interface (globus.org, globus.computecanada.ca) access both endpoints just created and transfer data:
## Read data transfer manual here https://docs.globus.org/how-to/get-started/.
## Additional instructions here Transfer between two personal endpoints.

For more on configuration details, see: https://computecanada.github.io/DHSI-cloud-course/globus/

Contact globus@tech.alliancecan.ca if any issues arise during this whole process.  We also recommend you submit a support ticket in advance if you have very large volumes to move.

== Small data volumes: rsync + ssh ==
You may use any other method you are familiar with for transferring data; for small volumes however, rsync+ssh provides good transfer speeds and can (like Globus) work in an incremental way. When moving data with rsync, consider using the IPv6 GUA network in OpenStack. This network is a VLAN network that bypasses the OpenStack Neutron component, potentially offering improved data transfer performance.

A typical use case would be:

# SSH to the legacy instance which has the principal volume attached. Note the absolute path you want to copy to the instance on the new cloud.
# Execute rsync over SSH. The example below assumes that password-less login via SSH Keys has already been set up between the instances. Replace the 	placeholders below with actual values:
#:  rsync -avzP -e 'ssh -i ~/.ssh/key.pem' /local/path/ remoteuser@remotehost:/path/to/files/
# Verify that the data has been successfully copied on the instance in the new cloud. Then, delete the data from the legacy cloud.

= Post-transfer activities =

Once your data is transferred to the new instance, there may be some post-transfer configurations required, for example:

* updating firewall rules to use any new IP addresses and networks if a host-based firewall (e.g. iptables, firewalld, etc.) is used;
* working with your DNS provider to update DNS entries for any custom domains (e.g., www.myarbutusproject.ca);
* updating IP addresses in configuration files (e.g., /etc/hosts, /etc/resolv.conf, /etc/haproxy/haproxy.cfg, /var/www/ /var/lib/pgsql/data/pg_hba.conf);
* altering usernames (e.g., 'root'@'192.168.65.%) in MySQL;
* renewing Let’s Encrypt Transport Layer Security (TLS) certificates using certbot or other utilities if, for example, there are IP addresses in the certificate’s Subject Alternate Name (SAM).

Make sure you test the configuration before informing your research team and users that the migration has been completed.

= Migrating the CephFS shared filesystem =

The CephFS shared filesystem on the new cloud is a distinct and separate service; any desired data must be intentionally migrated there.

Management of legacy shares, including operations for creation, deletion, and key management, is controlled through the legacy Arbutus Cloud. However, once a legacy share and key are created, those resources can be accessed from a virtual machine in the new Arbutus cloud. Similarly, creation and management for shares in the new cloud is done exclusively in the new cloud environment.

Both legacy shares and new shares can be mounted on virtual machines in the new Arbutus cloud. The following procedure is recommended to ensure data integrity when migrating data between legacy and new shares.
# For each share in the legacy cloud, create an equivalent share in the new cloud.
# Mount both shares to separate mount locations on the same virtual machine in the new cloud.
# Use a data copy tool such as rsync to transfer the data from the old share to the new share.

The procedure for mounting legacy shares can be found in our CephFS wiki page.

Creating the equivalent share in the new Arbutus cloud follows a similar procedure, with a few essential differences:
# You must create the new share and access keys with the new cloud web user interface.
# You must create a separate ceph.conf file, with a distinct name such as ceph-new.conf.
# The mon_host config value will need to be updated for the new share only, in the ceph-new.conf file:
## Legacy value: “10.30.201.3:6789,10.30.202.3:6789,10.30.203.3:6789”
## New value: “[v2:134.87.15.61:3300/0,v1:134.87.15.61:6789/0] [v2:134.87.15.62:3300/0,v1:134.87.15.62:6789/0] [v2:134.87.15.63:3300/0,v1:134.87.15.63:6789/0]”
# When mounting the new share, an extra value in the mount command is required after the -o to specify the new configuration file conf=/etc/ceph/ceph-new.conf.

Once both shares are mounted, use rsync to transfer the data. The a, v, and P flags for rsync are recommended.

rsync -avp /mnt/old-share/ /mnt/new-share/

Keep in mind that depending on the size of your share, this may take a long time. To keep the session alive in case of a dropped connection, use a tool such as screen or tmux.

= Migrating object storage =

Object storage on the new cloud is a distinct and separate service; any desired data must be intentionally migrated there.

Management for legacy buckets and objects, including operations for creation, deletion, object manipulation, and key management, are controlled through the legacy cloud. Similarly, creation and management for buckets and objects in the new Arbutus cloud is done exclusively in the new Arbutus cloud environment.

Migrating data to the new cloud object storage can be done using a variety of methods and tools. If you are familiar with the options, feel free to use whichever method works best for your data.

New Arbutus Cloud Object Storage Endpoint: https://object-arbutus.alliancecan.ca

Legacy Arbutus Cloud Object Storage Endpoint: https://object-arbutus.cloud.computecanada.ca

If you’re using bucket ACLs, check if the tool you use copies them correctly, otherwise you must recreate them in the new environment. Most tools do not preserve bucket ACLs. Keep in mind that if you reference any user or project UUIDs, they will be different in the new Arbutus cloud.

Additionally, object storage in the new cloud uses tenants; therefore, bucket name collisions will only happen within an individual project instead of across all projects. When authenticating with either the Swift or S3 API, the tenant is inferred from the user/key provided. However, for public access to buckets with no authentication, the tenant must be specified. The Tenant ID is identical to the OpenStack Project ID. The URL for unauthenticated Swift access can be found via the Horizon interface, while the URL for unauthenticated S3 access is of the following format:

https://object-arbutus.alliancecan.ca/:/

If you are not sure which tool to use, we recommend rclone. Rclone will not copy the bucket ACLs, so all access will initially be defaulted as private in the new location. Here is an example:

# Install rclone with https://rclone.org/install/.
# Create S3 credentials in both the legacy and the new Arbutus clouds; see our Arbutus object storage wiki page.
# Create a config file for rclone:
## File location on linux/MacOS: ~/.config/rclone/rclone.conf
## File contents, inserting your access and secret values for each environment: [new]
type = s3
access_key_id =
secret_access_key =
endpoint = https://object-arbutus.alliancecan.ca
[legacy]
type = s3
access_key_id =
secret_access_key =
endpoint= https://object-arbutus.cloud.computecanada.ca
# Sync all buckets with rclone sync legacy: renewal:.

= Getting help =

Support requests can be sent to cloud@tech.alliancecan.ca.