import pumpz as pz

f_aq = open("aq.ppl", "w")
f_org = open("org.ppl", "w")
f_master = open("master.ppl", "w")

aq = pz.Pump(f_aq, 26.59)
org = pz.Pump(f_org, 26.59)
master = pz.Masterppl(f_master)
master.quickset({0: org, 1: aq})
pz.Pump.init(aq, org)

aq.rate(22, 20, "wdr")
org.rate(22, 20, "wdr")
aq.beep()
org.beep()

aq.rate(10, 20, "inf")
aq.rate(1,1,"wdr")
aq.beep()
pz.Pump.sync(aq, org)

org.pause(30)
org.rate(3, 10, "inf")
org.rate(10,10,"inf")
org.beep()
org.pause(120)

pz.Pump.sync(aq,org)
aq.loopstart(3)
org.loopstart(3)
aq.rate(22,50,'wdr')
org.rate(22,50,'wdr')
aq.rate(22,50,'inf')
org.rate(22,50,'inf')
aq.loopend()
org.loopend()
pz.Pump.stop(aq, org)
