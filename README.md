# xen-tools-xendomains-wait-disk

[xendomains.service](https://github.com/mirage/xen/blob/master/tools/hotplug/Linux/systemd/xendomains.service.in) has problems
with disks that appear only latter in boot process (or even after booting is complete). This project creates a service that
loops over all disks that domU will use and wait for them to appear.

xendomains-wait-disk.service launches a script that reads both /etc/xen/auto/ configurations and /var/lib/xen/save/ dumps.
From those files, it extracts which disks are needed for all domU that will be started (respecting /etc/sysconfig/xendomains
settings). After that, it simply loops waiting for those disks to appear. There is a timeout (5 min) configured in
xendomains-wait-disk.service that prevents it to block booting process forever.

There are two known cases where this project is useful:

## degraded mdadm RAID

mdadm RAID are assembled by [udev rules](https://github.com/neilbrown/mdadm/blob/master/udev-md-raid-assembly.rules). 
However, it is only assembled when it is healthy. When not healthy, it starts a [timer](https://github.com/neilbrown/mdadm/blob/master/systemd/mdadm-last-resort%40.timer) that will try to assemble the RAID anyway after 30s. If a domU is depending on a degraded MD RAID (i.e. RAID 1 missing one disk), xendomains.service will be started before those 30s passed, failing that domU.

An alternative solution would be to add extra hard dependencies to xendomains.service for each required disk (Require=xxx.device). However, this solution introduces another greater problem. Before, if a single RAID is degraded, only the domU that depends on it will fail. With Require=xxx.device, xendomains will never start if
a RAID could not be assembled even after 30s (i.e. RAID5 with two missing disks).

With xendomains-wait-disk.service, xendomains.service will be blocked up to 5 min waiting for those MD RAID used by domUs. If it fails, xendomains.service
continues anyway.

## ISCSI disks

domU that uses iSCSI disk (mapped by host OS) also fails to start during boot. open-iscsi.service returns before it connect to the remote target and rescan
iscsi disks. As in mdadm RAID case, xendomains.service is started and domU that depends on iSCSI disks will fail.

## Installation


### Manually

 Copy xendomains-wait-disk to /usr/lib/xen-tools-xendomains-wait-disk/bin/xendomains-wait-disks

 Copy xendomains-wait-disk.service to systemd/system folder and enable it

 Relaod systemd daemon (systemctl daemon-reload)

 Enable xendomains-wait-disk.service (systemctl enable xendomains-wait-disk.service)

### Package

 Build xen-tools-xendomains-wait-disk.rpm from spec file and install
