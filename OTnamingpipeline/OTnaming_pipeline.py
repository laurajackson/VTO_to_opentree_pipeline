# author Pasan Fernando
# Date 06/12/2016
#
# This script is used to convert the VTO data matrix into open tree version.
# It will use combined approach that includes name conversion using NCBI ids and direct name matching.
# The script can also generate statistics for the final conversion.

######################################################################################################################

import re
import networkx as nx
import matplotlib.pyplot as plt
import collections

######Read VTO file to store relationships####################################################################################

p = open('vtonewfinal.owl', 'r')

G = nx.DiGraph()
name = {}
namer ={}
vtncbi ={}
vtncbir ={}
extinct =[]

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
     # extracting the ncbi taxon
    if '<oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">NCBITaxon:'in line:
        s = re.search('<oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">NCBITaxon:(.*)<', line)
        nc = s.group(1)
        ## there are synonyms for some taxa and they have ncbi id's as well so only the first ocurrance is stored
        if n not in vtncbi:
            vtncbi[n]=nc
        #reversed version: key is ncbi id
        if nc not in vtncbir:
            vtncbir[nc] = n

    if '<vto:is_extinct rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</vto:is_extinct>' in line:
        extinct.append(n)

########################## open tree data file processing########################################################################

otncbi ={}
otncbir={}
oid ={}
d = open('taxonomy.tsv', 'r')

for line in d:
    a = line.split('|')
    #print a
    otid = a[0].strip()
    otname = a[2].strip()

    #storing all ids
    oid[otname]=otid

    a1 = a[4].strip()
    #print a1

    if 'ncbi:' in a1:
        if ',' in a1:
            b = a1.split(',')
            for i in b:
                if 'ncbi' in i:
                    x = i

        else:
            x = a1
        #print '     ',x
        x=x.strip('ncbi:')
        otncbi[otname]=x
        #reversed assignment: key is ncbi id , value is name
        otncbir[x]=otname



# print len(oid)
# print len(otncbi)
# print len(otncbir)
# print len(vtncbi)
# print len(vtncbir)
# print len(name)


##### processing the VTO matrix############################################################################################################
matchnames={}
matchnamesr ={}
vtlist=[]
vtwitnc =[]
vtdic ={}
# list to count absences
peclosslist =[]
pellosslist =[]
pecprop =[]
pelprop=[]
pec ={}
pel ={}

# read the final VTO matrix, separate it so that name is the key and the rest of the line is the value
da = open('finalVTOmatrix.txt', 'r')
for line in da:
    line = line.strip()
    b = line.split('\t')
    a = line.partition('\t')
    if (b[3] =='0') or (b[3] =='0&1') or (b[4] =='0') or(b[4] =='0&1'):
        a1 = a[0].replace('_', ' ')
        a1 = a1.strip('\"')

        if (b[3] == '0') or (b[3] == '0&1'):
            peclosslist.append(a1)
            pec[a1]=b[3]
            if b[5] =='1':
                pecprop.append(a1)

        if (b[4] == '0') or (b[4] == '0&1'):
            pellosslist.append(a1)
            pel[a1] = b[4]
            if b[6] == '1':
                pelprop.append(a1)





    if a[0] !='taxa_name':
        a1= a[0].replace('_',' ')
        a1= a1.strip('\"')
        vtlist.append(a1)
        vtdic[a1]=a[2]


print 'the number of VTO data matrix taxa:',len(vtlist)


####################################################################################################################################
# defining a list to store VTO names with ncbi ids that is matching in OT
vtwitncid =[]
# defining the list to store VTO taxa that match by name and another list for name mismatches
otmatched =[]
otmismatched =[]
## checking the VTO list taxa has ncbi id and in OT

for i in vtlist:

    if i in vtncbi:

        nc1 =vtncbi[i]
        if nc1 in otncbir:
            vtwitncid.append(i)
            nm1 =otncbir[nc1]
            matchnames[i]=nm1
            #reversed dic : key is open tree name
            matchnamesr[nm1]=i
    else:
        vtwitnc.append(i)

