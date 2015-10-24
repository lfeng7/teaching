from fwlite_boilerplate import *

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputfile', metavar='F', type='string', action='store',
                  default = "",
                  dest='inputfile',
                  help='Input files')

(options, args) = parser.parse_args()

argv = []

with open('info.csv','r') as fin:
    data = fin.readlines()
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
    

print grades

# Book histograms
h_days = ROOT.TH1D('h_days','complete days;days;occurence',0,500,50)

for grade in grades : h1.Fill(grade)
h1.SetFillColor(4)

hlist = [h1]
plotting(hlist,'teaching','dump','no testing','not log') 
saving(hlist,'teaching')
