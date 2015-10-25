from fwlite_boilerplate import *
import datetime

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputfile', metavar='F', type='string', action='store',
                  default = "",
                  dest='inputfile',
                  help='Input files')

parser.add_option('--longdays', metavar='F', type='int', action='store',
                  default = 0,
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
h_dates = ROOT.TH1D('h_dates'+str(ldays),'complete dates, all locations and types, >'+str(ldays)+' days;dates;occurence',100,1,365)
h_month = ROOT.TH1D('h_month'+str(ldays),'completed month, F1 >'+str(ldays)+' days;the month;occurence',70,0,13)
h_month_start = ROOT.TH1D('h_month_start'+str(ldays),'start month, F1 >'+str(ldays)+' days;the month;occurence',70,0,13)

h_days = ROOT.TH1D('h_days'+str(ldays),'complete days,F1 >'+str(ldays)+' days;days;occurence',360/binw,0,360)
# Study the correlations
h_days_renew = ROOT.TH1D('h_days_renew'+str(ldays),'all renewal cases,> '+str(ldays)+' days;days;occurence',360/binw,0,360)
h_days_new = ROOT.TH1D('h_days_new'+str(ldays),'all new cases, >'+str(ldays)+' days;days;occurence',360/binw,0,360)
h_days_f1 = ROOT.TH1D('h_days_f1'+str(ldays),'all f1, >'+str(ldays)+' days;days;occurence',360/binw,0,360)
h_days_j1 = ROOT.TH1D('h_days_j1'+str(ldays),'all j1, >'+str(ldays)+' days;days;occurence',360/binw,0,360)
h_days_shanghai = ROOT.TH1D('h_days_shanghai'+str(ldays),'all Shanghai, F1 >'+str(ldays)+' days;days;occurence',360/binw,0,360)
h_days_beijing = ROOT.TH1D('h_days_beijing'+str(ldays),'all beijing, F1 >'+str(ldays)+' days;days;occurence',360/binw,0,360)
h_days_guangzhou = ROOT.TH1D('h_days_guangzhou'+str(ldays),'all Guangzhou, F1 >'+str(ldays)+' days;days;occurence',360/binw,0,360)

# My specific case
h_days_shanghai_f1_renew = ROOT.TH1D('h_days_shanghai_f1_renew'+str(ldays),'shanghai f1 renewal >'+str(ldays)+' days;days;occurence',360/binw,0,360)
h_days_shanghai_f1_new = ROOT.TH1D('h_days_shanghai_f1_new'+str(ldays),'shanghai f1 new >'+str(ldays)+' days;days;occurence',360/binw,0,360)
#hlist = [h_days,h_days_renew,h_days_new,h_days_f1,h_days_j1,h_days_shanghai,h_days_beijing,h_days_shanghai_f1_renew]
#hlist += [h_days_shanghai_f1_new]
#hlist = [h_days_guangzhou]
hlist = [h_dates,h_month,h_month_start]
nentry = 0
for line in data:

    raw_data = line.split('\t')
    visa_type = raw_data[2]
    visa_entry = raw_data[3]
    city = raw_data[4]
    major = raw_data[5]
    status = raw_data[6]
    check_date = raw_data[7]
    complete_date = raw_data[8]
    waiting_days = int(raw_data[9])

    complete_date = complete_date.split('-')
    check_date = check_date.split('-')

    complete_datetime = datetime.date(int(complete_date[0]),int(complete_date[1]),int(complete_date[2]))
    year_start = datetime.date(int(complete_date[0]),1,1)
    date = (complete_datetime-year_start).days
   
    month = int(complete_date[1])
    month_start = int(check_date[1])

    # Fill histograms
    if not  waiting_days>ldays and waiting_days<(ldays+interval) : continue

    if visa_type == 'F1' : 
        h_dates.Fill(date)
        h_month.Fill(month)
        h_month_start.Fill(month_start)

    h_days.Fill(waiting_days)

    if visa_type == 'F1' : h_days_f1.Fill(waiting_days)
    if visa_type == 'J1' : h_days_j1.Fill(waiting_days)
    if city == 'ShangHai' and visa_type == 'F1': h_days_shanghai.Fill(waiting_days)
    if city == 'BeiJing' and visa_type == 'F1': h_days_beijing.Fill(waiting_days)
    if city == 'GuangZhou' and visa_type == 'F1': h_days_guangzhou.Fill(waiting_days)
    if visa_entry == 'Renewal' : h_days_renew.Fill(waiting_days)
    if visa_entry == 'New' : h_days_new.Fill(waiting_days)
    if visa_type =='F1' and city == 'ShangHai' and visa_entry == 'Renewal' : h_days_shanghai_f1_renew.Fill(waiting_days)
    if visa_type =='F1' and city == 'ShangHai' and visa_entry == 'New' : h_days_shanghai_f1_new.Fill(waiting_days)
    
for ihist in hlist:    
    ihist.SetFillColor(4)

plotting(hlist,'check_all','dump','nolog',None,'','recreate') 
saving(hlist,'check_all')
