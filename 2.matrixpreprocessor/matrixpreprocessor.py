# author Pasan Fernando
# Date 06/13/2016
# Takes the tab delemited matrix that is converted from nexml format.
# prints all the taxa into a separate file
# Also removes the missing taxa ( ones with two ? for both pelvic and pectoral fins) and prints the statistics
__author__ = 'pasan fernando'
######################################################################################################################

import re
import networkx as nx
import collections

###### Reading the Vertebrate Taxonomy ontology (VTO) file to store relationships

p = open('vtonewfinal.owl', 'r')

G = nx.DiGraph()
# The dictiorary to store VTO name as the key and id as the value
name = {}
# The dictiorary to store id as the key and VTO name as the value
namer ={}
# The dictionary to store the rank of the taxa name; rank changes based on taxnonomic level
rank= {}

# The following loop iterates the VTO.owl file and stores taxonomy hirachy in dictionaries
for line in p:
    # print line
    if '<!-- http://purl.obolibrary.org/obo/' in line:
        result = re.search('<!-- http://purl.obolibrary.org/obo/(.*)-->', line)
        x = result.group(1)
        x1 = x.strip()
        # print x1
        if G.has_node(x1) == False:
            G.add_node(x1)

    if '<rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">' in line:
        name1 = re.search('<rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">(.*)</rdfs:label>', line)
        n = name1.group(1)
        # print n
        name[n] = x1
        namer[x1] = n
    #
    if '<rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/' in line:
        s = re.search('<rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/(.*)"/>', line)
        k = s.group(1)

        G.add_edge(k, x1)

    if '<vto:has_rank rdf:resource="http://purl.obolibrary.org/obo/TAXRANK_' in line:
        s = re.search('<vto:has_rank rdf:resource="http://purl.obolibrary.org/obo/TAXRANK_(.*)"/>', line)
        r = s.group(1)
        rank[n]=r

# print len(name)
# print len(rank)

######################################################################################################################


missinglist =[]
alltaxa =[]
remainingspecies =[]

######Read the tab delimited data matrix
#in1 = raw_input('enter the input matrix:')

d = open('tabdelemited_charactermatrix.txt', 'r')

for line in d:
    if (line != '\n') and ('taxa_name' not in line):
        line = line.strip()
        a = line.split('\t')
        a[0] = a[0].strip('\'')
        # following replacements removes the conventional naming errors in VTO names
        a[0] = a[0].replace(' ', '_')
        a[0] = a[0].replace('(', '')
        a[0] = a[0].replace(')', '')
        x = a[0]
        y = a[1]
        z = a[2]
        # some has and typed in for conflicts: 'O and 1' replace this with '0&1'
        if 'and' in y:
            line = line.replace(' and ','&')
        if 'and' in z:
            line = line.replace(' and ', '&')
        # store all the taxa in the input matrix in this list below
        alltaxa.append(x)
        # store all the taxa with missing states for all characters in the missinglist
        if (y=='?') and (z=='?'):
            missinglist.append(x)
        # remaining species are stored in the list below
        else:
            remainingspecies.append(line)



######################################################################################################################
#writing the missing removed matrix
out2 = open('missingremoved_matrix.txt', 'wb+')
out2.write('taxa_name\tpectoral_fin\tpelvic_fin\n')
for i in remainingspecies:
    out2.write('%s\n'%(i))

print 'the number of remaining taxa',len(remainingspecies)

######################################################################################################################
# writing all the taxa in the original matrix in originaldatamatrix_taxalist file
out = open('originaldatamatrix_taxalist.txt', 'wb+')

for i in alltaxa:
    out.write('%s\n'%(i))

print 'Statistics for all taxa and missing character state taxa:'
print len(alltaxa)

print len(missinglist)
print len(set(missinglist))

######################################################################################################################

## a method to print all taxa in any given list in a given output file
def printout(lis, out):
    out.write('taxa count: %s\n'%(len(lis)))

    for l in lis:
        out.write('%s\n'%(l))

    return

# a method to separate a list of taxa into different taxanomic levels basaed on VTO taxonomy ontology
def taxaseparate(lis1,out):
    total = []
    families = []
    genus = []
    species = []
    order = []
    nochild = []
    other = []

    for x in lis1:
        if '_' in x:
            species.append(x)
        elif x.endswith('idae'):
            families.append(x)
        elif x.endswith('iformes'):
            order.append(x)
        else:
            if x in rank:
                if rank[x] == '0000005':
                    genus.append(x)
                else:
                    other.append(x)
            else:
                nochild.append(x)

    out.write('orders\t')
    printout(order,out)
    out.write('\n')
    out.write('familes\t')
    printout(families,out)
    out.write('\n')
    out.write('\n')
    out.write('genera\t')
    printout(genus,out)
    out.write('\n')
    out.write('species\t')
    printout(species, out)
    out.write('\n')
    out.write('higher level taxa with rank\t')
    printout(other,out)
    out.write('\n')
    out.write('higher level taxa without rank\t')
    printout(nochild,out)
    out.write('\n')

    return

######################################################################################################################
# writing the missing taxa separated into different levels

out1 = open('missingtaxa.txt', 'wb+')
out1.write('total missing taxa: %s\n'%(len(missinglist)))

taxaseparate(missinglist,out1)

######################################################################################################################
# writing all taxa in the matrix separeted into levels
out3 = open('alltaxa.txt', 'wb+')
out3.write('total  taxa: %s\n'%(len(alltaxa)))

taxaseparate(alltaxa,out3)