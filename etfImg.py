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

def text_from_image(img_path):
  img = Image.open(img_path) 
  text = pytesseract.image_to_string(img)
  split_text = text.split("\n")
  cleaned_text = " ".join(split_text)
  lined_text = cleaned_text.split(" ")
  temp_lined_text = []
  print(len(lined_text))
  space = ''
  for item in lined_text:
    if(item == space):
        continue
    else:
        temp_lined_text.append(item)
  dc_zip_code = str(1571)
  file = open('result.txt', 'w+')
  prepared_text = []
  for item in temp_lined_text:
    if item.find('(') == -1:
      if item.find(')') == -1:
        file.write(item)
        file.write("\n")
        prepared_text.append(item)
        
  file.close()
  index_1 = prepared_text.index('1.')
  index_2 = prepared_text.index('2.')
  index_3 = prepared_text.index('3.')
  sift_text = []
  dc_key = []
  dc_name_pulled = []
  dc_number = []
  dc_probate_date = []
  dc_dod = []
  dc_prefix = []
  dc_suffix = []

  dc_county_index =  prepared_text.index('Division') - 1

  for index in range(index_1, index_2):
    if prepared_text[index] == 'Name:':
        dc_name_index = index + 1
        continue
    if 'Age' in prepared_text[index]:
        dc_Age_start_index = index
        continue
    if 'death' in prepared_text[index]:
        if index < dc_Age_start_index + 3:
          dc_Death_index = index
          continue
    if 'Address:' in prepared_text[index]:
        dc_address_index = index + 1
        continue
    if dc_zip_code in prepared_text[index]:
        dc_zip_code_index = index
        continue
    if 'domiciled' in prepared_text[index]:
        dc_last_address_index = index + 1
        dc_last_state_index = index + 2
        break




  dc_county = prepared_text[dc_county_index]
  dc_first_name = prepared_text[dc_name_index]
  dc_middle_name = ''
  dc_last_name = ''

  if dc_Age_start_index - dc_name_index == 3:
    dc_middle_name = prepared_text[dc_name_index + 1]
    dc_last_name = prepared_text[dc_name_index + 2]
  if dc_Age_start_index - dc_name_index == 2:
    dc_middle_name = ' '
    dc_last_name = prepared_text[dc_address_index + 1]

  dc_probate_state = prepared_text[dc_zip_code_index - 1]
  dc_state = dc_zip_code_index - 1
  dc_town = dc_zip_code_index - 2
  dc_last_address = prepared_text[dc_address_index] + " " + prepared_text[dc_address_index + 1] + " " + prepared_text[dc_address_index + 2] 
  dc_last_city = prepared_text[dc_last_address_index + 1]
  dc_last_state = prepared_text[dc_last_address_index + 2]

  sift_text.append(dc_key)
  sift_text.append(dc_name_pulled)
  sift_text.append(dc_county)
  sift_text.append(dc_probate_state)
  sift_text.append(dc_number)
  sift_text.append(dc_probate_date)
  sift_text.append(dc_dod)
  sift_text.append(dc_prefix)
  sift_text.append(dc_first_name)
  sift_text.append(dc_middle_name)
  sift_text.append(dc_last_name)
  sift_text.append(dc_last_address)
  sift_text.append(dc_last_city)
  sift_text.append(dc_last_state)
  sift_text.append(dc_zip_code)


  pr_address_index = -1
  pr_primary_index = -1
  pr_mailing_address_index = -1
  pr_zip_code_index = -1
  pr_Email_index = -1
  pr_monkey_symbol_index = -1
  pr_Email_index = -1
  pr_monkey_symebol_index = -1

    
    

  for index in range(index_2, index_3):
    if prepared_text[index] == 'Name:':
        pr_name_index = index + 1
        continue
    if 'First' in prepared_text[index]:
        pr_first_index = index
    if 'Last' in prepared_text[index]:
        pr_address_index = index + 2
        continue
    if 'Mailing' in prepared_text[index]:
        pr_zip_code_index = index
        while prepared_text[pr_zip_code_index].isdigit() == False:
          pr_zip_code_index -= 1
        continue
    if 'different:' in prepared_text[index]:
        pr_mailing_address_index = index
        continue
    if 'Primary' in prepared_text[index]:
        pr_primary_index = index
        continue
    if '#:' in prepared_text[index]:
        sharp_index = index
        continue
    if 'Email:' in prepared_text[index]:
        pr_Email_index = index
        continue
    if '@'  in prepared_text[index]:
        pr_monkey_symbol_index = index
        break

  pr_prefix = ''
  pr_first_name = prepared_text[pr_name_index]
  pr_middle_name = ''
  pr_last_name = ''

  if pr_first_index - pr_name_index == 3:
    pr_middle_name = prepared_text[pr_name_index + 1]
    pr_last_name = prepared_text[pr_name_index + 2]
  if pr_first_index - pr_name_index == 2:
    pr_middle_name = ' '
    pr_last_name = prepared_text[pr_name_index + 1]

  pr_suffix = ''

  pr_address = prepared_text[pr_address_index] + " " + prepared_text[pr_address_index + 1] + " " + prepared_text[pr_address_index + 2]
  pr_city = prepared_text[pr_zip_code_index - 2]
  pr_state = prepared_text[pr_zip_code_index - 1]
  pr_zip_code = prepared_text[pr_zip_code_index]
  pr_phone = prepared_text[sharp_index + 1]
  pr_Email = prepared_text[pr_monkey_symbol_index]

  sift_text.append(pr_prefix)
  sift_text.append(pr_first_name)
  sift_text.append(pr_middle_name)
  sift_text.append(pr_last_name)
  sift_text.append(pr_suffix)
  sift_text.append(pr_address)
  sift_text.append(pr_city)
  sift_text.append(pr_state)
  sift_text.append(pr_zip_code)
  sift_text.append(pr_phone)
  sift_text.append(pr_Email)
  return sift_text


entries = load_pdf_list('./')
print(entries)
for index in entries:
    convert_pdf2img(index)


