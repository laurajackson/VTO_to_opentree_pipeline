import dendropy
import re

nexmlname = "teleostei-pectoral_pelvic_fin_only.xml"
#opening the xml file
xmlfile = open(nexmlname, 'r')

# defining empty list to store character names
charlist = []

#this loop appends character names to the empty list
for line in xmlfile:
    if '<char id=' in line:
        #print line
        name1 = re.search('label="(.*)" about=', line)
        cname = name1.group(1)
        #print cname
        charlist.append(cname)

# printing the character list
print charlist

# converting the character list into a tuple
chartuple = tuple(charlist)

#print chartuple

# reading the nexml matrix using dendropy module
cmatrix = dendropy.StandardCharacterMatrix.get(path=nexmlname,schema="nexml")

# opening the output matrix
out = open("tabdelemited_charactermatrix.txt", 'wb+')

#writing the header of the output matrix: first the taxa name
out.write('taxa_name\t')

# and then all the character names
for i in chartuple:
    out.write('%s\t'%(i))

out.write('\n')

tot_num_char = len(chartuple)

# following loop goes fills character states for all taxa in tabdelimited format
# for conflicts it will print as 0 and 1, which is the default representation in phenoscape
# all the empty cells (without data) will have ?
for taxon in cmatrix:
    charlist = cmatrix[taxon]
    out.write('%s\t'%(taxon.label))
    #out.write('%s\n'%(charlist))
    number_to_append = tot_num_char - len(charlist)
    for num in range(number_to_append):
        charlist.append(None)
    for i in charlist:
        if i == None:
            i = '?'
        out.write('%s\t' % (i))
    out.write('\n')

