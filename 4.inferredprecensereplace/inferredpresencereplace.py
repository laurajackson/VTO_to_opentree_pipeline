# author: Pasan Fernando
# Date: 06/15/16
# Used to replace the character state of data matrix file for the taxa with inferred presence

#################################################################################################


pec = []
pelvic =[]

''' To run this code, taxa with inferred presence states for pectoral fin (pectoralinferred.txt) and pelvic fin (pelvicinferred.txt)
must be provided as separate lists. These lists are generated from another code that extracts this information from pectoral and pelvic
xml files'''

# reading the pelvic fin inferred presence list
pl = open('pelvicinferred.txt', 'r')

for line in pl:
    if line != '\n':
        line = line.strip()
        # removing the naming errors
        line = line.replace(' ','_')
        line = line.replace('(', '')
        line = line.replace(')', '')
        pelvic.append(line)


# print pelvic
# print len(pelvic)

# reading the pectoral fin inferred presence list
pc = open('pectoralinferred.txt', 'r')

for line in pc:
    if line != '\n':
        line = line.strip()
        line = line.replace(' ','_')
        line = line.replace('(', '')
        line = line.replace(')', '')
        pec.append(line)

#print len(pec)

pela=[]
peca=[]

# reading the input data matrix for the code
m = open('conflicts_removed_datamatrix.txt', 'r')

# defining the output matrix of the code
out = open('modified_inferredadded_matrix.txt', 'wb+')

# writing the header of the output matrix with two additional columns to distinguish inferred data
out.write('taxa_name\tpectoral_fin\tpelvic_fin\tpectoral_inferred\tpelvic_inferred\n')

# reading the input and selects the states with inferred presence which are represented by '2' hereafter
for line in m:
    if (line != '\n') and ( 'taxa_name' not in line):
        line = line.strip()
        a = line.split('\t')
        a[0] =a[0].strip('\'')

        a1 = a[0] # this line was required to keep the parenthesis within taxa names in the final VTO matrix
        a[0] = a[0].replace(' ', '_')
        a[0] = a[0].replace('(', '')
        a[0] = a[0].replace(')', '')
        if a[0] in pec:
            x = '2'
            peca.append(a[0])
        else:
            x = a[1]

        if a[0] in pelvic:
            y ='2'
            pela.append(a[0])

        else:
            y= a[2]

        out.write('%s\t%s\t%s\t%s\t%s\n'%(a1,a[1],a[2],x,y))



# print pela
# print peca

#################################################################################################
# generating statistics for inferred data

# defining another output file for inferred state statistics
out1 = open('inferredstats.txt', 'wb+')

# writing the number of taxa with inferred presence state
out1.write('inferred presence for pectoral fin: %i\n'%len(pec))
out1.write('inferred presence for pelvic fin: %i\n'%len(pelvic))


# Counting the unmapped taxa with inferred presence; the unmapped taxa are mismatched between pectoral and pelvic xml files
#with the input matrix with various naming errors; usually there are only one or two taxa like this; they are due to the presence
# of quot instead of actual "" in the taxa name

peld = set(pelvic) - set(pela)
peld =list(peld)

pecd = set(pec) - set(peca)
pecd = list(pecd)

out1.write('unmapped data for pectoral fin: %i\n'%len(pecd))
for i in pecd:
    out1.write('%s\n'%i)
out1.write('\n')
out1.write('\n')
out1.write('unmapped data for pelvic fin %i\n'%len(peld))
for i in peld:
    out1.write('%s\n'%i)