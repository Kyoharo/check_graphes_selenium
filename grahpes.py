#Live_session - Availability - Oracle
from graphes_links import Live_session,Availability,Memory,exchange,frontoffice,Oracle,Thread_Pool,recverence,send_email
from selenium  import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import concurrent.futures
import glob
import csv
from PIL import Image
import platform
import os
from dotenv import load_dotenv
from time import sleep

# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import WebDriverException
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.common.exceptions import NoSuchElementException


env_path = "C:\\env\\Graphs\\.env"  
load_dotenv(dotenv_path=env_path)
issues = {}
status = {}
screen_folder_path = os.getenv("screen_folder_path")


class InstaBot:
    def __init__(self, username, password,download_folder_name):
        self.download_folder_name = download_folder_name 
        user_home = os.path.expanduser("~")
        if platform.system() == "Windows":
            print("Windows")
            download_folder_path = os.path.join(user_home, download_folder_name)
        else:  # Linux or other platforms
            download_folder_path = os.path.join(os.path.expanduser("~"), download_folder_name)
        print(download_folder_path)
        if not os.path.exists(download_folder_path):
            os.makedirs(download_folder_path)
        url = "https://presentation.egyptpost.local"
        try:
            serv_obj = service= Service(os.getenv("geckodriver"))
            ops = FirefoxOptions()
            ops.set_preference("browser.download.folderList", 2)
            ops.set_preference("browser.download.manager.showWhenStarting", False)
            ops.set_preference("browser.download.dir", download_folder_path)
            ops.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            ops.add_argument('-width=1920')
            ops.add_argument('-height=1080')
            ops.headless = True
            # Create the Firefox driver with the configured options
            self.driver = webdriver.Firefox(service=serv_obj, options=ops)
            self.driver.get(url)
            self.driver.implicitly_wait(20)
            alert_window = self.driver.switch_to.alert
            alert_window.accept()

        except Exception as e:
            print("Error", "There is a problem with geckodriver.exe or the internet")
            try:
                chromedriver_path =os.getenv("chromedriver")
                serv_obj = ChromeService(executable_path=chromedriver_path)
                ops = webdriver.ChromeOptions()
                ops.headless = True
                prefs = {
                    "download.default_directory": download_folder_path,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True
                }
                ops.add_experimental_option("prefs", prefs)
                self.driver = webdriver.Chrome(service=serv_obj, options=ops)
                self.driver.get(url)
                self.driver.implicitly_wait(20)
                alert_window = self.driver.switch_to.alert
                alert_window.accept()
            except Exception as e:
                print("Error", "There is a problem with chromedriver.exe or the internet")
                return
            
        try:
            self.username = username
            self.password = password
            self.driver.find_element(By.XPATH, '//input[@id="user_login"]').send_keys(username)
            sleep(1)
            self.driver.find_element(By.XPATH, '//input[@id="login_user_password"]').send_keys(password)
            sleep(1)
            self.driver.find_element(By.XPATH, '//button[@id="login-jsp-btn"]').click()
            sleep(1)
            self.driver.maximize_window()
            sleep(5)
        except Exception as e:
            print("Error", "Username or password is incorrect or can't reach the page \n هنالك مشكلة بالانترنت او ان الاميل أو الباسورد خطأ")
            return
    
    def lastfile_name(self):
        download_folder_name = self.download_folder_name
        download_folder_path = os.path.join(os.path.expanduser("~"), download_folder_name)
        files_path = os.path.join(download_folder_path, '*')
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 
        mylastfile = files[0] 
        with open(mylastfile, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        # Get the last value of the second column
        last_value = data[-1][1]
        os.remove(mylastfile)
        return last_value
    
    def screen_shot(self,screen_name):
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        element = self.driver.find_element(By.XPATH, "(//section)[3]")  # Replace with your XPath expression
        location = element.location
        size = element.size
        self.driver.save_screenshot(f"{screen_folder_path}/screenshot.png")
        screenshot = Image.open(f"{screen_folder_path}/screenshot.png")
        extra_height=240
        left = location['x'] 
        top = location['y'] - extra_height
        right = location['x'] + size['width']
        bottom = location['y'] + size['height'] - 230
        element_screenshot = screenshot.crop((left, top, right, bottom))
        element_screenshot.save(f"{screen_folder_path}/{screen_name}.png")
        os.remove(f"{screen_folder_path}/screenshot.png")

    def graphs_live_session(self,key,url):
        try:
            start_input = {
            "KEY": key,
            "URL": url
            }
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            input_elements = self.driver.find_elements(By.XPATH, "(//div[@class='row metric-row'])[2]//label[1]/input")
            try:
                for input_element in input_elements:
                    if input_element.is_selected():
                        input_element.click()  # Click to unselect
            except Exception as e: 
                pass
            self.driver.find_element(By.XPATH, "//label[@for='501948505']").click()                 #live session 
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next da      
            self.driver.find_element(By.XPATH, "(//section)[3]")
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            print(f"{key}: {date}")
            if int(date) >= 1800:
                issues[key] = date
                self.screen_shot(key)
            self.driver.refresh()
            sleep(1)
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            self.graphs_live_session(self,
                                     start_input["KEY"],
                                      start_input["URL"])
        
    def graphes_Availability(self,key,url):
        try:
            start_input = {
            "KEY": key,
            "URL": url
            }
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            print(f"{key}: {date}")
            if int(date) == 1:
                issues[key] = date
                self.screen_shot(key)
            self.driver.refresh()
            sleep(1)
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            self.graphes_Availability(self,
                                     start_input["KEY"],
                                      start_input["URL"])
        
    def graphs_Oracle(self,key,url):
        try:
            start_input = {
            "KEY": key,
            "URL": url
            }
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            input_elements = self.driver.find_elements(By.XPATH, "(//div[@class='row metric-row'])[2]//label[1]/input")
            try:
                for input_element in input_elements:
                    if input_element.is_selected():
                        input_element.click()  # Click to unselect
            except Exception as e: 
                pass
            self.driver.find_element(By.XPATH, "//label[@for='501940506']").click()                 #  Connection Pool Utilization (%)
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            print(f"{key}: {date}")
            if int(date) > 80:
                issues[key] = date
                self.screen_shot(key)
            self.driver.refresh()
            sleep(1)
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            self.graphs_Oracle(self,
                                                start_input["KEY"],
                                                start_input["URL"])
        

    def graphs_Thread_Pool(self,key,url):
        try:
            start_input = {
            "KEY": key,
            "URL": url
            }
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            input_elements = self.driver.find_elements(By.XPATH, "(//div[@class='row metric-row'])[2]//label[1]/input")
            try:
                for input_element in input_elements:
                    if input_element.is_selected():
                        input_element.click()  # Click to unselect
            except Exception as e: 
                pass
            self.driver.find_element(By.XPATH, "//label[@for='501930510']").click()                 #Threads in Pool 
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            print(f"{key}: {date}")
            if int(date) > 132:
                issues[key] = date
                self.screen_shot(key)
            self.driver.refresh()
            sleep(1)
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            self.graphs_Thread_Pool(self,
                                                start_input["KEY"],
                                                start_input["URL"])
        
    def Memory(self,key,url,memory):
        try:
            start_input = {
            "KEY": key,
            "URL": url,
            "MEMORY":memory
            }
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            input_elements = self.driver.find_elements(By.XPATH, "(//div[@class='row metric-row'])[2]//label[1]/input")
            try:
                for input_element in input_elements:
                    if input_element.is_selected():
                        input_element.click()  # Click to unselect
            except Exception as e: 
                pass
            self.driver.find_element(By.XPATH, memory).click()        #check Percentage of Memory Used  OR Heap    
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            print(f"{key}: {date}")
            if float(date) > 90.00:
                issues[key] = date
                self.screen_shot(key)
            self.driver.refresh()
            sleep(1)
            
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            self.Memory(self,
                                                start_input["KEY"],
                                                start_input["URL"],
                                                start_input["MEMORY"])
    def ser_exchange(self,key,url,memory):
        try:
            start_input = {
            "KEY": key,
            "URL": url,
            "MEMORY":memory
            }
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            input_elements = self.driver.find_elements(By.XPATH, "(//div[@class='row metric-row'])[2]//label[1]/input")
            try:
                for input_element in input_elements:
                    if input_element.is_selected():
                        input_element.click()  # Click to unselect
            except Exception as e: 
                pass
            self.driver.find_element(By.XPATH, memory).click()        #check Percentage of Memory Used  OR Heap    
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            print(f"{key}: {date}")
            if float(date) > 80.00:
                issues[key] = date
                self.screen_shot(key)
            self.driver.refresh()
            sleep(1)
            
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            self.Memory(self,
                                                start_input["KEY"],
                                                start_input["URL"],
                                                start_input["MEMORY"])

    def ser_front_Login(self,key,url):
        try:
            start_input = {
            "KEY": key,
            "URL": url
            }
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            # self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            # input_elements = self.driver.find_elements(By.XPATH, "(//div[@class='row metric-row'])[2]//label[1]/input")
            # try:
            #     for input_element in input_elements:
            #         if input_element.is_selected():
            #             input_element.click()  # Click to unselect
            # except Exception as e: 
            #     pass
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            print(f"{key}: {date}")
            if int(date) > 1800 or  int(date) == 0: 
                issues[key] = date
                self.screen_shot(key)
            self.driver.refresh()
            sleep(1)
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            self.graphs_Thread_Pool(self,
                                                start_input["KEY"],
                                                start_input["URL"])


    def Quit(self):
        self.driver.quit()






username = os.getenv("name")
passwd =  os.getenv("passwd")
download_location01= os.getenv("download_location01")
download_location02= os.getenv("download_location02")

print(f"{username}: {passwd}")

def fun1():
    try:
        mybot=InstaBot(username, passwd,download_location01)
        # # #Live_session
        for key, value in Live_session.items():
            mybot.graphs_live_session(key, value)


        print("----------------------------------------------")
        # #Availability
        for key, value in Availability.items():
            mybot.graphes_Availability(key, value)

        print("----------------------------------------------")
        #Oracle
        for key, value in Oracle.items():
            mybot.graphs_Oracle(key, value)

        print("----------------------------------------------")
        #exchange processor
        for key, value in exchange.items():
            mybot.ser_exchange(key, value,"//label[@for='501024505']")
        print("----------------------------------------------")
        #exchange memory
        for key, value in exchange.items():
            mybot.ser_exchange(key, value,"//label[@for='501024502']")
            
        mybot.Quit()

    except Exception as e: 
        print("Exception")
        mybot.Quit()

#------------------------------------------------------------------------------------------------------------------------------
    
    print("----------------------------------------------")
def fun2():
    try:
        mybot1=InstaBot(username, passwd,download_location02)
        #Thread_Pool
        for key, value in Thread_Pool.items():
            mybot1.graphs_Thread_Pool(key, value)

        print("----------------------------------------------")
        #Heap_Memoryx
        for key, value in Memory.items():
            mybot1.Memory(key, value,"//label[@for='501978508']")


        print("----------------------------------------------")
        #Memory_Used
        for key, value in Memory.items():
            mybot1.Memory(key, value,"//label[@for='501978509']")

        #Front
        for key, value in frontoffice.items():
            mybot1.ser_front_Login(key, value)

        mybot1.Quit()
    except Exception as e: 
        print("Exception")
        mybot1.Quit()



with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_fun1 = executor.submit(fun1)
    future_fun2 = executor.submit(fun2)

    # Wait for both tasks to complete
    concurrent.futures.wait([future_fun1, future_fun2])

print("Both fun1 and fun2 have completed.")






all_urls = {**Live_session, **Availability, **Memory, **Oracle, **Thread_Pool, **exchange, **frontoffice}
txt_status = os.getenv("txt_status")
logs= os.getenv("logs")

try:
    with open(txt_status, "r") as f:
        for line in f:
            key, value = line.strip().split(":")
            status[key] = value
except Exception as e: 
    print(e)
    with open(logs, "a") as f:
        f.write(str(e) + "\n")   

print(f"status: {status}")
print(f"issues: {issues}")

try:
    if set(status.keys()) == set(issues.keys()):
        print("skip sending email")
        for filename in os.listdir(screen_folder_path):
            if filename.lower().endswith('.png'):
                file_path = os.path.join(screen_folder_path, filename)
                os.remove(file_path)
    else:
        print("gonna send mail")
        with open(txt_status, 'w') as file:
            for key, value in issues.items():
                file.write(f"{key}:{value}\n")
        if len(issues) == 0:
            down_service = 'All Graphs are working'
            content = f"Dear Soc Team,<br><br>Please check the status of Graphs below:<br>{down_service}<br><br>BR<br>Abdelrahman Ataa<br>Soc Engineer"
            send_email(content, screen_folder_path)
        else:
            formatted_issues = []
            for key, value in issues.items():
                        if key in all_urls:
                            url = all_urls[key]
                            hyperlink = f'<a href="{url}">{key}</a>'
                            formatted_issues.append(f"{hyperlink}: {value}")
                        else:
                            formatted_issues.append(f"{key}: {value}")
            if len(formatted_issues) > 0:
                print(f"formatted_issues: {formatted_issues}")
                down_service = '<br>'.join(formatted_issues)
                content = f"Dear Soc Team,<br><br>Please check the status of Graphs below:<br>{down_service}<br><br>{recverence}<br>BR<br>Abdelrahman Ataa<br>Soc Engineer"
                send_email(content, screen_folder_path)               
        for filename in os.listdir(screen_folder_path):
            if filename.lower().endswith('.png'):
                file_path = os.path.join(screen_folder_path, filename)
                os.remove(file_path)

except Exception as e: 
    print(e)
    with open(logs, "a") as f:
        f.write(str(e) + "\n")