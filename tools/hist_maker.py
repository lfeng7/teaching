from fwlite_boilerplate import *

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--inputfile', metavar='F', type='string', action='store',
                  default = "",
                  dest='inputfile',
                  help='Input files')

(options, args) = parser.parse_args()

argv = []

grades = [line for line in open(options.inputfile)]
print grades

# Book histograms
h1 = ROOT.TH1D('grades','lab3 grades;grades;occurence',10,35,50)

for i in grades : h1.Fill(grades)

hlist = [h1]
plotting(hlist,'teaching','dump','no','') 
