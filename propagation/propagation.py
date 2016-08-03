# author Pasan Fernando
# Date 06/06/2016
# This scripts propagates data of internal nodes to their species.
# If the species already have data for a specific internal node that data will be kept.
# All the other species without data will be added to data file. For now, the propagation only considers internal taxa up to family level.

######################################################################################################################

import re
import networkx as nx
import matplotlib.pyplot as plt
import collections

######Read VTO file to store relationships

p = open('vtonewfinal.owl', 'r')

G = nx.DiGraph()
name = {}
namer ={}
rank= {}

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

print len(name)
print len(rank)

pectoral = {}
pelvic ={}
pectoralo = {}
pelvico ={}
families =[]
genus = []
species = []
order =[]
nochild= []
other =[]
newspecies =[]

######Read the data file separate the taxa into levels: family, order, species, genera, others (differentiate between genus and others in this step)
d = open('modified_inferredadded_matrix.txt', 'r')

for line in d:
    if (line != '\n') and ('taxa_name' not in line):
        line = line.strip()
        a = line.split('\t')
        a[0] = a[0].strip('\'')
        # a[0] = a[0].replace(' ', '_')
        # a[0] = a[0].replace('(', '')
        # a[0] = a[0].replace(')', '')
        x = a[0]
        y = a[3]
        z = a[4]
        pectoralo[x]= a[1]
        pelvico[x]= a[2]
        pectoral[x] = y  #saving pectoral and pelvic data in the dictionaries
        pelvic[x] = z
        #save seperate the taxa into species, family and genera
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





speciesold = species
speciesold = set(speciesold)
print nochild
print genus
print other

############ propagation
pecnew =[]
pelnew= []

## these 3 dics are used for count the number of species in interanal taxa
excount ={}
necount ={}
totcount ={}


#### For i in genus: do the propagation

def propagate(x):
    replaced = []
    empty =[]
    for i in x:

        if (pectoral[i]== '?') and (pelvic[i]== '?'):
            empty.append(i)

        else:
            replaced.append(i)
            #print i
            li = list(nx.descendants(G, name[i]))
            tot=0
            ec =0
            nc =0

            for j in li:
                j = namer[j]
                if ' ' in j:
                    tot=tot+1
                    j = j.replace(' ','_')

                    if j in species:
                        ec= ec+1
                        if pectoral[j]== '?':
                            if pectoral[i] != '?':
                                pectoral[j] = pectoral[i]
                                pecnew.append(j)
                        if pelvic[j]== '?':
                            if pelvic[i] != '?':
                                pelvic[j] = pelvic[i]
                                pelnew.append(j)
                    else:
                        nc = nc+1
                        newspecies.append(j)
                        species.append(j)
                        pectoral[j] = pectoral[i]
                        pelvic[j] = pelvic[i]
                        if pectoral[i] != '?':
                            pecnew.append(j)
                        if pelvic[i] != '?':
                            pelnew.append(j)
            excount[i]=ec
            necount[i]=nc
            totcount[i]=tot
    return replaced,empty



genus_replaced, genus_empty = propagate(genus)
family_replaced, family_empty = propagate(families)

########### printing the final matrix output

out = open('finalVTOmatrix.txt', 'wb+')
out.write('taxa_name\tpectoral_fin\tpelvic_fin\tpectoral_inferred\tpelvic_inferred\tpectoral_propagated\tpelvic_propagated\n')

for i in species:
    #print i
    if pectoral[i] =='2':
        pc = '1'
    else:
        pc = pectoral[i]
    if pelvic[i] =='2':
        pl = '1'
    else:
        pl = pelvic[i]
    if i in pecnew:
        pcn = '1'
    else:
        pcn = '0'
    if i in pelnew:
        pln = '1'
    else:
        pln = '0'
    out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(i,pc,pl,pectoral[i],pelvic[i],pcn,pln))



###################### printing the statistics

out1 = open('propagationstatistics.txt', 'wb+')
out1.write('************* statistics for the original data file *******\n')
out1.write('number of species: %s\n'%(len(speciesold)))
out1.write('number of genera: %s\n'%(len(genus)))
out1.write('number of families: %s\n'%(len(families)))
out1.write('number of orders: %s\n'%(len(order)))
out1.write('number of other higher level taxa: %s\n'%(len(nochild)))


out1.write('\n')
out1.write('\n')





out1.write('************* statistics for the new data file *******\n')
out1.write('number of newly added species: %s\n'%(len(newspecies)))
out1.write('number of total species in the new data file: %s\n'%(len(species)))

out1.write('\n')
out1.write('\n')

out1.write('************* propagation statistics *******\n')
out1.write('newly propagated species for pelvic fin: %s\n'%(len(set(pelnew))))
out1.write('newly propagated species for pectoral fin: %s\n'%(len(set(pecnew))))
out1.write('number of genera that was propagated: %s\n'%(len(genus_replaced)))
out1.write('number of families that was propagated: %s\n'%(len(family_replaced)))
out1.write('\n')
out1.write('there were some internal nodes that had ? for both fins. There is no use of them for the propagation. They are printed below\n')
out1.write('\n')
out1.write('families :')
for i in family_empty:
    out1.write('%s,'%(i))
out1.write('\n')
out1.write('\n')

out1.write('genera :')
for i in genus_empty:
    out1.write('%s,'%(i))

out1.write('\n')
out1.write('\n')

out1.write('******the propagated counts for each internal node is given below\n')
out1.write('\n')
out1.write('families\t#existing_species_count\tnew_species_count\ttotal_number_of_speciesinVTO\n')
famcount=0
for i in family_replaced:
    famcount=famcount+totcount[i]
    out1.write('%s\t%s\t%s\t%s\n'%(i,excount[i],necount[i],totcount[i]))
out1.write('\n')
out1.write('genus\t#existing_species_count\tnew_species_count\ttotal_number_of_speciesinVTO\n')
for i in genus_replaced:
    out1.write('%s\t%s\t%s\t%s\n'%(i,excount[i],necount[i],totcount[i]))
# print genus_empty
# print len(genus)
#
# print len(families)
# print len(newspecies)
# print len(set(newspecies))
# print len(species)
# print len(set(species))
#

######printing a list of all species taxa for comparison purposes

out2 = open('finalVTOspecieslist.txt', 'wb+')
for i in species:
    out2.write('%s\n'%(i))



#print excount
#print necount
print famcount
print sum(totcount.values())
print sum(necount.values())

nofam=[]
for i in families:
    if rank[i]!='0000004':
        nofam.append(i)


print nofam
