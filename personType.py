import re
import pathlib
import phonenumbers
import gender_guesser.detector as gender


class Person:
    def __init__(self, text):
    # sef information
        self.data = text
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
        self.phone= ''
        self.email = ''
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
        city_pattern = r"\b[A-Za-z\s]+\b"
        zip_pattern = r"\b\d{5}\b"
        state_pattern = r"\b[A-Za-z]{2}\b"
        street_pattern = r"\b\d+\s+[\w\s]+\b"

        city_match = re.search(city_pattern, _addrInfo)
        zip_match = re.search(zip_pattern, _addrInfo)
        state_match = re.search(state_pattern, _addrInfo)
        street_match = re.search(street_pattern, _addrInfo)

        if city_match:
            self.lastCity = city_match.group()
        else:
            print("No city found.")

        if zip_match:
            self.lastZip = zip_match.group()
        else:
            print("No zip code found.")
        
        if state_match:
            self.lastState = state_match.group()
        else:
            print("No city found.")

        if street_match:
            self.lastAddress = street_match.group()
        else:
            print("No zip code found.")
    
    def set_extraInfo(self, _extraInfo):
        self.extraInfo = _extraInfo
        state_pattern = r"\b[A-Za-z]{2}\b"
        city_pattern = r"\b[A-Za-z\s]+\b"
        city_match = re.search(city_pattern, _extraInfo)
        state_match = re.search(state_pattern, _extraInfo)
        
        ###
    def set_phoneInfo(self, _phoneInfo):
        self.phoneInfo = _phoneInfo
        pattern = r"\d"
        # Find all matches of the pattern in the string
        matches = re.findall(pattern, _phoneInfo)
        # Join the matches into a single string
        digits = ''.join(matches)
        if len(digits) == 10:
            phone_digits = digits[:10]
        elif len(digits) == 11:
            if digits[0] == '1':
                phone_digits = digits[1:11]
            else:
                phone_digits = digits[0:10]
        else:
            phone_digits = digits
        parsed_number = phonenumbers.parse(phone_digits, "US")
        # Format the parsed number as a telephone number
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        self.phone = formatted_number
        ###
    def set_emailInfo(self, _emailInfo):
        self.emailInfo = _emailInfo
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        # Find the first match of the pattern in the string
        match = re.search(pattern, _emailInfo)
        if match:
            self.email = match.group()
            print("Email found:", self.email)
        else:
            print("No email found.")    

    def isDigit(self, _str):
        pattern = r"\d+"
        # Find all matches of the pattern in the string 
        matches = re.findall(pattern, _str)
        if matches:
            digits = [int(match) for match in matches]
            return False
        else:
            return True