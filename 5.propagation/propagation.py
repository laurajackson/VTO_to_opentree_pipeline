
# Date 06/06/2016
# This scripts propagates data of internal nodes to their species.
# If the species already have data for a specific internal node that data will be kept.
# All the other species without data will be added to data file. For now, the propagation only considers internal taxa up to family level.
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

# The following loop iterates the VTO.owl file and stores taxonomy hierarchy in dictionaries
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


# the dictionaries and lists required for propagation method is listed below
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
        #separating the taxa into different taxonomic levels and storing in the lists defined above
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
                nochild.append(x)  # taxonomic level undefined




# the list below contains species list for original set of species in the input matrix for this code
speciesold = species
speciesold = set(speciesold)
# print nochild
# print genus
# print other

############ propagation
pecnew =[]
pelnew= []

## these 3 dics are used for count the number of species in interanal taxa
excount ={}
necount ={}
totcount ={}


#### The method for performing the propagation

def propagate(x):
    replaced = []
    empty =[]
    pecreplaced =[]
    pelreplaced =[]

    # iterating trough internal taxa in the given list
    for i in x:

        # if taxa do not have data, append them to empty list
        if (pectoral[i]== '?') and (pelvic[i]== '?'):
            empty.append(i)

        # if the taxa do have data...
        else:
            # append them to the replaced list
            replaced.append(i)

            # retrieving the descendents of each internal taxa
            li = list(nx.descendants(G, name[i]))
            tot=0
            ec =0
            nc =0

            # for each taxa in the descendents list
            for j in li:
                # retrieve the taxa name
                j = namer[j]

                # check wether it is a species or genus
                if ' ' in j:
                    tot=tot+1
                    j = j.replace(' ','_')

                    # if the species is in the input matrix go into this code
                    if j in species:
                        ec= ec+1
                        # propagate only if the existing species do not have data or have '?' as state
                        # propagating the pectoral fin
                        if pectoral[j]== '?':
                            if pectoral[i] != '?':
                                pectoral[j] = pectoral[i]
                                pecnew.append(j)
                                pecreplaced.append(i)
                        # propagating for the pelvic fin
                        if pelvic[j]== '?':
                            if pelvic[i] != '?':
                                pelvic[j] = pelvic[i]
                                pelnew.append(j)
                                pelreplaced.append(i)

                    # if the descendent species is not in the original matrix we need to add it
                    else:
                        # counting the newly added species
                        nc = nc+1
                        # appending new species into a list
                        newspecies.append(j)
                        species.append(j)
                        # propagating the data into pectoral and pelvic fins
                        pectoral[j] = pectoral[i]
                        pelvic[j] = pelvic[i]
                        # counting the propagated number for newly added species for pectoral and pelvic fins
                        if pectoral[i] != '?':
                            pecnew.append(j)
                            pecreplaced.append(i)
                        if pelvic[i] != '?':
                            pelnew.append(j)
                            pelreplaced.append(i)
            excount[i]=ec
            necount[i]=nc
            totcount[i]=tot
    # the method peforms the propagation and retuns lists for emty taxa, total propagated, pelvic propagated and pectoral propagated
    return replaced,empty,pecreplaced,pelreplaced


# these two lines actually performs the propagation

# first start propagating the genus data; this must be peformed before family data propagation
genus_replaced, genus_empty, genus_pec,genus_pel = propagate(genus)

# then propagating the family data
family_replaced, family_empty, family_pec, family_pel = propagate(families)

########### printing the final matrix output

# defining the propagated matrix; this is the final matrix that contains VTO names
out = open('finalVTOmatrix.txt', 'wb+')

# writing the header of the propagated matrix
out.write('taxa_name\tpectoral_fin\tpelvic_fin\tpectoral_inferred\tpelvic_inferred\tpectoral_propagated\tpelvic_propagated\n')

# The propagated matrix only contains species; iterate trough species

for i in species:
    #print i
    # here, pc and pl are the original character states for each species; for instance, state 2 is inferred presence
    # which is originally represented as 1

    if pectoral[i] =='2':
        pc = '1'
    else:
        pc = pectoral[i]
    if pelvic[i] =='2':
        pl = '1'
    else:
        pl = pelvic[i]

    # if the species was propagated for pectoral fin, it should be found within pecnew list, thus represented as 1 for propagation
    if i in pecnew:
        pcn = '1'
    else:
        pcn = '0'

    # if the species was propagated for pelvic fin, it should be found within pelnew list, thus represented as 1 for propagation
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
genus_replaced = set(genus_replaced)
family_replaced = set(family_replaced)
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

################what families and genera the data is propagating from??? ######

genus_pec = set(genus_pec)
genus_pel = set(genus_pel)
family_pec = set(family_pec)
family_pel = set(family_pel)

# focusing on families first
famint = family_pec & family_pel
fampeconly = family_pec - family_pel
fampelonly = family_pel - family_pec

# data for genera
genusint = genus_pec & genus_pel
genpeconly = genus_pec - genus_pel
genuspelonly = genus_pel - genus_pec

# generates statistics for families and genera that propagated data
out3 = open('famlilyand_genera_propahated.txt', 'wb+')

out3.write('Number of families that propagated data for pectoral fin: %s\n'%(len(family_pec)))
out3.write('Number of families that propagated data for pelvic fin: %s\n'%(len(family_pel)))
out3.write('Number of genera that propagated data for pectoral fin: %s\n'%(len(genus_pec)))
out3.write('Number of genera that propagated data for pelvic fin: %s\n'%(len(genus_pel)))
out3.write('\n')
out3.write('Number of families that propagated data for bothfins: %s\n'%(len(famint)))
out3.write('Number of genera that propagated data for bothfins: %s\n'%(len(genusint)))
out3.write('Number of families that propagated data only for pectoral fin: %s\n'%(len(fampeconly)))
out3.write('Number of families that propagated data only for pelvic fin: %s\n'%(len(fampelonly)))
out3.write('Number of genera that propagated data only for pectoral fin: %s\n'%(len(genpeconly)))
out3.write('Number of genera that propagated data only for pelvic fin: %s\n'%(len(genuspelonly)))
out3.write('\n')
out3.write('\n')
out3.write('list of families that propagated data only for pectoral fin\n')
out3.write('families\tnew_species_count\n')
for i in fampeconly:
    out3.write('%s\t%s\n'%(i,necount[i]))

out3.write('\n')
out3.write('\n')
out3.write('list of families that propagated data only for pelvic fin\n')
out3.write('families\tnew_species_count\n')
for i in fampelonly:
    out3.write('%s\t%s\n'%(i,necount[i]))

out3.write('\n')
out3.write('\n')
out3.write('list of families that propagated data for both fins\n')
out3.write('families\tnew_species_count\n')
for i in famint:
    out3.write('%s\t%s\n'%(i,necount[i]))


out3.write('\n')
out3.write('\n')
out3.write('list of genera that propagated data for pectoral fin only\n')
out3.write('genus\tnew_species_count\n')
for i in genpeconly:
    out3.write('%s\t%s\n'%(i,necount[i]))

out3.write('\n')
out3.write('\n')
out3.write('list of genera that propagated data for pelvic fin only\n')
out3.write('genus\tnew_species_count\n')
for i in genuspelonly:
    out3.write('%s\t%s\n'%(i,necount[i]))

out3.write('\n')
out3.write('\n')
out3.write('list of genera that propagated data for both fins\n')
out3.write('genus\tnew_species_count\n')
for i in genusint:
    out3.write('%s\t%s\n'%(i,necount[i]))

