import psutil
import os, popen2, sys
from time import sleep
sys.path.append("..")

from riemann import RiemannClient

#print psutil.disk_io_counters()
#print psutil.network_io_counters(pernic=True)

rc = RiemannClient()

def alert(service, state, metric, description):
    rc.send({'service': service, 'state':state, 'metric':metric, 'description':description})

def cores():
    return psutil.NUM_CPUS

def cpu_report():
    r, w, e = popen2.popen3('ps -eo pcpu,pid,args | sort -nrb -k1 | head -10')
    return r.readlines()

def cpu(warning=0.9, critical=0.95):
    c = psutil.cpu_times()
    used = c.user + c.system + c.nice
    total = used + c.idle
    f = used/total
    state = "ok"
    if f > warning: state="warning"
    if f > critical: state="critical"
    alert("cpu", state, f, "%.2f %% user+nice+sytem\n\n%s" % (f * 100, cpu_report()))

def disk(warning=0.9, critical=0.95):
    for p in psutil.disk_partitions():
        u = psutil.disk_usage(p.mountpoint)
        perc = u.percent
        f = perc/100.0
        state = "ok"
        if f > warning: state="warning"
        if f > critical: state="critical"
        alert("disk %s" % p.mountpoint, state, f, "%s used" % perc)

def load(warning=3, critical=8):
    l = os.getloadavg()
    f = l[2]/cores()
    state = "ok"
    if f > critical: state="critical"
    if f > warning: state="warning"
    alert("load", state, l[2], "15-minute load average/core is %f" % l[2])

def memory(warning = 0.85, critical=0.95):
    pm = psutil.phymem_usage()
    vm = psutil.virtmem_usage()
    sf = sv = "ok"
    ff = pm.percent / 100.0
    fv = vm.percent / 100.0
    if ff > warning: sf = "warning"
    if ff > critical: sf = "critical"
    if fv > warning: sv = "warning"
    if fv > critical: sv = "critical"
    alert("phisycal memory", sf, ff, "%.2f%% used\n\n%s" % (ff * 100, memory_report()))
    alert("virtual memory", sv, fv, "%.2f%% used\n\n%s" % (fv * 100, memory_report()))

def memory_report():
    r, w, e = popen2.popen3('ps -eo pmem,pid,args | sort -nrb -k1 | head -10')
    return r.readlines()

def tick():
    try:
        cpu()
        memory()
        load()
        disk()
    except Exception, e:
        print "Exception: %s" % e

def run():
    while True:
        tick()
        # uncomment the line below for a dump of all data (very verbose)
        # print rc.query('service')
        sleep(10)

if __name__ == "__main__":
    run()

