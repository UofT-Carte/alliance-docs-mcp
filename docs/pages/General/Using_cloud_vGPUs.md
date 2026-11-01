---
title: "Using cloud vGPUs"
url: "https://docs.alliancecan.ca/wiki/Using_cloud_vGPUs"
category: "General"
last_modified: "2026-10-23T19:12:29Z"
page_id: 13658
display_title: "Using cloud vGPUs"
---

This page describes how to
* allocate virtual GPU (vGPU) resources to a virtual machine (VM),
* install the necessary drivers and
* check whether the vGPU can be used.
Access to repositories as well as to the vGPUs is currently only available within the Arbutus cloud. Please note that the documentation below only covers the vGPU driver installation. The CUDA toolkit is not pre-installed but you can install it directly from  NVIDIA or load it from the CVMFS software stack.
If you choose to install the toolkit directly from NVIDIA, please ensure that the vGPU driver is not overwritten with the one from the CUDA package.

== Supported flavors ==

To use a vGPU within a VM, the instance needs to be deployed on one of the flavors listed below. The vGPU will be available to the operating system via the PCI bus.

* g1-12gb-c3-35gb-125
* g1-24gb-c6-70gb-250

== Preparation of a VM ==

Once the VM is available, make sure to update the OS to the latest available software, including the kernel.

Reboot the VM to have the latest kernel running.

It is recommended to install DKMS package, which is available via default repositories for all major distributions.
If the dkms package doesn't install the kernel-header package automatically, it needs to be installed manually via the package manager of your distribution.

Download the 2 files listed below to your system.

1. NVIDIA-Linux-x86_64-580.105.08-grid.run or NVIDIA-Linux-x86_64-580.178.04-grid.run

2. kalpa-prod.tok

wget https://object-arbutus.alliancecan.ca/swift/v1/6c87c15eb7d2468daf3d2bd0c58bbfce/vgpu/NVIDIA-Linux-x86_64-580.105.08-grid.run
wget https://object-arbutus.alliancecan.ca/swift/v1/6c87c15eb7d2468daf3d2bd0c58bbfce/vgpu/kalpa-prod.tok

Install the Nvidia vGPU driver with

root@vgpudoc:/home/debian# chmod 755 NVIDIA-Linux-x86_64-580.105.08-grid.run && ./NVIDIA-Linux-x86_64-580.105.08-grid.run

Options NVIDIA Proprietary and DKMS, are recommended.

After a successful  installation, reboot the system and verify via nvidia-smi that the OS has now proper access to the vGPU.

root@vgpudoc:/home/debian# nvidia-smi
Thu Apr  2 19:06:00 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.105.08             Driver Version: 580.105.08     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA H100L-1-12C             On  |   00000000:00:06.0 Off |                   On |
| N/A   N/A    P0            N/A  /  N/A  |       1MiB /  12288MiB |     N/A      Default |
|                                         |                        |              Enabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| MIG devices:                                                                            |
+------------------+----------------------------------+-----------+-----------------------+
| GPU  GI  CI  MIG |              Shared Memory-Usage |        Vol|        Shared         |
|      ID  ID  Dev |                Shared BAR1-Usage | SM     Unc| CE ENC  DEC  OFA  JPG |
|                  |                                  |        ECC|                       |
|==================+==================================+===========+=======================|
|  0    0   0   0  |               1MiB / 10565MiB    | 16      0 |  1   0    1    0    1 |
|                  |               0MiB /  4096MiB    |           |                       |
+------------------+----------------------------------+-----------+-----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+

The vGPU is now accessible and needs to be licensed. Copy the token kalpa-prod.tok to /etc/nvidia/ClientConfigToken/.

Configure nvidia-gridd, via the command below.

echo "FeatureType=4" >/etc/nvidia/gridd.conf

Enable nvidia-gridd and verify it's status.

systemctl enable --now nvidia-gridd

nvidia-gridd.service - NVIDIA Grid Daemon
     Loaded: loaded (/usr/lib/systemd/system/nvidia-gridd.service; enabled; preset: enabled)
     Active: active (running) since Thu 2026-04-02 19:11:13 UTC; 19s ago
 Invocation: 11dbb0370aee4ceeb1603481991037ec
    Process: 836 ExecStart=/usr/bin/nvidia-gridd (code=exited, status=0/SUCCESS)
   Main PID: 837 (nvidia-gridd)
      Tasks: 4 (limit: 42042)
     Memory: 2M (peak: 2.7M)
        CPU: 307ms
     CGroup: /system.slice/nvidia-gridd.service
             ââ837 /usr/bin/nvidia-gridd

Apr 02 19:11:13 vgpudoc systemd[1]: Starting nvidia-gridd.service - NVIDIA Grid Daemon...
Apr 02 19:11:13 vgpudoc nvidia-gridd[837]: Started (837)
Apr 02 19:11:13 vgpudoc systemd[1]: Started nvidia-gridd.service - NVIDIA Grid Daemon.
Apr 02 19:11:13 vgpudoc nvidia-gridd[837]: vGPU Software package (0)
Apr 02 19:11:13 vgpudoc nvidia-gridd[837]: Ignore service provider and node-locked licensing
Apr 02 19:11:13 vgpudoc nvidia-gridd[837]: NLS initialized
Apr 02 19:11:14 vgpudoc nvidia-gridd[837]: Acquiring license. (Info: api.cls.licensing.nvidia.com; NVIDIA Virtual Compute Server)
Apr 02 19:11:16 vgpudoc nvidia-gridd[837]: License acquired successfully. (Info: api.cls.licensing.nvidia.com, NVIDIA Virtual Compute Server; Expiry: 2026-4-3 19:11:16 GMT)

Once gridd has received a valid license, all features of the vGPU can be used. The licenses renewal is handled via nvidia-gridd automatically.