#if it does not have ncbi id append to another list and check wether they have the name in open tree
for i in vtwitnc:
    if i in oid:
        matchnames[i]=i
        matchnamesr[i]=i







################################################################################################################################################
### matching with the final tree list
otlist=[]
ot = open('all_tips.txt', 'r')
for line in ot:
    a1 = line.strip()
    otlist.append(a1)


# checking the taxa that is not matching by name but that has ncbi ids
for i in vtlist:
    if i in otlist:
        otmatched.append(i)
    else:
        otmismatched.append(i)

matched = matchnames.keys()

mismatched = set(vtlist) - set(matched)


matchedvals = matchnames.values()

print 'VTO name count without ncbi ID:', len(vtwitnc)
print 'mapped count from VTO to OT conversion (using database):', len(matchnames)
print 'final mismatched list (database comparison): ', len(mismatched)

# getting the initial database vs tree file mismatched
fmismatch = set(matchedvals) - set(otlist)

# print fmismatch

## the below code was required because there are name changes between OT data file and OT tree file
# checkout Danio rerio for more information in the OT data file and the tips list
## so this is the second round of matched dic replacement
print 'initial mismatch count between database and the final tree file', len(fmismatch)
for i in fmismatch:
    k = matchnamesr[i]

    if k in otlist:
        del matchnamesr[i]
        # print k
        matchnames[k] = k
        matchnamesr[k] = k


        # print mismatched
        # print vtwitnc
# the intersection of name mismatches with ncbi id has ones
contranames = set(otmismatched) & set(vtwitncid)

### generating second round statistics##############
matchedot1 =matchnamesr.keys()
ffmismatch = set(matchedot1)- set(otlist)
print 'Final mismatch count between database and the final tree file',len(ffmismatch)
print len(fmismatch)-len(ffmismatch), 'mismatches were solved by second round'



#################### generating the final open tree matrix####################################################################################

out1 = open('finalfullopentree_matrix.txt', 'wb+')
out2 = open('finalopentree_matrix_onlydata.txt', 'wb+')

out1.write('taxa_name\tpectoral_fin\tpelvic_fin\tpectoral_inferred\tpelvic_inferred\tpectoral_propagated\tpelvic_propagated\n')
out2.write('taxa_name\tpectoral_fin\tpelvic_fin\tpectoral_inferred\tpelvic_inferred\tpectoral_propagated\tpelvic_propagated\n')
# read the opentree tips list if the taxa is in the mapped dictionary
#   get the data from the vtodic and print it out, else: print question marks
matchedots =[]
matchedvts =[]

for i in otlist:
    if i in matchnamesr:
        matchedots.append(i)
        a = matchnamesr[i]
        matchedvts.append(a)
        out1.write('%s\t%s\n'%(i,vtdic[a]))
        out2.write('%s\t%s\n' % (i, vtdic[a]))
    else:

        out1.write('%s\t?\t?\t?\t?\t?\t?\n'%(i))


print 'matched count of OT ids: ', len(matchedots)
print 'matched count of VTO ids: ', len(matchedvts)
mismatchedvts = set(vtlist) - set(matchedvts)
mismatchedvts=list(mismatchedvts)
print 'final mismatched count in VTO', len(vtlist)-len(matchedvts)
print 'final mismatched count in VTO', len(mismatchedvts)



################################################################################################################################################
# there are repeated entries in opentree mappings. The below code snippet is used to print them out
# print len(matchnamesr)
# print len(matchnames)
# print len(matchedvals)
# print len(set(matchedvals))

# opt = [item for item in set(matchedvals) if matchedvals.count(item) > 1]
# for i in opt:
#     print i,otncbi[i]

################################################################################################################################################
# seperating the mismatched VTO list

spmismatches =[]

#Detecting extinct taxa

extinctmismatches = set(mismatchedvts)& set(extinct)
ermismatchedvts = set(mismatchedvts) - extinctmismatches

#detecting sp.
#
for i in ermismatchedvts:
    if ('sp.'in i) or ('cf.'in i) or ('Species'in i) or ('Genus'in i):
        spmismatches.append(i)

finalmismatchedvts = ermismatchedvts - set(spmismatches)




