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

#until I figure out how to convert html tables into python usuable code, here is a manual copypast of the important parts:
event_id = """0000032172
0000032983
09-374704
0000032778
0000032947
04-3Q8504
04-2K7404
0000032953
10-0K1304
0000033002
0000033013
0000032819
0000033051
0000032971
0000032970
0000032969
0000032944
0000032821
0000032745
0000033036
0000032998
06A3121
0000032846
08A3782
07-355604
06A3123
0000033057
01-0K9404
03A3851
03A3885
04-0P9204
05A2772
08A3783
0000032546
0000032952
05A2782
06A3084
32A0609
0000033012
0000032975
0000033052
0000032967
C24-32866
603-2024
0000030279
0000033015
0000033019
0000032867
0000033033
0000033064
0000032946
0000031934
0000032759
0000033113
0000033017
611-2024
0000033095
0000033082
0000032092
0000032831
0000032849
0000033065
0000032810
0000032866
0000033091
0000033068
0000032995
0000033067
0000032807
0000032839
0000032847
0000032881
0000032845
0000033083
0000033081
0000033107
0000032930
0000032905
0000032270
0000033088
0000033137
0000033138
0000032693
64A0281
11A4048
11A4033
11-430904
10-1H3604
09A1029
0000033039
0000033060
01A6444
04A7123
07-358404
07A5979
0000032860
24-10205
0000032715
0000033041
04A7022
0000033106
0000032929
0000033044
0000032994
0000031286
0000033111
0000029644
12-0R3154
10-0Q2104
07-4P8504
04-0K6404
0000032858
0000033130
0000033110
C24-32761
0000033011
0000032750
0000032885
0000032601
0000032856
0000032972
10A2719
0000033119
0000032648
0000033109
0000033063
0000032933
0000033129
0000032805
24-197
0000033072
08A3773
07-377604
0000033139
56A0819
04-0P7604
0000032808
0000033038
56A0825
59A1294
0000033153
02A2339
08A3775
C24-32888
0000033073
0000032966
0000032816
0000032984
0000033066
0000033048
20A0362
0000033050
0000033097
0000033142
0000033166
5249923
0000033151
0000033143
0000033089
0000033145
0000032853
0000033144
0000033043
0000032820
0000032016
0000033156
0000032938
S24BS014
0000032754
0000033155
0000033134
0000033132
0000033058
0000033093
04A7117
0000033009
0000032997
0000032269
0000032977
02A2340
0000033062
0000033176
0000033148
0000033018
24-219
0000033116
0000032711
0000032838
0000032842
0000032948
0000032916
01A6464
02A2341
05A2788
06A3120
08-1J3004
09A1025
12-0R57U4
12A2235
0000033096
0000033164
0000033053
0000032397
0000033154
0000033188
0000033101
0000032955
0000033046
0000033045
0000033084
0000033085
0000033037
0000033055
10201544
C24-32781
0000033042
04-1Q5304
12-0U9804
0000033120
0000033022
0000033059
0000033152
0000032926
0000032981
0000033167
0000032869
0000032800
9CA07004
9CA07005
01-0J8904
12-0R3114
05-1J8604
01A6459
EADM90324
0000033074
9CA07006
0000032824
0000033070
0000033090
0000033118
0000033181
0000032685
0000032987
0000033121
0000033075
ST249012
0000033034
0000033186
ST249014
0000033086
610-2024
0000032949
0000033115
0000033123
0000033183
0000033023
0000033056
0000033087
0000033108
0000032961
0000033020
0000033103
0000033000
0000033040
65A1198
0000033182
0000032661
0000033069
0000033177
24-10243
0000033185
0000033178
0000032978
01-0H6404
08-1J2704
07-347904X
08-1J3304
03-2J5904
05-1H6914
05-1K4504
0000033026
0000033184
24-224
0000033080
0000033146
0000033114
0000033104
0000033003
0000032910
0000032877
0000033170
03-1H1404
05-1K6404
07-351124
08-1K6904
11-056404
12-0R32U4
0000033163
0000033150
03A3892
0000033133
0000033071
0000033092
0000033136
0000033160
EEOS90724
04-1Q76CM
0000032982
589-2024
3CA06820
0000032752
0000033128
24-229
0000033162
0000033078
0000033077
02-4H03U4
0000033047
0000033135
24-228
0000033149
0000033035
08-1J7204
04-0K8004X
0000033054
24-206
0000033098
08-0G8504
07-350404
0000033102
0000033141
0000032913
0000032976
A/E RFQ
0000033180
0000033061
0000033165
24-230
0000033171
0000033173
0000032991
0000028910
0000032960
0000032263
0000032893
09-379104
05-1G9504
24-173
0000033076
08-1K4004
0000033168
02-1J75U4
09-366804
0000032666
0000032550
02-4H0704
05-1J9704
0000033094
07-348204
HD249101
0000033127
0000032989
0000030212
0000027279
0000033006
0000032367
0000032868
0000032284
0000033099
0000033124
0000022860
0000015808
0000031994
0000032613
0000032650"""
event_id_list = event_id.split()
dept = """5225
8940
2660
7760
2720
2660
2660
7760
2660
8570
3600
3860
1111
2720
2720
2720
2720
3860
4140
7760
8955
2660
7760
2660
2660
2660
1700
2660
2660
2660
2660
2660
2660
7760
6100
2660
2660
2660
7100
7100
5225
3340
5160
6630
77601
2720
8940
1701
7760
7502
5225
5225
2720
2740
6200
6630
7920
3600
5225
7760
7760
3340
3560
5225
2720
0820
8955
7760
8855
2720
2720
SS246
2720
2720
8940
3790
3790
3790
8955
8940
8560
7920
7760
2660
2660
2660
2660
2660
2660
7760
7760
2660
2660
2660
2660
3860
4265
6770
8560
2660
8955
5225
2720
2720
77601
7760
77601
2660
2660
2660
2660
7760
5225
5225
5160
3600
3790
3840
3860
3860
4440
2660
7100
7100
7100
8955
4440
5225
3360
2740
8940
2660
2660
3600
2660
2660
5225
6840
2660
2660
3355
2660
2660
5160
7100
7100
3860
7100
3860
8955
2660
8940
8940
5225
7920
77601
5225
2720
3820
2720
5225
5180
4440
4440
0690
8955
8120
7350
5225
2720
7760
7760
3960
2740
2660
2720
5225
5225
8940
2660
8955
7760
2720
3600
2740
6530
SS246
2720
2720
5225
77601
2660
2660
2660
2660
2660
2660
2660
2660
3600
3860
4440
7100
7760
5420
0820
6820
2720
2720
2720
2720
2720
3790
3860
5160
7100
2660
2660
3600
8940
7760
2720
7760
7760
3790
8660
2720
3540
3540
2660
2660
2660
2660
0840
7760
3540
77601
7100
4440
6511
6530
7502
4440
4440
4300
4300
3900
5225
4300
8955
6630
2720
7760
7760
7760
8940
8940
8940
8940
3600
3600
7760
7760
7760
2660
6250
5225
4440
5420
4265
4440
7760
7760
2660
2660
2660
2660
2660
2660
2660
1701
0954
2740
7760
3790
3600
7760
7760
6810
3860
2720
2660
2660
2660
2660
2660
2660
2720
3360
2660
SS246
2720
SS246
5225
8570
0840
2660
3860
6630
3540
5225
3360
2740
2720
7760
2720
2660
6650
3860
2740
2720
7100
2660
2660
3860
2740
8940
2660
2660
0250
7760
3790
3790
6580
6770
7920
7760
2740
2720
2720
0650
4265
7730
4440
0250
2660
2660
2740
8660
2660
2720
2660
2660
3600
7760
2660
2660
6760
2660
4300
0509
3790
2665
4440
5225
3790
3600
1115
7760
0509
0840
SS135
6690
3760
0860
"""
dept_list = dept.split()


#function was copypasted wholesale
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
    

#nonfunc part obviously not complete, and I lack understanding of some parts
#filler variables
supabase = "foobar"
url = "foobar"

# Open an empty list to combine the results of 'dataList', obtained by 'GetSearch' and the addtional details from 'dataMore', obtained by 'GetDetails'.
#idk what total result does
totalResult=[]
# Open a Chrome broswer for web scraping.
browser=chrome_browser('https://www.google.co.kr')

for deptID, eventID in zip(dept_list, event_id_list): 
    data = {'url':'https://caleprocure.ca.gov/event/{}/{}'.format(deptID, eventID)}
    #print(data)
    result=GetDetails(data, browser, supabase, url)

    # Save the result to 'totalResult.
    totalResult.append(result)

  