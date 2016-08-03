# VTO_to_opentree_pipeline
The pipeline that converts ontotrace to open tree matrix

The open tree pipeline

This file gives information about the different codes in the open tree pipeline

The pipeline is used to convert an ontotrace data matrix (which has VTO taxa) into open tree format, so it can be mapped to open tree file.

The input to the pipeline is the tab delimited data file that contains data for pectoral and pelvic fins.

The description of the codes is given below.

1. intermediate_state_remover.py: The first step of the pipeline is to remove polymorphic states (0&1) from the internal nodes of the data matrix. This code detects taxa with '0&1' and separates them according to taxa level. Prints the literature sources for each taxa, and this code also replaces the 0&1 of internal nodes by ‘?’.
input:
the data file: pectoral.xml or pelvic.xml (depending on which fin you want) 
Final_dataONLY_6.6.16.txt: the original onto trace data matrix (without any processing)

Outputs:
intermediatecounts.txt: Contains the number of taxa that that has 0&1 states and their source paper where the data is coming from
intermediate_removed_datamatrix.txt: the data matrix where the 0&1 state of internal nodes are replaced by ‘?’. All the species level taxa still keep 0&1 states
 
2. inferredpresencereplace.py: This scripts detects the taxa with inferred presence and changes the state of the presence from ‘1’ to ‘2’. This new state is printed on new column. The original two columns for pelvic and pectoral fin will be kept without change.

input:	pectoralinferred.txt (the taxa list of inferred presence for pectoral fin)
	pelvicinferred.txt (the taxa list of inferred presence for pelvic fin)
	intermediate_removed_datamatrix.txt (the input data matrix with 3 columns)
	
output: modified_inferredadded_matrix.txt ( the modified data matrix with two new 		columns for inferred presence state replacement)
inferredstats: Prints the statistics for the number of inferred presence taxa that is transferred

3. propagation.py: This scripts propagates data of internal nodes to their species. If the species already have data for a specific internal node that data will be kept. All the other species without data will be added to data file. For now, the propagation only considers internal taxa up to family level.

input:	modified_inferredadded_matrix.txt (the input data matrix with 5 columns)
	vtonewfinal.owl(VTO ontology data file; the syntax for one species was 		problematic in the direct download. This was changed in this file.
	
output: finalVTOmatrix.txt (the final matrix with 7 columns: two new columns were added to indicate whether the species is propagated or not; ‘1’:propagated, 0: not propagated)
	propagationstatistics.txt (gives statistics about the original data file, propagation step and the new data matrix. It also gives the counts of propagated taxa for families and genera separately)
	finalVTOspecieslist.txt (list of species in the finalVTOmatrix. can be used for comparison purposes)

4. OTnaming_pipeline.py: 
This script is used to convert the VTO data matrix into open tree version.
It will use combined approach that includes name conversion using NCBI ids and direct name matching.
The script can also generate statistics for the final conversion.

Inputs

finalVTOmatrix.txt: this is the final propagated matrix and has VTO taxa
all_tips.txt: A list of all tips (species from final open tree file)
taxonomy.tsv: The data file downloaded from open tree database (contains all the information about all the taxa in open tree. Used to extract NCBI ids)
vtonewfinal.owl: The VTO ontology file

Outputs
finalfullopentree_matrix.txt: The final matrix. Contains open tree taxa. Ready for the mapping. This file contains all the open tree taxa that is in the tree file. Even the ones without data.
finalopentree_matrix_onlydata.txt: This final matrix contains only the taxa with data. It can be used for the mapping as well

finalmismatchedlist_andstats.txt: This file contains all the statistics about matching and mismatching taxa. Also prints out the mismatching taxa and counts how many extinct and sp. (inaccurate) names are there in the final mismatched taxa list.






Before propagation and after extra mapping step script

bpmatrix_generation.py
# Generating the before propagation matrix.
# Do not distinguish between '0' and '1' state, only inferred vs assereted state

inputs
finalVTOmatrix.txt
all_tips
taxonomy.tsv
vtonewfinal.owl


outputs
beforepropagatedstatistics.txt: The statistics before the propagation. This contains data for number of inferred vs asserted. Also some statistcs are there for the cell count of how many '0' s '1' s and '0&1' s etc. It gives number of matched taxa for each subgroup as well.

beforepropagatedmatrix1.txt: This matrix is generated before the propagation step. It distinguishes the inferred vs asserted taxa. asserted (1); inferred (2)

The two outputput files given below prints the list of mismatched taxa separated into different levels
beforepropagatedpectoralmismatchedlists.txt
beforepropagatedpelvicmismatchedlists.txt

propagated_matrix_generation.py

# Generating the after propagation matrix during the xtra mapping step
# Prints different state numbers for different combinations like 'inferred propagated, asserted propagated etc.

inputs
finalVTOmatrix.txt
all_tips
taxonomy.tsv
vtonewfinal.owl


outputs
propagatedmatrix3.txt: This matrix contains different states for different combinations such as inferred propagated, asserted unpropagated etc. The state key is given below; asserted un-propagated (1); inferred un-propagated (2); asserted propagated (3); inferred propagated (4)

propagatedstatistics.txt
Contains statistics after the propagation. Has numbers for different combinations like inferred propagated, asserted propagated, etc. Also contains the matched number of taxa

Some general purpose scripts that can be used (that are related to pipeline)


vtotolcompare_combinedmethod.py
This scripts compares the taxa list from data file (with extinct and sp. taxa) with taxa from the open tree file (only contain the tips). This is the new comparison which uses the 3 mapping methods
 
input:	all_tips.txt (taxa list from open tree)
	originaldatamatrix_taxalist.txt (unprocessed data matrix taxa)
output: beforepropagation_name_mismatched_taxalist.txt: the mismatched taxalist generated as a result of mapped by name method
	beforepropagation_mismatchedlist_andstats.txt: contains all the statistics of mismatched taxa (extinct, with sp. etc.)
	beforepropagation_mismatched_taxalist.txt: the mismatched taxa list generated as a result of combined method


sp_remover.py: This scripts removes the taxa names with “sp.” in the taxa list from the data file
input:	any user given list of taxa
output: 'spremoved_list.txt' (data file taxa with sp. Removed) 

extincttaxa_detector.py: 
This scripts removes the extinct taxa from the taxa names of the ontotrace data file

input: Taxa_in_datafile.txt (list of taxa in data file)
	vtonew.owl: The VTO datafile (the new version  7/4/16)


Output: extincttaxa.txt (lists the extinct taxa extracted from the list)
	extinctremoved_datafiletaxa.txt (this is the new data file taxa list without 
	any extinct taxa)


ott_remover.py:

This scripts removes ‘ott’ from the raw open tree file names

input: raw input tree downloaded from open tree (in .tre or newick format)
output: ottremoved.tre: ( the tree with ott code removed names)
