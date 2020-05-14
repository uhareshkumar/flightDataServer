from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import time

date = sys.argv[1]
month = sys.argv[2]
year = sys.argv[3]

faname = sys.argv[4].replace("_"," ")
fcode = sys.argv[5]
fcname = sys.argv[6].replace("_"," ")
fccode = sys.argv[7]

tname = sys.argv[8].replace("_"," ")
tcode = sys.argv[9]
tcname = sys.argv[10].replace("_"," ")
tccode = sys.argv[11]

fname = []
stime = []
rtime = []
duration = []
paytm_price = []
yatra_price = []
goibibo_price = []

#paytm

link = 'https://paytm.com/flights/flightSearch/'+fcode+'-'+faname+'/'+tcode+'-'+tname+'/1/0/0/E/'+year+'-'+month+'-'+date
print(link)

driver = webdriver.Chrome(executable_path=r'C:\xampp\htdocs\test2\chromedriver.exe')
driver.implicitly_wait(20)
try:
    driver.get(link)
except:
    exit(0)
    
try:
    driver.find_element_by_xpath("//*[@class='_3215 row']")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    i = 0

    for a in soup.findAll('div', attrs={'class':'_3215 row'}):
        i += 1
        temp = a.find('div', attrs={'class':'_3H-S _1Eia'})
        fname.append(temp.text)

        temp = a.find('div',attrs={'class':'_3Lds _1OV0'})
        temp = temp.find('div',attrs={'class':'_3H-S'})
        stime.append(temp.text[:5])

        temp = a.find('div', attrs={'class':'_3H-S _1wD5'})
        rtime.append(temp.text[:5])

        temp = a.find('div',attrs={'class':'_1cxG'})
        paytm_price.append(temp.text)
        yatra_price.append("Not Found")
        goibibo_price.append("Not Found")

        temp = a.find('div', attrs={'class':'_3zzl _1OV0'})
        x1 = temp.find('div',attrs={'class':'vY4t'})
        duration.append(x1.text)

except:
    driver.quit()

#yatra

i = 0

temp_name = ""
temp_stime = ""
temp_rtime = ""
temp_price = ""
temp_duration = ""

if(fccode.upper() != "IN" or tccode.upper() != "IN"):
    link = 'https://flight.yatra.com/air-search-ui/int2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin='+fcode.upper()+'&originCountry='+fccode.upper()+'&destination='+tcode.upper()+'&destinationCountry='+tccode.upper()+'&flight_depart_date='+date+'%2F'+month+'%2F'+year+'&ADT=1&CHD=0&INF=0&class=Economy'
    print(link)

    driver = webdriver.Chrome(executable_path=r'C:\xampp\htdocs\test2\chromedriver.exe')
    driver.implicitly_wait(20)
    try:
        driver.get(link)
    except:
        exit(0)
    try:
        driver.find_element_by_xpath("//*[@class='full no-pad pt-20']")

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(2)
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        
        soup = soup.find('div', attrs={'class':'result-set pr one single multiple-result'})
        for a in soup.findAll('div', attrs={'class':'js-flightItem'}):
            i += 1
    
            temp = a.find('div', attrs={'class':'full mb-8 fs-13 airline-name'})
            temp_name = temp.text.replace("\n","").strip()
            if temp_name == "Vistara Premium Economy":
                temp_name = "Vistara"
    
            temp = a.find('p', attrs={'class':'fs-16 bold mb-2 time'})
            temp = temp.text.replace(" ","")
            temp_stime = temp[4:].strip()
    
            temp = a.find('p', attrs={'class':'bold fs-16 mb-2 pr time'})
            temp_rtime = temp.text[:5].strip()

            temp = a.find('p', attrs={'class':'fs-12 bold du mb-2'})
            temp_duration = temp.text.strip()

            temp = a.find('div', attrs={'class':'mb-10 fs-20 bold lh-1 cursor-pointer'})
            temp = temp.find('p').text.replace("\n","")
            x = temp.index(" ")
            temp_price = temp[:x].strip()
    
            k = 0
            for j in range(len(fname)):
                if(temp_name.strip().lower() == fname[j].strip().lower() and temp_stime.strip() == stime[j].strip() and temp_rtime.strip() == rtime[j].strip()):
                    yatra_price[j] = temp_price
                    k = 1
                    break
        
            if k == 0:
                fname.append(temp_name)
                stime.append(temp_stime)
                rtime.append(temp_rtime)
                duration.append(temp_duration)
                paytm_price.append("Not Found")
                yatra_price.append(temp_price)
                goibibo_price.append("Not Found")
    except:
        driver.quit()

