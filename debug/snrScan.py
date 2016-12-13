#!/usr/bin/env python3

from subprocess import Popen, PIPE
import re
import time
import matplotlib.pyplot as plt


adapter=1
toTune=3 # seconds
toSample=1
dvbTune="/usr/bin/dvbtune"
symbolRate=6952
signalLimits=[-54, -43]
snrLowerLimit=32
frequencyLimits=(100,1000)

transponders=[
    {'nu': 114, 'qam': 256, 'sr': 6952,},
#    {'nu': 122, 'qam': 256, 'sr': 6952,},
    {'nu': 130, 'qam': 256, 'sr': 6952,},
#    {'nu': 138, 'qam': 256, 'sr': 6952,},
    {'nu': 146, 'qam': 256, 'sr': 6952,},
#    {'nu': 154, 'qam': 256, 'sr': 6952,},
    {'nu': 162, 'qam': 256, 'sr': 6952,},
#    {'nu': 170, 'qam': 256, 'sr': 6952,},
    {'nu': 346, 'qam': 256, 'sr': 6952,},
#    {'nu': 354, 'qam': 256, 'sr': 6952,},
#    {'nu': 362, 'qam': 256, 'sr': 6952,},
#    {'nu': 370, 'qam': 256, 'sr': 6952,},
#    {'nu': 378, 'qam': 256, 'sr': 6952,},
    {'nu': 386, 'qam': 256, 'sr': 6952,},
#    {'nu': 394, 'qam': 256, 'sr': 6952,},
#    {'nu': 402, 'qam': 256, 'sr': 6952,},
#    {'nu': 410, 'qam': 256, 'sr': 6952,},
#    {'nu': 418, 'qam': 256, 'sr': 6952,},
#    {'nu': 426, 'qam': 256, 'sr': 6952,},
#    {'nu': 434, 'qam': 256, 'sr': 6952,},
    {'nu': 442, 'qam': 256, 'sr': 6952,},
#    {'nu': 450, 'qam': 256, 'sr': 6952,},
#    {'nu': 458, 'qam': 256, 'sr': 6952,},
#    {'nu': 466, 'qam': 256, 'sr': 6952,},
#    {'nu': 474, 'qam': 256, 'sr': 6952,},
#    {'nu': 482, 'qam': 256, 'sr': 6952,},
    {'nu': 490, 'qam': 256, 'sr': 6952,},
#    {'nu': 498, 'qam': 256, 'sr': 6952,},
#    {'nu': 506, 'qam': 256, 'sr': 6952,},
#    {'nu': 514, 'qam': 256, 'sr': 6952,},
#    {'nu': 522, 'qam': 256, 'sr': 6952,},
#    {'nu': 530, 'qam': 256, 'sr': 6952,},
#    {'nu': 538, 'qam': 256, 'sr': 6952,},
    {'nu': 546, 'qam': 256, 'sr': 6952,},
#    {'nu': 554, 'qam': 256, 'sr': 6952,},
#    {'nu': 562, 'qam': 256, 'sr': 6952,},
#    {'nu': 570, 'qam': 256, 'sr': 6952,},
#    {'nu': 578, 'qam': 256, 'sr': 6952,},
    {'nu': 586, 'qam': 256, 'sr': 6952,},
#    {'nu': 594, 'qam': 256, 'sr': 6952,},
#    {'nu': 602, 'qam': 256, 'sr': 6952,},
#    {'nu': 610, 'qam': 256, 'sr': 6952,},
#    {'nu': 618, 'qam': 256, 'sr': 6952,},
#    {'nu': 626, 'qam': 256, 'sr': 6952,},
#    {'nu': 634, 'qam': 256, 'sr': 6952,},
    {'nu': 642, 'qam': 256, 'sr': 6952,},
#    {'nu': 650, 'qam': 256, 'sr': 6952,},
#    {'nu': 658, 'qam': 256, 'sr': 6952,},
#    {'nu': 666, 'qam': 256, 'sr': 6952,},
#    {'nu': 674, 'qam': 256, 'sr': 6952,},
#    {'nu': 682, 'qam': 256, 'sr': 6952,},
#    {'nu': 690, 'qam': 256, 'sr': 6952,},
    {'nu': 690, 'qam': 256, 'sr': 6952,},
#    {'nu': 706, 'qam': 256, 'sr': 6952,},
#    {'nu': 714, 'qam': 256, 'sr': 6952,},
#    {'nu': 722, 'qam': 256, 'sr': 6952,},
#    {'nu': 730, 'qam': 256, 'sr': 6952,},
#    {'nu': 738, 'qam': 256, 'sr': 6952,},
    {'nu': 746, 'qam': 256, 'sr': 6952,},
#    {'nu': 754, 'qam':  64, 'sr': 6952,},
#    {'nu': 762, 'qam':  64, 'sr': 6952,},
#    {'nu': 770, 'qam':  64, 'sr': 6952,},
#    {'nu': 778, 'qam':  64, 'sr': 6952,},
#    {'nu': 786, 'qam':  64, 'sr': 6952,},
#    {'nu': 794, 'qam':  64, 'sr': 6952,},
    {'nu': 802, 'qam':  64, 'sr': 6952,},
#    {'nu': 810, 'qam':  64, 'sr': 6952,},
#    {'nu': 818, 'qam':  64, 'sr': 6952,},
#    {'nu': 826, 'qam':  64, 'sr': 6952,},
#    {'nu': 834, 'qam':  64, 'sr': 6952,},
#    {'nu': 842, 'qam':  64, 'sr': 6952,},
#    {'nu': 850, 'qam':  64, 'sr': 6952,},
    {'nu': 858, 'qam':  64, 'sr': 6952,},
]

