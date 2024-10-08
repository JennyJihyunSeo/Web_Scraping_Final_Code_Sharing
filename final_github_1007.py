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

# Create a Supabase client
from supabase import create_client, Client

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
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
    options.add_experimental_option("detach", True)  # Opens browser window on a screen during web scrping and prevents the browser window from closing after the task completes.
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Disabling the enable-logging switch to suppress unnecessary logs displayed in the console.
    
    browser = webdriver.Chrome(service=Service(driver_path),options=options)  # Providing the Chrome driver path and browser configuration options defined above.  
    browser.get(url) # Instruct the browser to navigate to the specified URL. 
    browser.maximize_window() # Open the chrome browser maximized during web scraping.
    browser.implicitly_wait(3) # Wait 3 seconds for a browser to absorb all configuration settings before web scraping. 
    return browser # Configure all settings for the browser and save them to the 'browser' object. 
# Extract RFPs having at least one keyword defined in the keywordList using 'GetSearch' function.
def GetSearch(keywordList): # GET method to get data from the server.
  pageCount=0 # It starts from the first page of the website, SAM.gov. Sending a GET requset to SAM.gov.
  dataList=[]
  query = 'OR'.join([f'%22{keyword}%22' for keyword in keywordList]) # Using OR operators when joining keywords.
  query = f'({query})' # This supports logic grouping of keywords using parantheses. For example, ("Water" OR "Electricity" OR ...)
  while True:
    cookies = {
        '_gid': 'GA1.2.1289656124.1726216063',
        'lastVisitedRoute': '%2Fsearch%2F%3Findex%3Dopp%26page%3D1%26pageSize%3D25%26sort%3D-modifiedDate',
        '_ga': 'GA1.2.680698727.1726216063',
        '_ga_1TZM4G6B9F': 'GS1.1.1726216063.3.1.1726216070.0.0.0',
        '_ga_CSLL4ZEK4L': 'GS1.1.1726216063.1.1.1726216130.0.0.0',
        '_dd_s': 'rum=0&expire=1726217030873',
    } # SAM.gov has public data without login. SessionID is not required and the same cookies can be reused whenenver web scarping.

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': '_gid=GA1.2.1289656124.1726216063; lastVisitedRoute=%2Fsearch%2F%3Findex%3Dopp%26page%3D1%26pageSize%3D25%26sort%3D-modifiedDate; _ga=GA1.2.680698727.1726216063; _ga_1TZM4G6B9F=GS1.1.1726216063.3.1.1726216070.0.0.0; _ga_CSLL4ZEK4L=GS1.1.1726216063.1.1.1726216130.0.0.0; _dd_s=rum=0&expire=1726217030873',
        'priority': 'u=1, i',
        'referer': 'https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5BsimpleSearch%5D%5BkeywordRadio%5D=ALL&sfm%5BsimpleSearch%5D%5BkeywordEditorTextarea%5D=(%22WATER%22OR%22TREE%22OR%22NARROW%22)',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    } # Metadata included in HTTP Get request to the server. 
    # Send GET request to Search API endpoint with cookies, headers, search query and page number. 
    response = requests.get(
    'https://sam.gov/api/prod/sgs/v1/search/?random=1726217486086&index=opp&page={}&sort=-modifiedDate&size=100&mode=search&responseType=json&is_active=true&q={}&qMode=SEARCH_EDITOR'.format(pageCount,query),
        cookies=cookies,
        headers=headers,
    ) 
    # Converting JSON formatted 'response' object into a dictionary format and save them into a 'results' object. 
    try:
      results=json.loads(response.text)['_embedded']['results']
    except:
      print("더없다1")
      break
    # Process to see if the 'results' data is saved successfully by converting it into json file.  
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)
    # Check whether there are dictionary-formatted data in the 'results' list.    
    if len(results)==0:
      print('더없다2')
    # If there are data in the list, Get details and save them in a 'data' dictionary and append them into 'dataList'.  
    for result in results:
        title=result.get('title',"")
        postingId=result.get('_id',"")
        url='https://sam.gov/opp/{}/view'.format(postingId)
        try:
          status=result['organizationHierarchy'][0]['status']
        except:
          status=''
        try:
          department=result['organizationHierarchy'][0]['name']
        except:
          department=''
        data={'title':title,'postingId':postingId,'url':url,'status':status,'department':department}
        print(data)
        dataList.append(data)
    # Process to check whether dictionaries are successfully saved in the 'dataList' by converting the list into JSON formatted file.     
    with open('dataList.json', 'w', encoding='utf-8') as f:
        json.dump(dataList, f, ensure_ascii=False)
    # Increment the page number     
    pageCount+=1
    time.sleep(1)
  
