# VTO_to_opentree_pipeline
https://zenodo.org/badge/64852544.svg

The pipeline that converts ontotrace matrix to a matrix that can be mapped to a open tree phylogeny

This file gives information about the different codes in the open tree pipeline

The pipeline is used to convert an ontotrace data matrix (which has VTO taxa) into open tree format, so it can be mapped to open tree file.

The input to the pipeline is a nexml file that contains data for pectoral and pelvic fins. This file was downloaded from ontotrace web interface in phenoscape knowledgebase. This pipeline also needs a meta data files in xml formart for pectoral and pelvic fin, which can be requested from the phenoscape team. The taxonomic reconciliation step requires the open tree phylogeny downloaded from open tree. It requires list of open tree taxa.

The description of the codes is given below.

## 1. nexml_to_txt_converter.py

This code converts the nexml character matrix downloaded from ontotrace into a tab delimited format, which is suitable to proceed through the pipeline. It correctly identifies the conflict states and writes ‘0 and 1’ for them. It also detects empty cell with missing data and writes ‘?’ for those cells. This code works for any matrix with any number of characters downloaded from ontotrace in nexml format.

### input
the ontotrace matrix in nexml format (should be a .xml file)

### outputs

tabdelemited_charactermatrix.txt  : The nexml matrix converted into tab delemited format. This is the input for the next code


2.matrixpreprocessor.py

Takes the original tab delemited matrix file. 
prints all the taxa into a separate file
Also removes the missing taxa ( ones with two ? for both pelvic and pectoral fins) and prints the statistics

input
original trimmed input matrix
vtonewfinal.owl: VTO ontology file gives the relationships of VTO

outputs

missingremoved_matrix.txt: the matrix after the removal of missing taxa
originaldatamatrix_taxalist.txt: taxa list of the original matrix
alltaxa.txt: all taxa separated into levels
missingtaxa.txt: missing taxa separated into levels


3.conflict_state_remover.py: 
The second step of the pipeline is to remove polymorphic states (0&1) from the internal nodes of the data matrix. This code detects taxa with '0&1' and separates them according to taxa level. Prints the literature sources for each taxa, and this code also replaces the 0&1 of internal nodes by ‘?’.

input:
the xml files for fins: pectoral.xml or pelvic.xml (depending on which fin you want) 
missingremoved_matrix.txt: the original onto trace data matrix after the removal of missing taxa(without any processing)
Outputs:
intermediatecounts.txt: Contains the number of taxa that that has 0&1 states and their source paper where the data is coming from
intermediate_removed_datamatrix.txt: the data matrix where the 0&1 state of internal nodes are replaced by ‘?’. All the species level taxa still keep 0&1 states
 
4.inferredpresencereplace.py: 
This scripts detects the taxa with inferred presence and changes the state of the presence from ‘1’ to ‘2’. This new state is printed on new column. The original two columns for pelvic and pectoral fin will be kept without change.

input:	pectoralinferred.txt (the taxa list of inferred presence for pectoral fin)
	these files are coming after manually processing the asserted_inferredcount.py code output)
	pelvicinferred.txt (the taxa list of inferred presence for pelvic fin)
	conflicts_removed_datamatrix.txt (the input data matrix with 3 columns)
	
output: modified_inferredadded_matrix.txt ( the modified data matrix with two new 		columns for inferred presence state replacement)
inferredstats: Prints the statistics for the number of inferred presence taxa that is transferred
It will print out the taxa that was failed to be matched (due to name errors) find them and manually change the output matrix

5.propagation.py:
 This scripts propagates data of internal nodes to their species. If the species already have data for a specific internal node that data will be kept. All the other species without data will be added to data file. For now, the propagation only considers internal taxa up to family level. Two original columns will be updated to only contain propagated states.

input:	modified_inferredadded_matrix.txt (the input data matrix with 5 columns)
	vtonewfinal.owl(VTO ontology data file; the syntax for one species was 		problematic in the direct download. This was changed in this file.
	
output: finalVTOmatrix.txt (the final matrix with 7 columns: two new columns were added to indicate whether the species is propagated or not; ‘1’:propagated, 0: not propagated)
	propagationstatistics.txt (gives statistics about the original data file, propagation step and the new data matrix. It also gives the counts of propagated taxa for families and genera separately)
	finalVTOspecieslist.txt (list of species in the finalVTOmatrix. can be used for comparison purposes)
famlilyand_genera_propahated.txt  statistics for families and genera that propagated data

6.taxonomic_reconcilliation.py: 
This script is used to convert the VTO data matrix into open tree version.
It will use combined approach that includes name conversion using NCBI ids and direct name matching.
The script can also generate statistics for the final conversion.

Inputs

finalVTOmatrix.txt: this is the final propagated matrix and has VTO taxa
all_tips.txt: A list of all tips (species from final open tree file. We need to get this as a list)
taxonomy.tsv: The data file downloaded from open tree database (contains all the information about all the taxa in open tree. Used to extract NCBI ids)
vtonewfinal.owl: The VTO ontology file

Outputs
finalfullopentree_matrix.txt: The final matrix. Contains open tree taxa. Ready for the mapping. This file contains all the open tree taxa that is in the tree file. Even the ones without data.
finalopentree_matrix_onlydata.txt: This final matrix contains only the taxa with data. It can be used for the mapping as well

finalmismatchedlist_andstats.txt: This file contains all the statistics about matching and mismatching taxa. Also prints out the mismatching taxa and counts how many extinct and sp. (inaccurate) names are there in the final mismatched taxa list.


paired_fin_analyzer.py: 

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

Teleostei_presence_absence_pipeline_output.txt: This is the final matrix with open tree names that should be used for the visualization. Contains a new column (7th column) for the paired fin data analysis (the original two columns will be removed)

paired_fin_analysis_stats.txt: The statistics for paired fin analysis



