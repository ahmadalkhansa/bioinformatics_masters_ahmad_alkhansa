# parsing_fasta.py
# For this exercise the pseudo-code is required (in this same file) 
# Write a script that:
# a) Reads sprot_prot.fasta line by line
# b) Copies to a new file ONLY the record(s) that are not from Homo sapiens
# b) And prints their source organism and sequence lenght 
# Use separate functions for the input and the output

a)1.open the file in reading mode 
 2.read the file line by line using readline function
b)3.detect the line that contains '>' 
 4.if it is found that there is 'Homo sapiens' in the line 
 5.continue reading until the line that contain another '>'
 6.if the line that contain '>' does not have 'Homo sapiens'
 7.write lines to the new file until the line that contain '>' is reached
 8.Repeat from step 3
 9.After '>' find 'OS=' and print the element after it
 10.in the line below the line that contains '>' count 'G' 'C' 'A' 'T'
 11.stop at second '>'
 12. Repeat from step 9
