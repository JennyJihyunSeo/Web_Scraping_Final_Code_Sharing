import json
import os
import time
from bs4 import BeautifulSoup
import requests
import shutil
from selenium.webdriver.chrome.service import Service # Providing the Chrome driver path installed in a local machine to a web driver to control the Chrome browser. 
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver # Using webdriver library in a Selenium module to configure Chrome settings and control the Chrome browser. 
from selenium.webdriver.common.by import By
import pprint
import chromedriver_autoinstaller # Library to automatically install chromedriver that matches the Chrome browser in a local machine. 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Browser wait until a expected_conditions is met. 
from selenium.webdriver.support import expected_conditions as EC # Define a specific conditon that should be met. 
from selenium.common.exceptions import TimeoutException # Browser does not meet a specific condition, TimeoutException can be executed. 
from selenium.webdriver.common.keys import Keys
import datetime

import pandas

#also needed to make supabase upload work
# Create a Supabase client
from supabase import create_client, Client

downloadDir = "docfoo"

#function was copypasted wholesale
    #plan to add a different default download spot to make programming much easier
# Define chrome_browser to initialize and set up the Chrome browser for installation purposes. 
def chrome_browser(url):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # Identify the version of Chrome browser in a local machine 
    driver_path = f'{chrome_ver}/chromedriver.exe' # Create a path for the Chrome driver and save the installation file. 

    if os.path.exists(driver_path):
        print(f"chromedriver is installed: {driver_path}")  # To check if the Chrome drive exists at the specified path.
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")  # If the driver does not exist, the function will automatically install the driver. 
        chromedriver_autoinstaller.install(True)

    options = webdriver.ChromeOptions()  # Configure Chrome browser options at once and send all configurations to the webdriver in one go by using options as object(or instance). 
    # options.add_argument('headless') # 'headless' mode enables Chrome browser to be operated in the background without opening a window on a screen.
    # options.add_argument('--headless=new') # This is the newer version of 'headless' mode that matched the newer version of 'Chrome browser' 

    #set new download directory
    #downloadDir = "docfoo" #set globally now
    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' + directory)
    createFolder(downloadDir)
    #print(os.path.dirname(downloadDir))
    #print(os.path.realpath(downloadDir))
    prefs = {"download.default_directory" : os.path.realpath(downloadDir) #this one works
             #"download.default_directory" : os.path.dirname(downloadDir)
             #"download.default_directory" : "/"+downloadDir
             #,'savefile.default_directory': "/"+downloadDir
             #,"directory_upgrade": True
             }
    
    options.add_experimental_option("prefs",prefs)

    options.add_experimental_option("detach", True)  # Opens browser window on a screen during web scrping and prevents the browser window from closing after the task completes.
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Disabling the enable-logging switch to suppress unnecessary logs displayed in the console.
    
    browser = webdriver.Chrome(service=Service(driver_path),options=options)  # Providing the Chrome driver path and browser configuration options defined above.  
    browser.get(url) # Instruct the browser to navigate to the specified URL. 
    browser.maximize_window() # Open the chrome browser maximized during web scraping.
    browser.implicitly_wait(3) # Wait 3 seconds for a browser to absorb all configuration settings before web scraping. 
    return browser # Configure all settings for the browser and save them to the 'browser' object. 

