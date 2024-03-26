#code form https://www.geeksforgeeks.org/convert-excel-to-csv-in-python/
import pandas as pd 
from tqdm import tqdm

with open("4_Utilitise/xlsxToConvert.txt", "r") as file_xlsxToConvert:
    xlsxToConvert = file_xlsxToConvert.read()

for file in tqdm(xlsxToConvert.split("\n")):
    read_file = pd.read_excel (file + ".xlsx") 
      
    read_file.to_csv (file +".csv", index = None, header=True) 
        