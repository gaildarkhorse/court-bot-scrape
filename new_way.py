import os
import pytesseract
from PIL import Image 
from pytesseract import pytesseract 
from pdf2image import convert_from_path
import requests
from bs4 import BeautifulSoup
import mechanicalsoup
import re
import pandas as pd
import xlsxwriter
from pathlib import Path
import pathlib

path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


def load_pdf_list(dir_path):
  pdf_list = []
  entries = Path(dir_path)
  for entry in entries.iterdir():
    if pathlib.Path(entry).suffix == '.pdf':
       pdf_list.append(entry)
  return pdf_list

def convert_pdf2img(pdf_path):
   split_tup = os.path.splitext(pdf_path)
   file_name = split_tup[0]
   image_path = file_name + '.png'
   images = convert_from_path(pdf_path)
   images[0].save(image_path, 'png')

def send_data_to_xlsx(xlsx_path, datalist, col_pos):
  workbook = xlsxwriter.Workbook(xlsx_path)
  worksheet = workbook.add_worksheet()
  idx = 0
  for item in datalist:
    worksheet.write(col_pos, idx, item)
    idx += 1
  workbook.close() 

def get_all_img_files(img_dir_path):
    img_list =[]
    entries = Path(img_dir_path)
    for entry in entries.iterdir():
        if pathlib.Path(entry).suffix == '.png':
            img_list.append(entry)
        return img_list

def text_from_image(img_path):
    print(">>>>>>>>>>>> start")
    img = Image.open(img_path) 
    text = pytesseract.image_to_string(img)
    sift_text = []
    lined_text0 = text.split('\n')
    print(lined_text0)
    lined_text1 = []
    #for item in lined_text0:
       
    return sift_text


entries = load_pdf_list('./')
print(entries)
for index in entries:
    convert_pdf2img(index)
_text = text_from_image('2-1.png')
print(_text)

