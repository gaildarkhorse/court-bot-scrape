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
import phonenumbers

path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

class decedent:
    def __init__(self):
    # sef information
        self.docketInfo = ''
        self.nameInfo = ''
        self.addrInfo = ''
        self.extraInfo = ''
        self.phoneInfo = ''
        self.emailInfo = ''
    # get information
        # base information
        self.key = ''
        self.namePulled = ''
        self.probateCounty = ''
        self.probateState = ''
        self.docketNumber = ''
        self.probateDate = ''
        self.dateOfDeath = ''
        # name information
        self.decdPreffix = ''
        self.firstName = ''
        self.middleName = ''
        self.lastName = ''
        self.suffix = ''
        # Address information
        self.lastAddress = ''
        self.lastCity = ''
        self.lastState = ''
        self.lastZip = ''
    def set_docketInfo(self, _docketInfo):
        self.docketInfo = _docketInfo
        ###

    def set_nameInfo(self, _nameInfo):
        self.nameInfo = _nameInfo
        ###
        splitedName = _nameInfo.split(' ')
        if len(splitedName) == 3:
            self.firstName = splitedName[0]
            self.middleName = splitedName[1][0]
            self.lastName = splitedName[2]
        if len(splitedName) == 4:
            self.firstName = splitedName[0]
            self.middleName = splitedName[1][0]
            self.lastName = splitedName[2]
            self.suffix = splitedName[3]

    def set_addrInfo(self, _addrInfo):
        self.addrInfo = _addrInfo
        splited_addr = _addrInfo.split(' ')
        add_len = len(splited_addr)
        last_string = splited_addr[len - 1]
        first_string = splited_addr[2]
        if self.isDigit(last_string) == True:
            self.lastZip = last_string
            self.lastState = splited_addr[add_len - 2]
            self.lastCity = splited_addr[add_len - 3]
            if self.isDigit(first_string) == True:
                self.lastAddress = splited_addr[2] + " " + splited_addr[3] + " " + splited_addr[4]
        else: 
            self.lastState = splited_addr[add_len - 1]
            self.lastCity = splited_addr[add_len - 2]
            if self.isDigit(first_string) == True:
                self.lastAddress = splited_addr[2] + " " + splited_addr[3] + " " + splited_addr[4]
        ###
    def set_extraInfo(self, _extraInfo):
        self.extraInfo = _extraInfo
        split_info = _extraInfo.split(' ')
        if len(split_info) > 6:
            self.lastState = split_info[6]
            self.lastCity = split_info[5]
        ###
    def set_phoneInfo(self, _phoneInfo):
        self.phoneInfo = _phoneInfo
        pattern = r"\d"
        # Find all matches of the pattern in the string
        matches = re.findall(pattern, _phoneInfo)
        # Join the matches into a single string
        digits = ''.join(matches)
        parsed_number = phonenumbers.parse(digits, "US")
        # Format the parsed number as a telephone number
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        ###
    def set_phoneInfo(self, _emailInfo):
        self.emailInfo = _emailInfo    
    def isDigit(self, _str):
        pattern = r"\d+"
        # Find all matches of the pattern in the string 
        matches = re.findall(pattern, _str)
        if matches:
            digits = [int(match) for match in matches]
            return False
        else:
            return True


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
    #print(lined_text0)
    lined_text1 = []
    decedent_start_index = -1
    petitioner_start_index = -1
    petitioner_end_index = -1
    decedent_name_line = ''
    # divide into {decedent, petitioner}:
    
    for index in range(len(lined_text0)):
        if 'Information about the Decedent:' in lined_text0[index]:
           decedent_start_index = index
           continue
        if 'Information about the Petitioner:' in lined_text0[index]:
           petitioner_start_index = index
           continue
        if '3.' in lined_text0[index]:
           petitioner_last_index = index
           break
    
    probate_county =''
    decedent_suffix = ''
    decedent_ageAtDeath = 0
    decedent_street_addr =''
    decedent_city = ''
    decedent_state = ''
    decedent_zip_code = ''
    decedent_address_info = ''
    decedent_domiciled_in = ''

    if decedent_start_index > 0:
       if petitioner_start_index > 0:
            for index in range(decedent_start_index):
                if 'Division' in lined_text0[index]:
                    pattern = r"(\w+)\s+Division"
                    string = lined_text0[index]
                    print(">>>>>", string)
                    # Search for the pattern in the string
                    match = re.search(pattern, string)
                    if match:
                        probate_county = match.group(1)
                        print(probate_county)
                break

            for index in range(decedent_start_index, petitioner_start_index):
                if 'Name:' in lined_text0[index]:
                    decedent_name_line = lined_text0[index]
                    ### get some infromation from decedent_name_line
                    #print(decedent_name_line)
                    continue
                    continue
                if 'Domicile at death:' in lined_text0[index]:
                    decedent_address_info = lined_text0[index]
                    #print(">>> decedent address info >>> ", decedent_address_info)
                    # TODO : add some function to get detailed information from decendent_address_info
                    continue
                if 'Street Address:' in lined_text0[index]:
                    decedent_address_info = lined_text0[index]
                    #print(decedent_address_info)
                    continue
                if 'The Decedent was domiciled in' in lined_text0[index]:
                    decedent_domiciled_in = lined_text0[index]
                    print(decedent_domiciled_in)
                    continue
            


    return sift_text


entries = load_pdf_list('./')
#print(entries)
for index in entries:
    convert_pdf2img(index)
_text = text_from_image('2-1.png')