result_nu = []
result_sig = []
result_snr = []
for transponder in transponders:
    sigAvg = 0
    snrAvg = 0
    n = 0


    nu = transponder['nu']
    processTune = Popen(['timeout', str(toTune), dvbTune, '-c', str(adapter), '-f', str(nu*1e6), '-s', str(transponder['sr']), '-qam', str(transponder['qam'])], stdout=PIPE, stderr=PIPE)
    (output, err) = processTune.communicate()
    exit_code = processTune.wait()
#    print("DVB tune err-code", exit_code)
#    print(output, err)

    if exit_code != 0: continue
    time.sleep(1)

    print("%f MHz: " % ( nu, ), )

    process = Popen(['timeout', '--preserve-status', str(toSample), 'dvb-fe-tool', '-a', str(adapter), '-m', '-g'], stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
#    print(output.decode('utf-8'))

#    print(exit_code)
    lines = err.decode("utf-8").splitlines()
    for line in lines:
#        print(line)
        x = line.split()
        if len(x) != 6: continue
        state = x[0]
        sig = float(re.findall('[-+]?\d+[\.]?\d*[eE]?[-+]?\d', x[3])[0])
        snr = float(re.findall('[-+]?\d+[\.]?\d*[eE]?[-+]?\d', x[5])[0])
        if state == 'Lock':
            n += 1
            sigAvg += sig
            snrAvg += snr
#            print(" %f | %f" % ( sig, snr) )
    
    if n > 0:
        print
        sigAvg /= float(n)
        snrAvg /= float(n)
    
    result_nu.append(nu)
    result_sig.append(sigAvg)
    result_snr.append(snrAvg)
    print("%f;%f;%f" % (nu, sigAvg, snrAvg) )


for i in range(len(result_nu)):
    print("%f;%f;%f" % (result_nu[i], result_sig[i], result_snr[i]) )

# plot it
fig = plt.figure()
plt.subplots_adjust(left=0.10, bottom=0.10, right=0.95, top=0.90, wspace=0.20, hspace=0.4)
ax = fig.add_subplot(2, 1, 1)
ax.plot(result_nu, result_sig, 'o')
ax.set_title("Signal spectrum")
ax.set_xlabel("Frequency / MHz")
ax.set_ylabel("Signal / dBm")
ax.set_xlim(frequencyLimits)
for l in signalLimits: ax.axhline(l)

ax = fig.add_subplot(2, 1, 2)
ax.plot(result_nu, result_snr, 'o')
ax.set_title("SNR spectrum")
ax.set_xlabel("Frequency / MHz")
ax.set_ylabel("SNR / dB")
ax.axhline(snrLowerLimit)
ax.set_ylim(20, 40)
ax.set_xlim(frequencyLimits)

fig.savefig('scan.png', dpi=300)
fig.savefig('scan.pdf', dpi=300)
