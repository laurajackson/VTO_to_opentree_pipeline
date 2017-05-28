# author Pasan Fernando
# Date 07/20/2016
# This code adds a new column to the final opentreematrix by analyzing the loss or presence of paired fin data (together as combination)
# it introduces 4 states for the different combinations
# This code is not part of the generic pipeline.
# It was only used because we want to study the evolution of both pectoral and pelvic fins together as paired fin
__author__ = 'pasan fernando'

################################################################################
import re
import collections

par ={}
paired ={}
both =[]
pec =[]
pel =[]
presence=[]
missing =[]

# opening the input matrix with open tree names
da = open('finalopentree_matrix_onlydata.txt', 'r')

for line in da:
    line = line.strip()
    if (line != '\n') and ('taxa_name' not in line):
        b = line.split('\t')
        a = line.partition('\t')
        #saving all partitions
        par[a[0]]=a[2]

        # combination for both absence : state '0'
        if ((b[3] =='0') or (b[3] =='0&1')) and ((b[4] =='0') or(b[4] =='0&1')):
            both.append(a[0])
            paired[a[0]]= '0'

        # combination for only pectoral fin absence: state '1'
        elif ((b[3] == '0') or (b[3] == '0&1')) and ((b[4] == '?') or (b[4] == '1') or (b[4] == '2')):
            pec.append(a[0])
            paired[a[0]] = '1'

        # combination for only pelvic fin absence: state '2'
        elif ((b[4] == '0') or (b[4] == '0&1')) and ((b[3] == '?') or (b[3] == '1') or (b[3] == '2')):
            pel.append(a[0])
            paired[a[0]] = '2'

        # there can be double missing ones (detect them or exclude them)
        elif (b[3] == '?') and (b[4] == '?'):
            missing.append(a[0])
            paired[a[0]] = '?'

        # combination for no absences (only presence): state '1'
        else:
            paired[a[0]]='3'
            presence.append(a[0])
print par
print len(par)

# defining the output file
out1 = open('Teleostei_presence_absence_pipeline_output.txt', 'wb+')

# writing the header
out1.write('taxa_name\tpectoral_fin\tpelvic_fin\tpectoral_inferred\tpelvic_inferred\tpectoral_propagated\tpelvic_propagated\tpaired_fin\n')

for i in par:
    out1.write('%s\t%s\t%s\n' % (i, par[i],paired[i]))

print both
print len(both)

# writing the statistics of paired fin analysis in the paired_fin_analysis_stats file

out2 = open('paired_fin_analysis_stats.txt', 'wb+')
out2.write('The total taxa in the matrix: %s\n'%(len(par)))
out2.write('Here are the statistics for the paired fin analyses\n')
out2.write('\n')
out2.write('The number for both fins absent (state 0): %s\n'%(len(both)))
out2.write('The number for only pectoral fin absent (state 1): %s\n'%(len(pec)))
out2.write('The number for only pelvic fin absent (state 2): %s\n'%(len(pel)))
out2.write('The number for no absences (state 3): %s\n'%(len(presence)))
out2.write('The number for both missing taxa: %s\n'%(len(missing)))

        # if (b[3] =='0') or (b[3] =='0&1') or (b[4] =='0') or(b[4] =='0&1'):
        #     a1 = a[0].replace('_', ' ')
        #     a1 = a1.strip('\"')
        #
        #     if (b[3] == '0') or (b[3] == '0&1'):
        #         peclosslist.append(a1)
        #         pec[a1]=b[3]
        #         if b[5] =='1':
        #             pecprop.append(a1)
        #
        #     if (b[4] == '0') or (b[4] == '0&1'):
        #         pellosslist.append(a1)
        #         pel[a1] = b[4]
        #         if b[6] == '1':
        #         pelprop.append(a1)