else:
    link = 'https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin='+fcode.upper()+'&originCountry='+fccode.upper()+'&destination='+tcode.upper()+'&destinationCountry='+tccode.upper()+'&flight_depart_date='+date+'%2F'+month+'%2F'+year+'&ADT=1&CHD=0&INF=0&class=Economy'
    print(link)

    driver = webdriver.Chrome(executable_path=r'C:\xampp\htdocs\test2\chromedriver.exe')
    driver.implicitly_wait(20)
    try:
        driver.get(link)
    except:
        exit(0)
    try:
        driver.find_element_by_xpath("//*[@class='flightItem border-shadow pr']")

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(2)
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
    
        for a in soup.findAll('div', attrs={'class':'flightItem border-shadow pr'}):
            i += 1
    
            temp = a.find('span', attrs={'class':'i-b text ellipsis'})
            if temp.text == "Vistara Premium Economy":
                temp_name = "Vistara"
            else:
                temp_name = temp.text
    
            temp = a.find('div', attrs={'class':'i-b pr'})
            temp_stime = temp.text[:5]
    
            temp = a.find('p', attrs={'class':'bold fs-15 mb-2 pr time'})
            temp_rtime = temp.text[:5]
    
            temp = a.find('p', attrs={'class':'fs-12 bold du mb-2'})
            temp_duration = temp.text

            temp = a.find('p', attrs={'class':'i-b tipsy fare-summary-tooltip fs-18'})
            temp_price = temp.text
    
            k = 0
            for j in range(len(fname)):
                if(temp_name.strip().lower() == fname[j].strip().lower() and temp_stime.strip() == stime[j].strip() and temp_rtime.strip() == rtime[j].strip()):
                    yatra_price[j] = temp_price
                    k = 1
                    break
        
            if k == 0:
                fname.append(temp_name)
                stime.append(temp_stime)
                rtime.append(temp_rtime)
                duration.append(temp_duration)
                paytm_price.append("Not Found")
                yatra_price.append(temp_price)
                goibibo_price.append("Not Found")
    except:
        driver.quit()

#Goibibo

i = 0

temp_name = []
temp_stime = []
temp_rtime = []
temp_price = []
temp_duration = []

link = "https://www.goibibo.com/flights/air-"+fcode.upper()+"-"+tcode.upper()+"-"+year+month+date+"--1-0-0-E-D/"
print(link)

driver = webdriver.Chrome(executable_path=r'C:\xampp\htdocs\test2\chromedriver.exe')
driver.implicitly_wait(20)
try:
    driver.get(link)
except:
    driver.quit()
    exit(0)

try:
    driver.find_element_by_xpath("//div[@class='marginB10']")
 
    # Get scroll height
    for x in range(1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.45)")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.60)")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.75)")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.85)")
        time.sleep(1)

    temp = driver.find_elements_by_xpath("//span[@class='ico13 padR10 padL5']")
    for x in temp:
        xx = x.text.split(",")[0]
        if xx.strip() == "Emirates Airline":
            temp_name.append("Emirates")
        elif xx.strip() == "AirAsia India":
            temp_name.append("Air Asia")
        elif xx.strip() == "Vistara Premium Economy":
            temp_name.append("Vistara")
        else:
            temp_name.append(xx)
    
    temp = driver.find_elements_by_xpath("//span[@data-cy='depTime']")
    for x in temp:
        temp_stime.append(x.text)
    
    temp = driver.find_elements_by_xpath("//span[@data-cy='arrTime']")
    for x in temp:
        temp_rtime.append(x.text)

    temp = driver.find_elements_by_xpath("//div[@data-cy='duration']")
    for x in temp:
        temp_duration.append(x.text)   

    temp = driver.find_elements_by_xpath("//span[@data-cy='finalPrice']")
    for x in temp:
        temp_price.append(x.text)
    
    driver.quit()

    for tt in range(len(temp_name)):
        k = 0
        for j in range(len(fname)):
            if(temp_name[tt].strip().lower() == fname[j].strip().lower() and temp_stime[tt].strip() == stime[j].strip() and temp_rtime[tt].strip() == rtime[j].strip()):
                goibibo_price[j] = temp_price[tt]
                k = 1
                break
        
        if k == 0:
            fname.append(temp_name[tt])
            stime.append(temp_stime[tt])
            rtime.append(temp_rtime[tt])
            duration.append(temp_duration[tt])
            paytm_price.append("Not Found")
            yatra_price.append("Not Found")
            goibibo_price.append(temp_price[tt])
except:    
    driver.quit()
    
for i in range(len(fname)):
    print(fname[i]+"\n"+stime[i]+"\n"+rtime[i]+"\n"+duration[i]+"\n"+paytm_price[i]+"\n"+yatra_price[i]+"\n"+goibibo_price[i])