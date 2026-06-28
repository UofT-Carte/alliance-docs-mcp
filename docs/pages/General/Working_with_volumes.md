---
title: "Working with volumes/en"
url: "https://docs.alliancecan.ca/wiki/Working_with_volumes/en"
category: "General"
last_modified: "2026-06-18T17:33:41Z"
page_id: 21268
display_title: "Working with volumes"
---

A volume provides storage which is not destroyed when a VM is terminated. On our clouds, volumes use Ceph storage with either a 3-fold replication factor or erasure codes to provide safety against hardware failure. On Arbutus, the rbd1 volume type is stored on spinning disk hard drives and uses erasure codes to provide data safety while reducing the extra storage costs of 3-fold replication. The high_performance volume type is stored on solid state NVMe drives and uses the less storage efficient but higher performance 3-fold replication factor. More documentation about OpenStack volumes can be found here.

=Creating a volume=

To create a volume click on  and fill in the following fields:

*Volume Name: data, for example
*Description: (optional)
*Volume Source: No source, empty volume
*Type: No volume type
*Size (GiB): 40, or some suitable size for your data or operating system
*Availability Zone: the only option is nova

Finally, click on the blue Create Volume button at the bottom.

=Mounting a volume on a VM=
==Attaching a volume==

* Attaching is the process of associating a volume with a VM. This is analogous to inserting a USB key or plugging an external drive into your personal computer.
* You can attach a volume from the Volumes page in the dashboard.
* At the right-hand end of the line describing the volume is the Actions column; from the drop-down menu, select Manage Attachments.
* In the Attach to Instance drop-down menu, select a VM.
* Click on the blue Attach Volume button.
Attaching should complete in a few seconds. Then the volumes page will show the newly created volume attached to your selected VM on /dev/vdb or some similar location.
==Formatting a newly created volume==
* DO NOT FORMAT if you are attaching an existing volume. Instead you can skip this step as the volume would have already been formatted if you had been previously using it to store data.
* Formatting erases all existing information on a volume and therefore should be done with care.
* Formatting is the process of preparing a volume to store directories and files.
* Before a newly created and attached volume can be used, it must be formatted.
* See instructions for doing this on a Linux or Windows VM.

==Mounting a volume==
* Mounting is the process of mapping the volume's directory and file structure logically within the VM's directory and file structure.
* To mount the volume, use a command similar to [name@server ~]$ sudo mount /dev/vdb1 /mnt depending on the device name, disk layout, and the desired mount point in your filesystem.
This command makes the volume's directory and file structure available under the VM's /mnt directory. However, when the virtual machine reboots, the volume will need to be re-mounted using the same mount command.

It is possible to automatically mount volumes when a virtual machine boots. This requires editing the file named /etc/fstab to contain a new line with details about how the volume should be mounted.

To view mounting information, use the 'blkid' command
blkid

Based on the UUID, add a line to /etc/fstab like this:

/dev/disk/by-uuid/anananan-anan-anana-anan-ananananana /mnt auto defaults,nofail 0 3

Where 'anananan-anan-anana-anan-ananananana' is substituted with UUID of the device you wish to auto-mount.

For details on how to edit this file, see this Ubuntu community help page.

=Booting from a volume=

If you want to run a persistent machine, it is safest to boot from a volume. When you boot a VM from an image rather than a volume, the VM is stored on the local disk of the actual machine running the VM. If something goes wrong with that machine or its disk, the VM may be lost. Volume storage has redundancy, which protects the VM from hardware failure. Typically when booting from a volume VM flavors starting with the letter p are used (see Virtual machine flavors).

For details on storage options, see this Cloud storage options.
There are several ways to boot a VM from a volume. You can
* boot from an image, creating a new volume, or
* boot from a pre-existing volume, or
* boot from a volume snapshot, creating a new volume.

If you have not done this before, then the first one is your only option. The other two are only possible if you have already created a bootable volume or a volume snapshot.

If creating a volume as part of the process of launching the VM, select Boot from image (creates a new volume), select the image to use, and the size of the volume. If this volume is something you would like to remain longer than the VM, ensure that the Delete on Terminate box is not checked. If you are unsure about this option, it is better to leave this box unchecked. You can manually delete the volume later.

=Creating an image from a volume=

Creating an image from a volume allows you to download the image. Do this if you want to save it as a backup, or to spin up a VM on a different cloud, e.g., with VirtualBox. If you want to copy a volume to a new volume within the same cloud see cloning a volume instead.

To create an image of a volume, it must first be detached from a VM. If it is a boot (root) volume, it can only be detached from a VM if the VM is terminated/deleted; however, make sure you have not checked Delete Volume on Instance Delete when creating the VM.

Large images (more than 10-20GB) may be very slow to create, upload, and otherwise manage. You may want to consider  separating data if possible.

==Using the dashboard==
# Click on the Volumes left-hand menu.
# Under the volume you wish to create an image of click on the drop-down Actions menu and select Upload to Image.
# Choose a name for your new image.
# Choose a disk format. QCOW2 is recommended for using within the OpenStack cloud as it is relatively compact compared to Raw and works well with OpenStack. If you wish to use the image with Virtualbox, the vmdk or vdi image formats might be better suited.
# Finally, click on Upload.

==Using the command line client==
The command line client can do this:

where
*  is the disk format (two possible values are qcow2 and vmdk),
*  can be found from the OpenStack dashboard by clicking on the volume name, and
*  is a name you choose for the image.
You can then download the image.

=Cloning a volume=
Cloning is the recommended method for copying volumes. While it is possible to make an image of an existing volume and use it to create a new volume, cloning is much faster and requires less movement of data behind the scenes. This method is handy if you have a persistent VM and you want to test out something before doing it on your production site. It is highly recommended to shut down your VM before creating a clone of the volume as the newly created volume may be left in an inconsistent state if there was writing to the source volume during the time the clone was created. To create a clone you must use the command line client with this command

=Detaching a volume=
Before detaching a volume, it is important to make sure that the operating system and other programs running on your VM are not accessing files on this volume. If so, the detached volume can be left in a corrupted state or the programs could show unexpected behaviours. To avoid this, you can either shut down the VM before you detach the volume or unmount the volume.

To detach a volume, log in to the OpenStack dashboard (see the list of links to our cloud systems) and select the project containing the volume you wish to detach. Selecting Volumes -> Volumes displays the project’s volumes. For each volume, the Attached to  column indicates where the volume is attached.

*If attached to /dev/vda, it is a boot volume; you must delete the attached VM before the volume can be detached otherwise you will get the error message Unable to detach volume.

*With volumes attached to /dev/vdb, /dev/vdc, etc. you do not need to delete the VM it is attached to before proceeding. In the Actions column drop-down list, select Manage Attachments, click on the Detach Volume button and again on the next Detach Volume button to confirm.