def GetDetails(data,browser,supabase,baseUrl): # baseURL = 'https://sam.gov/opp'
  
  
  # Now starting web scraping. 
  browser.get(data['url']) # Already defined URL format above. url='https://sam.gov/opp/{}/view'.format(postingId), indicating each RFP URL. 
  browser.implicitly_wait(3) # Wait until all web elements appear on the web page. 
  # Pop-up window opens when accessing a url. Remove the window by clicking it. 
  try:
    browser.find_element(By.XPATH,'//*[@id="sds-dialog-0"]/layout-splash-modal/div[4]/div[2]/div/button').click()  
  except:
    print("버튼없다.") # After the first access, no more window pop up. 
  time.sleep(0.5)
  browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to the very bottom part of the web page. 
  time.sleep(0.5)
  browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP) # Scroll up to the very top. 
  time.sleep(0.5)

  try: # Identify whether there are attachments on the page.
    WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.ID, "opp-view-attachments-fileLinkId0")) # Find the first link existed within 3 seconds. 
    )
  except TimeoutException: # If the link is not found, the exception code is printed. 
    print("attachments-links section not found within 3 seconds.")

  soup=BeautifulSoup(browser.page_source,'html.parser')
  with open('soup.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

  # Create an empty list.
  generalInfos = []
  try:   
      generalInformation=soup.find('ul',attrs={'class':'usa-unstyled-list'}) # Find 'ul' tag with the specified attribute in the HTML using 'soup' object.
      if generalInformation: # If there is a general informaiton, it will execute the below code. 
          generalInfoList=generalInformation.find_all('li') # Find all 'li' tags under the parent 'ul' tag and store as a dictionary for each 'li' tag in a list.
          for generalInfo in generalInfoList:
              text=generalInfo.get_text() # Only extract text in the 'li' tag.
              if text.find(":")>=0: # Find ':' character in the text.
                title, contents = text.split(":", 1) # Split the text at the first occurrence of :
                generalInfos.append({'title': title.strip(), 'contents': contents.strip()}) # Get only text withouht any spaces.
      else:
          print("generalInformation section not found.")  # When the general info is not found, print this.         
      # generalInfos.append(text)    
  # Handling unexpected errors while executing 'try' loop.     
  except Exception as e:
      print("generalInfoList 오류:", e)
      

  # 수정 사항 반영 
  # Find 'div' tag in the HTML document, parsed by bs4 using HTML.parser and stored in 'soup' object. 
  try:
    descriptionTag=soup.find('div',attrs={'class':'inner-html-description ng-star-inserted'})
    description=descriptionTag.get_text() # Only extract text within 'div' tag. 
  except Exception as e:
    print("descriptionTag 오류",e)
    description="" # If there is no description in a RFP, just leave it as "".

  # 수정 사항 반영 contact information 가지고 오기 (Separate Contracting Office Address, Primary Point of Contact, and Secondary Point of Contact)
 
  
    # Extracting Contracting Office Address 
  try:
      contracting_office_div = soup.find('div', attrs={'id':'-contracting-office'}) # Find 'div' (division) tag in the HTML and stored them in 'contracting_office_div' object.
      if contracting_office_div: # If 'div' tag exists, find inner 'div' tag with the  class 'ng-star-inserted'.
          contracting_office_content = contracting_office_div.find('div',attrs={'class':'ng-star-inserted'}) 
          contracting_office_address = contracting_office_content.get_text(strip=True) if contracting_office_content else "" # Only Extract the exact office address under the subtitle. 
      else:
          contracting_office_address = "" # If 'div' tag does not exist, return back the empty string. 
  except Exception as e: # This error code handles any unexpected error except for neither the subtitle nor the details of address exist on the page.  
      print(f"Error fectching Contracting Office Address: {e}")
      contracting_office_address = "" 
  
  # Extract the primary point of contact and the secondary point of contact. 
  primary_poc_list = []
  secondary_poc_list = []
  try:
      primary_poc_div = soup.find('div', attrs={'id':'contact-primary-poc'}) # Find 'div' (division) tag and store them in 'primary_poc_div' object. 
      if primary_poc_div:
          primary_poc_ul = soup.find('ul', attrs={'class':'usa-unstyled-list ng-star-inserted'}) # Find inner 'ul' (Unordered list) tag with the specified class. 
          primary_poc_li_list = primary_poc_ul.find_all('li') # Find inner 'li' (list) tag where 'name', 'email' and 'phone number' are placed in each 'li' tag. 
      # 빈 dictionary를 생성해서 Name, Email, Phone을 기재 (Add details in an empty dictionary.)
          primary_poc_info = {'Name': '', 'Email': '', 'Phone': ''}

          for li in primary_poc_li_list: # 'li' tag was parsed as a bs4 object. 
              name_tag = li.find('strong') # name in charge of the document is placed within 'strong' tag under 'li' tag. 
              if name_tag:
                  primary_poc_info['Name'] = name_tag.get_text(strip=True) # Only Extract the text representing the name of the person in charge of. 
              else:
                  primary_poc_info['Name'] = "" # Return back the empty string if there is no name. 

              email_tag = li.find('a', href=True) # Find 'a' tag with the hypertext reference being True as its attribute under 'li' tag. 
              if email_tag:
                  primary_poc_info['Email'] = email_tag.get_text(strip=True)
              else:
                  primary_poc_info['Email'] = ""

              phone_tag = li.find('span', attrs={'class': 'sr-only'}) # Find 'span' tag with the 'sr-only' class under 'li' tag.
              if phone_tag and 'Phone Number' in phone_tag.get_text(strip=True):
                  phone_number = phone_tag.find_next_sibling(text=True) # 해당 tag에 있는 2번째 글자를 가지고 와야 함. 
                  primary_poc_info['Phone'] = phone_number.strip() if phone_number else ""
              else:
                  primary_poc_info['Phone'] = "" 
          primary_poc_list.append(primary_poc_info)

      else: # If there isn't any contact details existed at all on the page, return back the empty dictionary. 
          primary_poc_info = {'Name': '', 'Email': '', 'Phone': ''}             
          primary_poc_list.append(primary_poc_info) # Add an empty dictionary if no contact info is available. 
  except Exception as e:
      print("Error fetching Primary Point of Contact: {e}")
      primary_poc_list.append({'Name': '', 'Email': '', 'Phone': ''}) 

  # Extract Secondary Point of Contact
 
  try:
      secondary_poc_div = soup.find('div', attrs={'id':'contact-secondary-poc'})
      if secondary_poc_div:
          secondary_poc_ul = soup.find('ul', attrs={'class':'usa-unstyled-list ng-star-inserted'}) 
          secondary_poc_li_list = secondary_poc_ul.find_all('li') 
      
          secondary_poc_info = {'Name': '', 'Email': '', 'Phone': ''}

          for li in secondary_poc_li_list:
              name_tag = li.find('strong')
              if name_tag:
                  secondary_poc_info['Name'] = name_tag.get_text(strip=True) 
              else:
                  secondary_poc_info['Name'] = "" 

              email_tag = li.find('a', href=True) 
              if email_tag:
                  secondary_poc_info['Email'] = email_tag.get_text(strip=True)
              else:
                  secondary_poc_info['Email'] = ""

              phone_tag = li.find('span', attrs={'class': 'sr-only'}) 
              if phone_tag and 'Phone Number' in phone_tag.get_text(strip=True):
                  phone_number = phone_tag.find_next_sibling(text=True)
                  secondary_poc_info['Phone'] = phone_number.strip() if phone_number else ""
              else:
                  secondary_poc_info['Phone'] = "" 
          secondary_poc_list.append(secondary_poc_info)

      else:
          secondary_poc_info = {'Name': '', 'Email': '', 'Phone': ''}             
          secondary_poc_list.append(secondary_poc_info)
  except Exception as e:
      print("Error fetching Primary Point of Contact: {e}")
      secondary_poc_list.append({'Name': '', 'Email': '', 'Phone': ''}) 


# Find all <a> (anchor) tag in the HTML of the page that contains file download links. 
  fileLinks=soup.find_all('a',attrs={'class':'file-link ng-star-inserted'}) # The find_all function searches for all matching tags in the HTML and return them as a list. 
  downloadUrls=[]
  for fileLink in fileLinks: # baseURl + partial URL in 'href' (hypertext reference) & (opens in new window) means opening a file in another window but remove it here.
    input={'url':'https://sam.gov'+fileLink['href'],'title':fileLink.get_text().replace("(opens in new window)","").strip()} 
    downloadUrls.append(input) 
  

  for index,downloadUrl in enumerate(downloadUrls):
    print(f"{index+1}/{len(downloadUrls)}번째 파일 다운로드")
    response = requests.get(downloadUrl['url'])
    with open(f'docs/{downloadUrl["title"]}', 'wb') as file:
        file.write(response.content)





  # Create an empty list to store public URLs of uploaded files to Supabase.
  hostingUrls=[]
  # Upload files to Supabase storage.
  for index,downloadUrl in enumerate(downloadUrls):
    print(f"{index+1}/{len(downloadUrls)}번째 파일 업로드") # Upload the downloaded file in your local computer to Supabase.
    file_path = f'docs/{downloadUrl["title"]}'
    with open(file_path, 'rb') as file: # Open the downloaded file in read-binary mode to upload it using 'file' object
      # Get today's date in YYYY-MM-DD format
      today_date = datetime.datetime.today().strftime('%Y-%m-%d') # Define variable. 
      file_data = file.read() # Read each file in a 'docs' folder in your local computer and save then in 'file_data' variable. 
      file_name = f'{today_date}/{data["postingId"]}/{downloadUrl["title"]}' # Define file_path in Supabase storage.
      try:
        response = supabase.storage.from_('docs').upload(file_name, file_data) # Assign 'file_name' and 'file_data' to 'response' instance to upload each file. 
        public_url = f"{baseUrl}/storage/v1/object/public/docs/{file_name}" # The standard format of the public URL of the uploaded file in Supabase.
        hostingUrls.append({'title': downloadUrl['title'], 'url': public_url})
      except Exception as e:
        print(f"Error uploading file: {e}")

    
    
    
    
  
  dataMore={
    'generalInfos':generalInfos,
    'description':description,
    'downloadUrls':downloadUrls,
    'hostingUrls':hostingUrls,
    'contracting_office_address':contracting_office_address, 
    'primary_poc':primary_poc_list,
    'secondary_poc': secondary_poc_list # Add the contact_info
  }
  data.update(dataMore) # The original 'data' dictionary is data={'title':title,'postingId':postingId,'url':url,'status':status,'department':department} but add more keys from dataMore.
  pprint.pprint(data)  # Print the dictionary in more readable and formatted way. 
  return data
  
  
  time.sleep(3)
    
def GetUploads(data):
    url = "https://wbdjmxiyffwpazexmdhr.supabase.co"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndiZGpteGl5ZmZ3cGF6ZXhtZGhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzNjM5OTAsImV4cCI6MjA0MTkzOTk5MH0.poQUOwW-9otlWDD_VXjktIowQtY8hS0AUC4vh3k4azk"
    table_name = "data" # Need to create a new 'data' table in Supabase in advance.

    headers = {
        "Content-Type": "application/json",
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}"
    }
    # Use HTTP POST Request to send an API call to Supbase for uploading data. 
    response = requests.post(
        f"{url}/rest/v1/{table_name}", # Supabase REST API 
        headers=headers,
        data=json.dumps(data) # Upload JSON encoded data. 
    )

    if response.status_code == 201:
        print("Data successfully inserted into the Supabase table.")
    else:
        print(f"Failed to insert data into Supabase table. Status code: {response.status_code}, Response: {response.text}")

