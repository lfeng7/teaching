from fwlite_boilerplate import *

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputfile', metavar='F', type='string', action='store',
                  default = "",
                  dest='inputfile',
                  help='Input files')

(options, args) = parser.parse_args()

argv = []

# Constants
f1_type = ['F1','F-1','f1','F 1']
# Get input file
with open('check_data.csv','r') as fin:
    data = fin.readlines()

# Book histograms
h_days = ROOT.TH1D('h_days','complete days, 2013-2015, all locations and types;days;occurence',100,0,500)
h_days_f1 = ROOT.TH1D('h_days_f1','complete days, 2013-2015, F1, all locations;days;occurence',100,0,500)
h_days_shanghai = ROOT.TH1D('h_days_shanghai','complete days, 2013-2015, Shanghai;days;occurence',100,0,500)
h_days_shanghai_f1_renew = ROOT.TH1D('h_days_shanghai_f1_renew','complete days, 2013-2015, shanghai f1 renew;days;occurence',100,0,500)

hlist = [h_days,h_days_shanghai,h_days_f1,h_days_shanghai_f1_renew]

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
    
for ihist in hlist:    
    ihist.SetFillColor(4)

plotting(hlist,'check','dump','no testing','not log') 
saving(hlist,'check')
