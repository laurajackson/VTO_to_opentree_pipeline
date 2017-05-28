Takes the tab delemited matrix that is converted from nexml format. 
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