#no keyword functionality yet
#heavily modified for no api
#I can either download the file to a more convenient location or try the request.get route
def GetSearch():
    browser.get("https://caleprocure.ca.gov/pages/Events-BS3/event-search.aspx") #cannot use any keywords if I go straight to this webpage #no actually i can, I think.
    

    #going to insert my keyword search functionality here
    if True: #change to False to toggle off the keyword search
        browser.implicitly_wait(15) #page loads super long for some reason
        searchBox = browser.find_element(By.NAME, "RESP_INQA_WK_ZZ_AUC_NAME")
        theKeywords = "water"
        searchBox.send_keys(theKeywords)  # Enter text
        browser.implicitly_wait(1) #paranoid that text input could somehow cause delay
        browser.find_element(By.NAME, "RESP_INQA_WK_INQ_AUC_GO_PB").click()
        #print("got to here, test 1")
        
        time.sleep(0.5)
        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element_attribute((By.ID, "loadingContainer"), "style", "display: none") #this checks if the search loading screen is displayed or not
        )
        #inserted the above b/c i wonder if the bug that I'm encountering where it says the (first) download buttom is not clickable is related to the page refreshing
        #I think the issue is that, while searching, the page technically still has the button on the screen, it just is not clickable while the search is loading

    #print("got to here, test 2")
    browser.implicitly_wait(15) #page loads super long for some reason
    browser.find_element(By.ID,'RESP_INQA_HD_VW_GR$hexcel$0').click() #clicks on download link
    #copypasted from another one
    #should be best sleep thing
    #is it better or worse than an implicit wait?
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "downloadButton"))
    )
    #we'll see if the below works or not, don't entirely understand it because I copied some parts
    browser.find_element(By.ID,'downloadButton').click() #to see if my issue is with request or with something else
    #do i need to wait for file to download?

    #soup=BeautifulSoup(browser.page_source,'html.parser')
    #downloadURL = soup.find(id='downloadButton')['href']
    #print(soup.find(id='downloadButton'))

    #could be a useful code chunk if I do go go the request.get route
    #remember that a proxy could be an option too
    #cookies = browser.get_cookies()
    #print(cookies)
    #requests.get(downloadURL, cookies=cookies)

    #response = requests.get(downloadURL)
    #print(response.content)
    #print(response.text)

    #downloadFile = response.content
    #soup2=BeautifulSoup(downloadFile,'html.parser')
    #print(soup2.get_text)

#I've separated the getting of excel file and the parsing of it for now
def GetSearch2(rawtext): 
    soup3=BeautifulSoup(rawtext,'html.parser')
    print(soup3.stripped_strings)
    
    #for now, the (single needed) url is manually put in
def GetDetails(data,browser,supabase,baseUrl):
    # Now starting web scraping. 
    #browser.get(data['url']) # Already defined URL format above. #the ideal form
    #note for later: dept (id) and event id make up the url
    #browser.get('https://caleprocure.ca.gov/event/5225/0000032172') #first testing on one page
    browser.get(data['url'])
    browser.implicitly_wait(5) # Wait until all web elements appear on the web page. 
    
    #no idea what this code block is for
    time.sleep(0.5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to the very bottom part of the web page. 
    time.sleep(0.5)
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP) # Scroll up to the very top. 
    time.sleep(0.5)

    #no idea what this code block is for
    try: # Identify whether there are attachments on the page.
        WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.ID, "opp-view-attachments-fileLinkId0")) # Find the first link existed within 3 seconds. 
        )
    except TimeoutException: # If the link is not found, the exception code is printed. 
        print("attachments-links section not found within 3 seconds.")

    #don't quite get this code block etiher
    soup=BeautifulSoup(browser.page_source,'html.parser')
    with open('soup.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    #skipped the general info code block
    
    #taking the description
    # 수정 사항 반영 #no clue what this comment is
    # Find 'div' tag in the HTML document, parsed by bs4 using HTML.parser and stored in 'soup' object. 
    try:
        descriptionTag=soup.find('div',attrs={'class':'pre-wrap'}) #modified
        description=descriptionTag.get_text() # Only extract text within 'div' tag. 
    except Exception as e:
        print("descriptionTag 오류",e)
        description="" # If there is no description in a RFP, just leave it as "".    

    #skipped more text extraction like the contact info
    #and the download links
    #and anything related to supabase

    dataMore={'description': description} #incomplete
    data.update(dataMore) # The original 'data' dictionary is data={'title':title,'postingId':postingId,'url':url,'status':status,'department':department} but add more keys from dataMore.
    pprint.pprint(data)  # Print the dictionary in more readable and formatted way. 
    return data
    
#supabase upload time, I hope this works b/c it's copypaste
#my proj url: https://lnfmdenuypxerbhryayk.supabase.co
def GetUploads(data):
    print("got to here")
    url = "https://lnfmdenuypxerbhryayk.supabase.co" #new url, for my own supabase thing
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxuZm1kZW51eXB4ZXJiaHJ5YXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkwMDkwMzksImV4cCI6MjA0NDU4NTAzOX0.EcEByECBNGhPZAb3vvLKWQER9OmWmX9ItbSIkH33DFw" #new api key, for my own supabase thing

    #from here on out it is completely copypaste, let's hope this works
    table_name = "data" # Need to create a new 'data' table in Supabase in advance.
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}"
    }
    # Use HTTP POST Request to send an API call to Supbase for uploading data. 
    #print("got to pre-post")
    response = requests.post(
        f"{url}/rest/v1/{table_name}", # Supabase REST API 
        headers=headers,
        data=json.dumps(data) # Upload JSON encoded data. 
    )
    print("got to post-post")#it appears that when my project is paused it had an error where it did not get to here, but after unpausing I still have problems
    #^after unpausing, my second run worked just fine without, I recall, any code changes

    if response.status_code == 201:
        print("Data successfully inserted into the Supabase table.")
    else:
        print(f"Failed to insert data into Supabase table. Status code: {response.status_code}, Response: {response.text}")


