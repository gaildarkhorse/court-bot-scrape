import json
from sanitize_filename import sanitize
import os
import shutil
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Set the desired file save location and filename
save_location = './/'
file_name = 'searchresults.pdf'

extension_paths = [
    "adblocker.crx",
    "XBlocker 1.0.4",
    "XBlocker 1.0.4 - langpack"
]

chrome_options = Options()
download_path = r'C:\Users'
chrome_options.add_experimental_option('prefs', {
"download.default_directory": download_path, # change default directory for downloads
"download.prompt_for_download": False, # to auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True # it will not show PDF directly in chrome
})


driver = webdriver.Chrome(options=chrome_options)

driver.maximize_window()
driver.get("https://www.masscourts.org/eservices/home.page.2")

# Wait for the page to load completely
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))

recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

# Solve reCAPTCHA
solver = RecaptchaSolver(driver=driver)
solver.click_recaptcha_v2(iframe=recaptcha_iframe)

# Click on elements using WebDriverWait
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id21"]/span'))).click()
wait.until(EC.element_to_be_clickable((By.ID, "id65"))).click()
Select(driver.find_element(By.ID, "id65")).select_by_visible_text("Probate and Family Court")
wait.until(EC.element_to_be_clickable((By.ID, "id6c"))).click()
Select(driver.find_element(By.ID, "id6c")).select_by_visible_text("Worcester County Probate and Family Court")

wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tab1'))).click()

# Fill out date fields
wait.until(EC.element_to_be_clickable((By.ID, "id54"))).send_keys("10/02/2023")
wait.until(EC.element_to_be_clickable((By.ID, "id55"))).send_keys("11/02/2023")

# Click on an option in a dropdown
select = Select(driver.find_element(By.ID, "id56"))
select.select_by_index(7)

wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id5b"]'))).click()



my_table=driver.find_element(By.CLASS_NAME,'tableResults')
rows = my_table.find_elements(By.TAG_NAME,'tr')
print(len(rows))
for row in range(1,len(rows)):
    row_num=str(row)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#grid\~row-{row_num}\~cell-4'))).click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#titleBar > h1 > ul > li')))

    file_name=driver.find_element(By.CSS_SELECTOR,'#titleBar > h1 > ul > li').text
    file_name=file_name+'.pdf'
    file_name=sanitize(file_name)

    # Click on other elements as needed
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nowrap'))).click()

    time.sleep(10)
    #driver.execute_script('window.print();')

    driver.switch_to.window(driver.window_handles[-1])
    new_file_name = file_name
    destination_path = os.path.join(download_path, new_file_name)
    counter = 1
    while os.path.exists(destination_path):
        # If the file already exists, add a number to the new filename
        file_name, file_extension = os.path.splitext(file_name)
        new_file_name = f"{file_name}_{counter}{file_extension}"
        destination_path = os.path.join(download_path, new_file_name)
        counter += 1
        os.rename(os.path.join(download_path, 'searchresults.pdf'), destination_path)
        driver.execute_script("window.history.go(-1)")

driver.close()
print("PDF saved as:", file_name)
time.sleep(100)
