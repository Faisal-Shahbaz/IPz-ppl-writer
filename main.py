import pumpz as pz

f_aq = open("aq.ppl", "w")
f_org = open("org.ppl", "w")
f_master = open("master.ppl", "w")

aq = pz.Pump(f_aq, 26.59)
org = pz.Pump(f_org, 26.59)
master = pz.masterppl(f_master)
master.quickset({0: org, 1: aq})

pz.Pump.init(aq, org)
aq.rate(22, 20, "wdr")
org.rate(22, 20, "wdr")

aq.rate(3, 20, "inf")
aq.beep()
pz.Pump.sync(aq, org)

org.rate(3, 20, "inf")
org.beep()
org.pause(60)
pz.Pump.sync(aq,org)

aq.loopstart(3)
org.loopstart(3)
aq.rate(22,50,'wdr')
org.rate(22,50,'wdr')
aq.rate(22,50,'inf')
org.rate(22,50,'inf')

# pz.Pump.sync(org,wash)
# wash.loopstart(2)
# wash.rate(21, 50, "inf")
# wash.rate(21, 50, "wdr")
# wash.loopend()
# wash.rate(21, 50, "inf")
pz.Pump.stop(aq, org)
