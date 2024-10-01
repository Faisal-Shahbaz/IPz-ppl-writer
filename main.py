
from ipzppl import *
f_aq = open("aq.ppl", "w")
f_org = open("org.ppl", "w")
f_wash = open("wash.ppl", "w")

aq = pump(f_aq, 26.59)
org = pump(f_org, 26.59)
wash = pump(f_wash, 26.59)

aq.init()
org.init()
wash.init()

aq.rat(22, 20, "wdr") 
org.rat(22, 20, "wdr") 
aq.rat(10, 20, "inf") 
aq.pas(5 * 60)
print(f'aq: {aq.time}, org: {org.time}, wash: {wash.time}')
pump.sync(aq, org)
print(f'aq: {aq.time}, org: {org.time}, wash: {wash.time}')
org.rat(10, 20, "inf") 
org.pas(5 * 60)
pump.sync(org, wash)
wash.lps()
wash.rat(21, 50, "wdr", 3)
wash.rat(21, 50, "inf", 3)
wash.lop(3) 