################################################################################################################################################
## printing the mismatched list
out = open('finalmismatchedlist_andstats.txt', 'wb+')
out.write('VTO data matrix taxa count:%s\n'%(len(vtlist)))
out.write('Open tree file taxa count:%s\n'%(len(otlist)))


out.write('\n')
out.write('The number of VTO taxa that is mismatched with OT tree file:%s\n'%(len(mismatchedvts)))
out.write('The number of VTO taxa that is matched with OT tree file:%s\n'%(len(matchedvts)))
out.write('\n')

out.write('####################################################################################\n')

out.write('####################################################################################\n')
out.write('The number of mismatched taxa that is extinct:%s\n'%(len(extinctmismatches)))
for i in extinctmismatches:
    out.write('%s\n'%(i))

out.write('\n')
out.write('\n')

out.write('The number of mismatched taxa that has sp. in name (improper naming):%s\n'%(len(spmismatches)))
for i in spmismatches:
    out.write('%s\n'%(i))

out.write('\n')
out.write('\n')

out.write('The remaining mismatches list:%s\n'%(len(finalmismatchedvts)))
for i in finalmismatchedvts:
    out.write('%s\n'%(i))

out.write('\n')
out.write('\n')

out.write('out of the remaining mismatched taxa There are %s VTOtaxa that is in the Open tree Database but they were not in the final open tree file\n'%(len(ffmismatch)))
out.write('VTO_name\tOTname\n')
for i in ffmismatch:

    out.write('%s\t%s\n'%(matchnamesr[i],i))
out.write('\n')
out.write('\n')
# out.write('There are %s VTOtaxa that is not matched in Open tree Database\n'%(len(mismatched)))
# out.write('\n')
# for i in mismatched:
#     out.write('%s\n'%(i))
out.write('####################################################################################\n')
out.write('the mismatched taxa with finloss\n')
out.write('\n')

pecpropmismatchloss = set(peclosslist)&set(mismatchedvts)&set(pecprop)
pelpropmismatchloss = set(pellosslist)&set(mismatchedvts)&set(pelprop)
pecunpropmismatchloss = (set(peclosslist)&set(mismatchedvts))-set(pecprop)
pelunpropmismatchloss = (set(pellosslist)&set(mismatchedvts))-set(pelprop)

out.write('the mismatched taxa pectoral fin propagated with finloss: %s\n'%(len(pecpropmismatchloss)))
for i in pecpropmismatchloss:
    out.write('%s\t%s\n' % (i,pec[i]))
out.write('\n')

out.write('the mismatched taxa pectoral fin unpropagated with finloss: %s\n'%(len(pecunpropmismatchloss)))
for i in pecunpropmismatchloss:
    out.write('%s\t%s\n' % (i,pec[i]))
out.write('\n')

out.write('the mismatched taxa pelvic fin propagated with finloss: %s\n'%(len(pelpropmismatchloss)))
for i in pelpropmismatchloss:
    out.write('%s\t%s\n' % (i,pel[i]))
out.write('\n')

out.write('the mismatched taxa pelvic fin unpropagated with finloss: %s\n'%(len(pelunpropmismatchloss)))
for i in pelunpropmismatchloss:
    out.write('%s\t%s\n' % (i,pel[i]))
out.write('\n')


out.write('####################################################################################\n')
out.write('There are %s that that match by only NCBI ids \n'%(len(vtwitncid)))
out.write('There are %s that that is mismatched by only NCBI ids \n'%(len(vtlist)-len(vtwitncid)))
out.write('\n')
out.write('\n')
out.write('There are %s that that match by only names \n'%(len(otmatched)))
out.write('There are %s that that is mismatched by only names \n'%(len(otmismatched)))
out.write('There are %s that do not match by name but are matching by NCBI ids \n'%(len(contranames)))
out.write('\n')
out.write('VTO_name\tOTname\n')
for i in contranames:
    out.write('%s\t%s\n' % (i,matchnames[i]))

################################################################################################################################################
out4 = open('finalmatchedvtlist.txt', 'wb+')

for i in matchedvts:
    out4.write('%s\n'%(i))