def clear_docs_folder():
    folder = 'docs'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


# # ==========Frist Part.Searching Keywords=============
# # Define which keywords you are going to extract from SAM.gov.
# # Input keywords related to a utilities sector.
keywordList=['WATER','Electricity','Wifi','sewage','irrigation','waste','telecommunications','Natural gas','recycling','Internet']
# # GetSearch function defined above will search RFPs having at least one keyword in the KeywordList.
GetSearch(keywordList)
# #=============================

# Create a Supabase client information to connect by defining public URL and personal api-key.
url = "https://wbdjmxiyffwpazexmdhr.supabase.co"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndiZGpteGl5ZmZ3cGF6ZXhtZGhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzNjM5OTAsImV4cCI6MjA0MTkzOTk5MH0.poQUOwW-9otlWDD_VXjktIowQtY8hS0AUC4vh3k4azk"
# Supabase Client Creation.
supabase: Client = create_client(url, api_key)

# Create 'docs' folder.
createFolder('docs')

#============Extracting specific details of each RPF searched already=============
# Before extracting specific details from RFPs, Load the 'dataList' saved in a Json format back into a Python 'List' for further processing.
with open('dataList.json', 'r', encoding='utf-8') as f:
  dataList=json.load(f) # json.load is a function coverting Json file into a Python dictionary or a list, making it easeir to further process.