#i think the following block is the missing piece as to why my supabase upload is not working?
# Create a Supabase client information to connect by defining public URL and personal api-key.
url = "https://lnfmdenuypxerbhryayk.supabase.co" #new url, for my own supabase thing
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxuZm1kZW51eXB4ZXJiaHJ5YXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkwMDkwMzksImV4cCI6MjA0NDU4NTAzOX0.EcEByECBNGhPZAb3vvLKWQER9OmWmX9ItbSIkH33DFw" #new api key, for my own supabase thing
# Supabase Client Creation.
supabase: Client = create_client(url, api_key)

#nonfunc part obviously not complete, and I lack understanding of some parts
#filler variables
#supabase = "foobar"
#url = "foobar" #is this the variable messing me up?

# Open an empty list to combine the results of 'dataList', obtained by 'GetSearch' and the addtional details from 'dataMore', obtained by 'GetDetails'.
#idk what total result does
totalResult=[]
# Open a Chrome broswer for web scraping.
browser=chrome_browser('https://www.google.co.kr')

GetSearch() #let's see if this works

#f = open("ps (14).xls")
#content = f.read()
#f.close()
#GetSearch2(content)
time.sleep(5) #because download take some time
#but I wish there was a better way to wait for file to download, something using implicit wait
#no idea why regular directory name does not work
foo1 = pandas.read_html(os.path.realpath(downloadDir)+"\\ps.xls", header=0)
#print(len(foo1)) #it's one
dept_list = foo1[0]["Department"]
event_id = foo1[0]["Event ID"]

#copied almost wholesale (thus with little true understanding)
def clear_foobar_folder():
    folder = downloadDir
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

clear_foobar_folder()
#convenience, so that the pgm can work without manually resetting things

for deptID, eventID in zip(dept_list, event_id): 
    data = {'url':'https://caleprocure.ca.gov/event/{}/{}'.format(deptID, eventID)}
    #print(data)
    result=GetDetails(data, browser, supabase, url) 

    # Save the result to 'totalResult.
    totalResult.append(result)

    #below is mostly copypaste, and also I have no idea if converting to json is necessary or not
    # This process is for checking the result by converting the result into json format. 
    #this idk what this does or if it is necessary
    with open('result.json', 'w', encoding='utf-8') as f: # 
        json.dump(result, f, ensure_ascii=False) # Convert the 'result' dictionary into the Json format using json.dump and write the file using 'f' object. 
  
    #print(result)
    # Upload result to Supabase.
    GetUploads(result)

#do i have to manually create the data table in supabase??? it does seem to work at changing the error code from ?404? to 400
#after adding new columns, i now have status code 401
#perhaps supabase must also allow anonymous users or whatever its called
#it worked after allowing anonymous users or whatever they're called, then adjusting the rls policies to match the other db's exactly
#meaningless line to try another shot at making my github push work
  