#!/bin/bash
# This cronjob generates a text file dump with the current channel usage which is used by the munin plugin.
# This reduces the munin runtime.

# source the configuration
source etc/defaults/munin-docsis

echoerr() { echo "$@" 1>&2; }

# configure stick

# disable sleep mode
/usr/local/bin/disableDVBSleep.sh

# set stick to DVB-C mode
/usr/bin/dvb-fe-tool -d DVBC/ANNEX_A &> /dev/null


TMPFILE=$( mktemp )
sum=0
for freq in $freqs
do
	# Tune to frequency
	${DVBTUNE} -f $freq -s 6952 -qam 256 &> /dev/null
	# Get bandwidth usage
	bandwidth=`timeout 3 sudo ${DVBSNOOP} -adapter 0 -s bandwidth 8190 -n 5000 -hideproginfo | awk -F: 'END { print $NF }' | sed 's/^[ t]*//' | awk '{print $1 * 1000}'`
	echo $freq.value $bandwidth >> $TMPFILE
	sum=$( expr $sum + $bandwidth )
done
echo sum.value $sum >> $TMPFILE

mv $TMPFILE $DATAFILE 