# Open an empty list to combine the results of 'dataList', obtained by 'GetSearch' and the addtional details from 'dataMore', obtained by 'GetDetails'.
totalResult=[]
# Open a Chrome broswer for web scraping.
browser=chrome_browser('https://www.google.co.kr')

# Get details from each document using 'GetDetails' function. 

for index,data in enumerate(dataList): # DataList is a list of dictionaries and 'data' is one of the dictionaries in the list, representing each document(RFP). 
  print(f"{index+1}/{len(dataList)}번째 기사 상세정보 가져오기") 
  result=GetDetails(data, browser, supabase, url)

    # This process is for checking the result by converting the result into json format. 
  with open('result.json', 'w', encoding='utf-8') as f: # 
    json.dump(result, f, ensure_ascii=False) # Convert the 'result' dictionary into the Json format using json.dump and write the file using 'f' object. 
  
  # Upload result to Supabase.
  GetUploads(result) 

 


  # Clear a 'docs' folder .
  clear_docs_folder()
  # Save the result to 'totalResult.
  totalResult.append(result)
  # 전체 결과를 'totalResult.json' 파일에 저장합니다.
  with open('totalResult.json', 'w', encoding='utf-8') as f:
    json.dump(totalResult, f, ensure_ascii=False)
  
  # Wait for 1 minute.
  time.sleep(1)
