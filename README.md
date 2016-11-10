munin-docsis
============

A munin plugin to graph the utilization of the own DOCSIS segment.

On the hardware side a DVB-C card or USB stick which is supported
by the used Linux kernel is required.

This is based on the Munin plugin previously published by Falk Husemann
but expands its support to non Sundteck DVB-C interfaces.

The munin plugin has been split up in two parts:
a) Data acquisition via cron job
b) Data presentation towards munin

The cron job currently needs to be run as root.

The installation is quite simple:
1) Copy cronjob.sh to e.g. /usr/local/sbin/munin-docsis-cron.sh
2) Copy etc/default/munin-docsis /etc/default/munin-docsis
3) Copy docsis_bandwidth /etc/munin/plugins

Ensure that the content of /etc/default/munin-docsis matches your environment.
