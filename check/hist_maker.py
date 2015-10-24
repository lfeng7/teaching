from fwlite_boilerplate import *

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputfile', metavar='F', type='string', action='store',
                  default = "",
                  dest='inputfile',
                  help='Input files')

parser.add_option('--longdays', metavar='F', type='int', action='store',
                  default = 30,
                  dest='longdays',
                  help='how long is long check')

parser.add_option('--interval', metavar='F', type='int', action='store',
                  default = 10000,
                  dest='interval',
                  help='how many days for a check category. Like 30days? 60 Days?')

(options, args) = parser.parse_args()

argv = []

# Constants
f1_type = ['F1','F-1','f1','F 1']
binw = 7
# Get input file
with open('check_data_all.csv','r') as fin:
    data = fin.readlines()

ldays = options.longdays
interval = options.interval
# Book histograms
h_days = ROOT.TH1D('h_days','complete days, all locations and types;days;occurence',360/binw,0,360)
h_days_f1 = ROOT.TH1D('h_days_f1','complete days, F1, all locations;days;occurence',360/binw,0,360)
h_days_shanghai = ROOT.TH1D('h_days_shanghai','complete days, Shanghai;days;occurence',360/binw,0,360)
h_days_shanghai_f1_renew = ROOT.TH1D('h_days_shanghai_f1_renew','complete days, shanghai f1 renew;days;occurence',360/binw,0,360)
h_days_long = ROOT.TH1D('h_days_long_'+str(ldays),'complete days, all locations and types, checks longer than '+str(ldays)+' days;days;occurence',360/binw,0,360)


hlist = [h_days,h_days_shanghai,h_days_f1,h_days_shanghai_f1_renew,h_days_long]

for line in data:
    raw_data = line.split('\t')
    visa_type = raw_data[2]
    visa_entry = raw_data[3]
    city = raw_data[4]
    major = raw_data[5]
    status = raw_data[6]
    check_data = raw_data[7]
    complete_data = raw_data[8]
    waiting_days = int(raw_data[9])
    # Fill histograms
    h_days.Fill(waiting_days)
    if visa_type in f1_type : h_days_f1.Fill(waiting_days)
    if city == 'ShangHai': h_days_shanghai.Fill(waiting_days)
    if visa_type in f1_type and city == 'ShangHai' and visa_entry == 'Renewal' : h_days_shanghai_f1_renew.Fill(waiting_days)
    if visa_type in f1_type and city == 'ShangHai' and  waiting_days>ldays and waiting_days<(ldays+interval): h_days_long.Fill(waiting_days)
    
for ihist in hlist:    
    ihist.SetFillColor(4)

plotting(hlist,'check_all','dump','no testing','not log') 
saving(hlist,'check_all')
