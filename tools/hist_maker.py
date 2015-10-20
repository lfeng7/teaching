from fwlite_boilerplate import *

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputfile', metavar='F', type='string', action='store',
                  default = "",
                  dest='inputfile',
                  help='Input files')

(options, args) = parser.parse_args()

argv = []

grades = [int(line.strip()) for line in open(options.inputfile)]
print grades

# Book histograms
h1 = ROOT.TH1D('grades','lab3 grades;grades;occurence',30,35,50)

for grade in grades : h1.Fill(grade)
h1.SetFillColor(4)

hlist = [h1]
plotting(hlist,'teaching','dump','no testing','not log') 
saving(hlist,'teaching')
