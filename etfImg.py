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


# Defining paths to tesseract.exe 
# and the image we would be using 
path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
print(">>> loading pdf file")

images = convert_from_path('3.pdf')

images[0].save('temp' +'.png', 'png')
#image_path = r"csv\sample_text.jpg"
print(">>> convet to image from pdf file")
print(">>>conversion succeed")

# Opening the image & storing it in an image object 
img = Image.open('page0.png') 


print(">>>image information:",  img)
#img.show()

print("extract text from image >>>")
text = pytesseract.image_to_string(img)
split_text = text.split("\n")
cleaned_text = " ".join(split_text)
print(cleaned_text)
lined_text = cleaned_text.split(" ")
new_lined_text = []

print(len(lined_text))
space = ''
for item in lined_text:
  if(item == space):
      continue
  else:
      new_lined_text.append(item)


#match = re.search(r'\W(', '(fdsfe)fadf')
#print(match)
#print(new_lined_text)
#print(len(new_lined_text))

workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()


pre_lined_text = new_lined_text
dc_zip_code = str(1571)

idx = 0
for item in new_lined_text:
   worksheet.write(0, idx, item)
   idx += 1

workbook.close()

file = open('result.txt', 'w+')

line_land = []
for item in pre_lined_text:
  if item.find('(') == -1:
    if item.find(')') == -1:
      file.write(item)
      file.write("\n")
      lined_text.append(item)
      
file.close()



index_1 = new_lined_text.index('1.')
index_2 = new_lined_text.index('2.')
index_3 = new_lined_text.index('3.')

sift_text = []
dc_key = []
dc_name_pulled = []
dc_number = []
dc_probate_date = []
dc_dod = []
dc_prefix = []
dc_suffix = []

dc_county_index =  new_lined_text.index('Division') - 1

for index in range(index_1, index_2):
   if new_lined_text[index] == 'Name:':
      dc_name_index = index + 1
      continue
   if 'Age' in new_lined_text[index]:
      dc_Age_start_index = index
      continue
   if 'death' in new_lined_text[index]:
      if index < dc_Age_start_index + 3:
         dc_Death_index = index
         continue
   if 'Address:' in new_lined_text[index]:
      dc_address_index = index + 1
      continue
   if dc_zip_code in new_lined_text[index]:
      dc_zip_code_index = index
      continue
   if 'domiciled' in new_lined_text[index]:
      dc_last_address_index = index + 1
      dc_last_state_index = index + 2
      break




dc_county = new_lined_text[dc_county_index]
dc_first_name = new_lined_text[dc_name_index]
dc_middle_name = ''
dc_last_name = ''

if dc_Age_start_index - dc_name_index == 3:
   dc_middle_name = new_lined_text[dc_name_index + 1]
   dc_last_name = new_lined_text[dc_name_index + 2]
if dc_Age_start_index - dc_name_index == 2:
   dc_middle_name = ' '
   dc_last_name = new_lined_text[dc_address_index + 1]

dc_probate_state = new_lined_text[dc_zip_code_index - 1]
dc_state = dc_zip_code_index - 1
dc_town = dc_zip_code_index - 2
dc_last_address = new_lined_text[dc_address_index] + " " + new_lined_text[dc_address_index + 1] + " " + new_lined_text[dc_address_index + 2] 
dc_last_city = new_lined_text[dc_last_address_index + 1]
dc_last_state = new_lined_text[dc_last_address_index + 2]

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
   if new_lined_text[index] == 'Name:':
      pr_name_index = index + 1
      continue
   if 'First' in new_lined_text[index]:
      pr_first_index = index
   if 'Last' in new_lined_text[index]:
      pr_address_index = index + 2
      continue
   if 'Mailing' in new_lined_text[index]:
      pr_zip_code_index = index - 1
      continue
   if 'different:' in new_lined_text[index]:
      pr_mailing_address_index = index
      continue
   if 'Primary' in new_lined_text[index]:
      pr_primary_index = index
      continue
   if '#:' in new_lined_text[index]:
      sharp_index = index
      continue
   if 'Email:' in new_lined_text[index]:
      pr_Email_index = index
      continue
   if '@'  in new_lined_text[index]:
      pr_monkey_symbol_index = index
      break

pr_prefix = ''
pr_first_name = new_lined_text[pr_name_index]
pr_middle_name = ''
pr_last_name = ''

if pr_first_index - pr_name_index == 3:
   pr_middle_name = new_lined_text[pr_name_index + 1]
   pr_last_name = new_lined_text[pr_name_index + 2]
if pr_first_index - pr_name_index == 2:
   pr_middle_name = ' '
   pr_last_name = new_lined_text[pr_name_index + 1]

pr_suffix = ''

pr_address = new_lined_text[pr_address_index] + " " + new_lined_text[pr_address_index + 1] + " " + new_lined_text[pr_address_index + 2]
pr_city = new_lined_text[pr_zip_code_index - 2]
pr_state = new_lined_text[pr_zip_code_index - 1]
pr_phone = new_lined_text[sharp_index + 1]
pr_Email = new_lined_text[pr_monkey_symbol_index]

sift_text.append(pr_prefix)
sift_text.append(pr_first_name)
sift_text.append(pr_middle_name)
sift_text.append(pr_last_name)
sift_text.append(pr_suffix)
sift_text.append(pr_address)
sift_text.append(pr_city)
sift_text.append(pr_state)
sift_text.append(pr_phone)
sift_text.append(pr_Email)

print(sift_text)






