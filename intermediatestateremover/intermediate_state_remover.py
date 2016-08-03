# this file works for the new format
#detects taxa with '0&1' and seperates them according to taxa level
# prints the literature sources for each taxa : the output is intented tobe reading only
# this code also replaces the intermediate taxa state of internal nodes by '?'
# 06/28/16
__author__ = 'pasan'


import re
import collections


u = raw_input('input the data file:')
p = open(u, 'r')

#reading the names of each taxa
name = {}
for line in p:
    if '<otu id=' in line:
        result = re.search('<otu id="(.*)" label', line)
        x = result.group(1)
        nm = re.search('label="(.*)" about', line)
        y = nm.group(1)
        name[x] = y


print len(name)
print name

##################################################################################
# reading the full tab delimited data file ands storing pectoral and pelvic taxa with 0&1
da = open('Final_dataONLY_6.6.16.txt', 'r')

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

print pectoral
print len(pectoral)
print pelvic
print len(pelvic)
source = collections.defaultdict(list)
count = []
p = open(u, 'r')
#getting the assertion data
z =None
if 'pectoral' in u:
    s = '<meta xsi:type="LiteralMeta" property="dc:identifier">UBERON_0000151'
else:
    s = '<meta xsi:type="LiteralMeta" property="dc:identifier">UBERON_0000152'

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
                print name[x]
                count = count +1

        else:
            if name[x] in pelvic:
                countpel = countpel+1

    if '<meta xsi:type="LiteralMeta" property="dc:source">' in line:
        result = re.search('<meta xsi:type="LiteralMeta" property="dc:source">(.*)</meta>', line)
        y = result.group(1)
        #print y
        if y not in source[name[x]]:
            source[name[x]].append(y)

print count
print countpel
print source

    # if s+'_0' in line:
    #
    #     z = '0'
    #
    # if s+'_1' in line:
    #     z = '1'
    #
    # if '<meta xsi:type="LiteralMeta" property="ps:isDirect">' in line:
    #     #print 'yes'
    #     result = re.search('<meta xsi:type="LiteralMeta" property="ps:isDirect">(.*)</meta>', line)
    #     y = result.group(1)
    #     # print y
    #     ont[x].append(y)
    #
    #     if y == 'false':
    #         if z =='0':
    #             count.append(x)
    #
    # #
    # if '<meta xsi:type="LiteralMeta" property="dc:identifier">UBERON_0000152_1' in line:
    #     z = '1'

out = open('intermediatecounts.txt', 'wb+')


#defining method for family count
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


if 'pectoral' in u:
    out.write('polymorpic state statistics for pectoral fin\n')
    out.write('total number of taxa: %s\n'%(len(pectoral)))
    out.write('\n')
    out.write('\n')
    pasan(pectoral)

else:
    out.write('polymorpic state statistics for pelvic fin\n')
    out.write('total number of taxa: %s\n'%(len(pelvic)))
    out.write('\n')
    out.write('\n')
    pasan(pelvic)


######## removing the internal taxa containing intermediate states
# note that when writing the new names the space in species name is replaced by '_" from herein
out1 = open('intermediate_removed_datamatrix.txt', 'wb+')
out1.write('taxa_name\tpectoral_fin\tpelvic_fin\n')
da = open('Final_dataONLY_6.6.16.txt', 'r')
for line in da:
    if line != '\n':
        line = line.strip()
        a = line.split('\t')
        a[0] =a[0].strip('\'')
        a[0] = a[0].replace(' ', '_')
        x = a[1]
        y = a[2]
        if '_' not in a[0]:
            if a[1] == '0&1':
                #print a[0]
                x = '?'
            if a[2] == '0&1':
                #print a[0]
                y = '?'
        out1.write('%s\t%s\t%s\t\n'%(a[0],x,y))