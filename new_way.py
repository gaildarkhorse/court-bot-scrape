import os
import pytesseract
from PIL import Image 
from pytesseract import pytesseract 
from pdf2image import convert_from_path
import preprocess
import personType
import toExcel





def text_from_image(img_path):
    print(">>>>>>>>>>>> start")
    img = Image.open(img_path) 
    text = pytesseract.image_to_string(img)
    sift_text = []
    lined_text0 = text.split('\n')
    cleaned_text = " ".join(lined_text0)
    lined_text = cleaned_text.split(" ")
    temp_lined_text = []
    space = ''
    for item in lined_text:
        if(item == space):
            continue
        else:
            temp_lined_text.append(item)
    print(temp_lined_text)
    total_text = " ".join(temp_lined_text)
    print(total_text)
    #return total_text
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





entries = preprocess.load_pdf_list('./')
#print(entries)
for index in entries:
    preprocess.convert_pdf2img(index)
_text = text_from_image('3-1.png')
index1 = _text.find('Decedent:')
index2 = _text.find('Petitioner:')
print(index2)
index3 = _text.find('3.')
substring1 = _text[:index1]
substring2 = _text[index1 : index2]
substring3 = _text[index2 : index3]
print(">>>>>>>>>>>>>>", index1)
print(">>>>>>>>>>>>>>>>>", substring1)
print(">>>>>>>>>>>>>>", index2)
print(">>>>>>>>>>>>>>>>>", substring2)
print(">>>>>>>>>>>>>>", index3)
print(">>>>>>>>>>>>>>>>>", substring3)

print(_text)

city_pattern = r"\b[A-Za-z\s]+\b"
zip_pattern = r"\b\d{5}\b"

# Find the matches of the patterns in the string
city_match = re.search(city_pattern, _text)
zip_match = re.search(zip_pattern, _text)

if city_match:
    city = city_match.group()
    print("City:", city)
else:
    print("No city found.")

if zip_match:
    zip_code = zip_match.group()
    print("Zip code:", zip_code)
else:
    print("No zip code found.")

pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

# Find the first match of the pattern in the string
match = re.search(pattern, _text)

if match:
    email = match.group()
    print("Email found:", email)
else:
    print("No email found.")


name_pattern = r'Name: ([A-Za-z\s.]+)'  # Matches the full name
suffix_pattern = r',\s?([A-Za-z\s]+)'  # Matches the suffix
gender_pattern = r'(\b[A-Za-z]+\b)$'  # Matches the last word as the gender

# Find the matches of the patterns in the string
name_match = re.search(name_pattern, substring3)
suffix_match = re.search(suffix_pattern, substring3)
gender_match = re.search(gender_pattern, substring3)

if name_match:
    full_name = name_match.group(1)
    name_parts = full_name.split()
    
    first_name = name_parts[0]
    middle_name = name_parts[1] if len(name_parts) > 2 else ''
    last_name = name_parts[-1]
    
    print("First name:", first_name)
    print("Middle name:", middle_name)
    print("Last name:", last_name)
else:
    print("No name found.")

if suffix_match:
    suffix = suffix_match.group(1)
    print("Suffix:", suffix)
else:
    print("No suffix found.")

if gender_match:
    gender = gender_match.group(1)
    print("Gender:", gender)
else:
    print("No gender found.")