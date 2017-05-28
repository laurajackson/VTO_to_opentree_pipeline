# this file works for the new format
#detects taxa with '0&1' and seperates them according to taxa level
# prints the literature sources for each taxa : the output is intented tobe reading only
# this code also replaces the intermediate taxa state of internal nodes by '?'
# 06/28/16


'''Instructions for running the code
This code must be run twice for each fin (pectoral and pelvic fin)
The reason is it requires the pectoral and pelvic xml data to identify the conflict literature sources
Make sure the pectoral fin xml file contains the pectoral name in the file name
You can save the intermediatecounts.txt file as pectoral and pelvic fin conflicting data'''


__author__ = 'pasan fernando'


import re
import collections


u = raw_input('input the xml data file for each fin:')
p = open(u, 'r')

#reading the names of each taxa and storing in a dictionary

# This dictionary stores VTO id as key and taxa name as the value
name = {}
for line in p:
    if '<otu id=' in line:
        result = re.search('<otu id="(.*)" label', line)
        x = result.group(1)
        nm = re.search('label="(.*)" about', line)
        y = nm.group(1)
        name[x] = y


# print len(name)
# print name

##############################################################################################################################
# reading the full tab delimited data file ands storing pectoral and pelvic taxa with 0&1
da = open('missingremoved_matrix.txt', 'r')

# two dictionaries to store pectoral and pelvic fins
pectoral =[]
pelvic =[]

for line in da:
    if line != '\n':
        line = line.strip()
        a = line.split('\t')
        a[0] =a[0].strip('\'')
        a[0] = a[0].replace('_', ' ')
        if a[1] == '0&1':
            #print a[0]
            pectoral.append(a[0])
        if a[2] == '0&1':
            #print a[0]
            pelvic.append(a[0])

# print pectoral
# print len(pectoral)
# print pelvic
# print len(pelvic)

source = collections.defaultdict(list)
count = []

# again opening the xml file for interested fin (pectoral or pelvic)
p = open(u, 'r')


####################################################################################################################

'''the code section below, reads the xml file for the given fin, and checks wether they have '0&1' states in the matrix
Then it searches for the literature sources in the xml file and writes the conflicting sources in intermediatecounts.txt file'''


z =None

if 'pectoral' in u:
    s = '<meta xsi:type="LiteralMeta" property="dc:identifier">UBERON_0000151'
else:
    s = '<meta xsi:type="LiteralMeta" property="dc:identifier">UBERON_0000152'

# counters for counting number of conflicting states for pectoral and pelvic fin
count = 0
countpel = 0

for line in p:

    if '<row id=' in line:
        result = re.search('otu="(.*)"', line)
        x = result.group(1)
        #print x
        # print name[x]
        if 'pectoral' in u:

            if name[x] in pectoral:
                #print name[x]
                count = count +1

        else:
            if name[x] in pelvic:
                countpel = countpel+1

    # This code finds the literature source for each occurance of conflict state
    if '<meta xsi:type="LiteralMeta" property="dc:source">' in line:
        result = re.search('<meta xsi:type="LiteralMeta" property="dc:source">(.*)</meta>', line)
        y = result.group(1)
        #print y
        # store the literacture sources of conflicting states in a multiple dictionare
        # taxa name is the key and conflicting literature sources are values
        if y not in source[name[x]]:
            source[name[x]].append(y)

# print count
# print countpel
# print source


out = open('intermediatecounts.txt', 'wb+')


#defining method for family count
# This method takes a taxa list as an input and and separates them based on taxonomic level and writes the conflicting sources
# in output file
def pasan(li):
    family =[]
    genus = []
    species = []
    for e in li:
        nm1 = e
        if 'idae' in nm1:
            family.append(nm1)
        elif ' ' in nm1:
            species.append(nm1)
        else:
            genus.append(nm1)
    # print family
    # print species
    # print genus
    out.write('number of families: %d\n'%len(family))
    for line in family:
        li = source[line]
        out.write('%s\n' % (line, ))
        if  li:
            for i in li:
                out.write('       %s\n'%(i))
        # else:
        #     out.write('%s \n' % (line))
    out.write('\n')
    out.write('number of genera: %d\n'%len(genus))
    for line in genus:
        li = source[line]
        out.write('%s\n' % (line, ))
        if  li:
            for i in li:
                out.write('       %s\n'%(i))
    out.write('\n')
    out.write('number of species: %d\n'%len(species))
    for line in species:
        li = source[line]
        out.write('%s\n' % (line, ))
        if  li:
            for i in li:
                out.write('       %s\n'%(i))
    return

# writing conflict states for pectoral fin
if 'pectoral' in u:
    out.write('polymorpic state statistics for pectoral fin\n')
    out.write('total number of taxa: %s\n'%(len(pectoral)))
    out.write('\n')
    out.write('\n')
    pasan(pectoral)

# writing conflict states for pelvic fin
else:
    out.write('polymorpic state statistics for pelvic fin\n')
    out.write('total number of taxa: %s\n'%(len(pelvic)))
    out.write('\n')
    out.write('\n')
    pasan(pelvic)

####################################################################################################################
# removing the internal taxa containing intermediate states
# note that when writing the new names the space in species name is replaced by '_" from herein

# defining the name of the output file
out1 = open('conflicts_removed_datamatrix.txt', 'wb+')

# writing the header in the output file
out1.write('taxa_name\tpectoral_fin\tpelvic_fin\n')

# Opening the input matrix and removing the conflict states '0&1's from only the interanal nodes
da = open('missingremoved_matrix.txt', 'r')
for line in da:
    if (line != '\n') and ('taxa_name' not in line):
        line = line.strip()
        a = line.split('\t')
        a[0] =a[0].strip('\'')
        a[0] = a[0].replace(' ', '_')
        x = a[1]
        y = a[2]
        # the following if statement excludes all the species and removes '0&1' states only from internal nodes
        if '_' not in a[0]:
            if a[1] == '0&1':
                #print a[0]
                x = '?'
            if a[2] == '0&1':
                #print a[0]
                y = '?'
        out1.write('%s\t%s\t%s\t\n'%(a[0],x,y))