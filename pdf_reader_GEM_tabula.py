import tabula
import cv2
import pytesseract
from pdf2image import convert_from_path
from transformers import pipeline
import pandas as pd

file_name = "GEMC.pdf"

df = tabula.read_pdf(file_name,  pages='all', lattice = True, multiple_tables= True, silent = True, guess=False)#, lattice = 'True', silent = True)#, output_format="dataframe", multiple_tables=True, lattice=True)
print(f"Found {len(df)} tables and saved the da")
pd.concat(df).to_csv("view.csv") #The data in the table are not in the same order as in the pdf. But relevant data are in the same rows. Kindly extract it as per needs.
#Check the screenshot and csv file sent in mail.
