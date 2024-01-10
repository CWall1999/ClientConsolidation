# ClientConsolidation
Python program that reads a csv of family data from a Microsoft Access query and outputs a list of clients available for room consolidation.  

For use:  
Step 1: Open migrant shelter database  
Step 2: Run R-0QryInputRoster BU 20231002  
Step 3: Export the data to a csv file.  
  note: it is important to save the data as a csv file for successful import into the program  
Step 4: Run elligableFamilies.py  
  note: it will prompt you to select a file, make sure to select the csv file that you saved.  

Known cases where things break:  
  If you have one of the output files(SingleFathers.csv, SingleMomDaughter.csv, SingleMomSon.csv) open python will throw an error because it does not have permission to edit the active file  
  Families that have a / in their room number. This is not a major issue since these clients have large family units that have already been split between two rooms thus not elligable for consolidation  
  
