# author: Pasan Fernando
# Date: 06/15/16
# Used to replace the character state of data matrix file for the taxa with inferred presence
#################################################################################################


pec = []
pelvic =[]
pl = open('pelvicinferred.txt', 'r')

for line in pl:
    if line != '\n':
        line = line.strip()
        line = line.replace(' ','_')
        line = line.replace('(', '')
        line = line.replace(')', '')
        pelvic.append(line)


print pelvic
print len(pelvic)

pc = open('pectoralinferred.txt', 'r')

for line in pc:
    if line != '\n':
        line = line.strip()
        line = line.replace(' ','_')
        line = line.replace('(', '')
        line = line.replace(')', '')
        pec.append(line)

print len(pec)

pela=[]
peca=[]

m = open('intermediate_removed_datamatrix.txt', 'r')
out = open('modified_inferredadded_matrix.txt', 'wb+')
out.write('taxa_name\tpectoral_fin\tpelvic_fin\tpectoral_inferred\tpelvic_inferred\n')
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

        #print a

print pela
print peca

out1 = open('inferredstats.txt', 'wb+')
out1.write('inferred presence for pectoral fin: %i\n'%len(pec))
out1.write('inferred presence for pelvic fin: %i\n'%len(pelvic))
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