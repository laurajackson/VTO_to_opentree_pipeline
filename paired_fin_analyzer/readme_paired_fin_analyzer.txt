 This code adds a new column to the final opentreematrix by analyzing the loss or presence of paired fin data (together as combination)
it introduces 4 states for the different combinations

This code is not part of the generic pipeline. It was only used because we want to study the evolution of both pectoral and pelvic fins together as paired fin

The states for different combinations are given below

Combinations
State 0 BOTH ABSENT
0 and 0
0&1 and 0
0 and 0&1

State 1 PECTORAL ABSENT
0 and ?
0&1 and ?
0 and 1
0 and 2
0&1 and 1
0&1 and 2

State 2 PELVIC ABSENT
? and 0
? and 0&1
1 and 0
1 and 0&1
2 and 0
2 and 0&1

State 3 NO/UNKNOWN ABSENCE
1 and ?
2 and ?
? and 1
? and 2
1 and 1
1 and 2
2 and 1
2 and 2

input:finalopentree_matrix_onlydata.txt: the data matrix with 6 columns with open tree names( data is separated for different fins)

outputs

Teleostei_presence_absence_pipeline_output.txt: This is the final matrix with open tree names that should be used for the visualization. Contains a new column (7th column) for the paired fin data analysis

paired_fin_analysis_stats.txt: The statistics for paired fin analysis


