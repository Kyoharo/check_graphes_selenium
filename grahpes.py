#Live_session - Availability - Oracle
from selenium  import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import WebDriverException
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.common.exceptions import NoSuchElementException
import os
import glob
import csv
from graphes_links import Live_session,Availability,Memory,Oracle,Thread_Pool,send_email



class InstaBot:
    def __init__(self,username,password):  
        #webdriver
        try:
            url = "https://presentation.egyptpost.local"
            serv_obj = service= Service(r'\\10.199.199.35\soc team\Abdelrahman Ataa\Graphes\check_graphes\geckodriver.exe')
            ops=webdriver.FirefoxOptions()
            #ops.headless=True        
            self.driver = webdriver.Firefox(service=serv_obj,options=ops)
            #launch
            self.driver.get(url)
            self.driver.implicitly_wait(20)
            alert_window= self.driver.switch_to.alert                    #to get the alert message to var
            alert_window.accept()      
        except Exception as e :
            print("Error", f"There is problem with geckodriver.exe or problem with internet \n  geckodriver هنالك مشكلة بالانترنت او بملف ")
            #try to use chromedriver instead
            try:
                serv_obj = service= Service(r'\\10.199.199.35\soc team\Abdelrahman Ataa\Graphes\check_graphes\chromedriver.exe')
                ops=webdriver.ChromeOptions()
                #ops.headless=True        
                self.driver = webdriver.Chrome(service=serv_obj,options=ops)
                #launch
                self.driver.get(url)
                self.driver.implicitly_wait(20)
                alert_window= self.driver.switch_to.alert                    #to get the alert message to var
                alert_window.accept()      
            except Exception as e :
                print("Error", f"There is problem with chromedriver.exe or problem with internet \n  chromedriver هنالك مشكلة بالانترنت او بملف ")
                return 
        try:
            self.username= username
            self.password= password
            self.driver.find_element(By.XPATH, '//input[@id="user_login"]').send_keys(username)
            sleep(1)
            #password
            self.driver.find_element(By.XPATH, '//input[@id="login_user_password"]').send_keys(password)
            sleep(1)
            #login
            self.driver.find_element(By.XPATH, '//button[@id="login-jsp-btn"]').click()
            sleep(1)
            self.driver.maximize_window()
            sleep(5)
        except Exception as e :
            print("Error","Username or password uncorrecty or can't reach the page \n هنالك مشكلة بالانترنت او ان الاميل أوالباسورد خطأ")
            return 
        
    def lastfile_name(self):
        download_folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
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


    def graphs_live_session(self,url):
        try:
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            self.driver.find_element(By.XPATH, "//label[@for='501948505']").click()                 #live session 
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            # date = self.driver.find_element(By.XPATH, "(//input[@placeholder='HH'])[2]")
            # date.send_keys(Keys.BACKSPACE,Keys.BACKSPACE)
            # date.send_keys("23")
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            self.driver.refresh()
            sleep(1)
            return  date 
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            print(e)
            return None 
        
    def graphes_Availability(self,url):
        try:
            # action_chains = ActionChains(self.driver)
            # action_chains.send_keys(Keys.ESCAPE,Keys.ESCAPE).perform()
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            self.driver.refresh()
            sleep(1)
            return  date      # get the last value in sec column 
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            print(e)
            return None 
        
    def graphs_Oracle(self,url):
        try:
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            self.driver.find_element(By.XPATH, "//label[@for='501940512']").click()                 #  unchecked Connections Created (#)
            self.driver.find_element(By.XPATH, "//label[@for='501940513']").click()                 #  unchecked 	Connections Destroyed (#) 
            self.driver.find_element(By.XPATH, "//label[@for='501940506']").click()                 #  Connection Pool Utilization (%)
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            self.driver.refresh()
            sleep(1)
            return  date 
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            print(e)
            return None 
        

    def graphs_Thread_Pool(self,url):
        try:
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            self.driver.find_element(By.XPATH, "//label[@for='501930510']").click()                 #Threads in Pool 
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            self.driver.refresh()
            sleep(1)
            return  date 
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            print(e)
            return None 
        
    def Memory(self,url,memory):
        try:
            self.driver.get(url)
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()      # tap click
            self.driver.find_element(By.XPATH, "//a[@class='ng-scope']").click()                    # edit
            self.driver.find_element(By.XPATH, "//label[@for='501978515']").click()                 #  unchecked Total memory 
            self.driver.find_element(By.XPATH, "//label[@for='501978516']").click()                 #  unchecked 	 Used Memory in JVM Runtime  
            self.driver.find_element(By.XPATH, "//label[@for='501978502']").click()                 #  unchecked 	 Free Memory in JVM Runtime  
            self.driver.find_element(By.XPATH, "//label[@for='501978511']").click()                 #  unchecked 	 The average percent of CPU usage since the last query
            self.driver.find_element(By.XPATH, memory).click()        #  unchecked 	 Percentage of Memory Used  OR Heap    
            self.driver.find_element(By.XPATH, "//input[@id='applyConfigButton']").click()          # apply
            self.driver.find_element(By.XPATH, "//span[@class='bmc-actionmenu dateTimeSelection dropdown']//a[@class='fi menuIcon fi-action-menu dropdown-toggle']").click()     # time tap
            self.driver.find_element(By.XPATH, "//a[@id='customTimeFilterId']").click()                 #customTimeFilterId
            self.driver.find_element(By.XPATH, "//table[contains(.,'End')]//button[@class='btn btn-default btn-sm btn-info active']/following::button[1]").click()       #next day
            self.driver.find_element(By.XPATH, "//button[contains(@class,'btn ng-isolate-scope btn-primary')]").click()         #apply
            self.driver.find_element(By.XPATH, "(//a[@aria-label=' [Click, tap or press ENTER to open]'])[1]").click()          # download button
            self.driver.find_element(By.XPATH, "//a[normalize-space()='CSV']").click()              # download csv 
            date = self.lastfile_name()
            self.driver.refresh()
            sleep(1)
            return  date 
        #except NoSuchElementException or StaleElementReferenceException as e :
        except Exception as e:
            print(e)
            return None 
        


    def Quit(self):
        self.driver.quit()






mybot=InstaBot("w_abdelrahman.ataa", "a1591997A!")
issues = {}
# #Live_session
for key, value in Live_session.items():
    Live_session_status = mybot.graphs_live_session(value)
    print(f"{key}: {Live_session_status}")
    if int(Live_session_status) >= 1800:
        issues[key] = Live_session_status

print("----------------------------------------------")
# #Availability
for key, value in Availability.items():
    Availability_status = mybot.graphes_Availability(value)
    print(f"{key}: {Availability_status}")
    if int(Availability_status) == 1:
        issues[key] = Availability_status
print("----------------------------------------------")
#Oracle
for key, value in Oracle.items():
    Oracle_status = mybot.graphs_Oracle(value)
    print(f"{key}: {Oracle_status}")
    if int(Oracle_status) > 80:
        issues[key] = Oracle_status
print("----------------------------------------------")

#Thread_Pool
for key, value in Thread_Pool.items():
    Thread_Pool_status = mybot.graphs_Thread_Pool(value)
    print(f"{key}: {Thread_Pool_status}")
    if int(Thread_Pool_status) > 133:
        issues[key] = Thread_Pool_status

print("----------------------------------------------")
# #Heap_Memory
# for key, value in Memory.items():
#     Heap_Memory_status = mybot.Memory(value,"//label[@for='501978509']")
#     key_Heap = f"{key}_Heap"
#     print(f"{key_Heap}: {Heap_Memory_status}")
#     if float(Heap_Memory_status) > 80.00:
#         issues[key_Heap] = Heap_Memory_status


# print("----------------------------------------------")
# #Memory_Used
# for key, value in Memory.items():
#     Memory_Used_status = mybot.Memory(value,"//label[@for='501978508']")
#     key_used = f"{key}_Used"
#     print(f"{key_used}: {Memory_Used_status}")
#     if float(Memory_Used_status) > 90.00:
#         issues[key_used] = Memory_Used_status
    
mybot.Quit()


print(issues)




#mail status
status = {}
txt_status = r'\\10.199.199.35\soc team\Abdelrahman Ataa\Graphes\check_graphes\status.txt'
try:
    with open(txt_status, "r") as f:
        for line in f:
            key, value = line.strip().split(":")
            status[key] = value
except Exception as e: 
    print(e)
    with open(r'\\10.199.199.35\soc team\Abdelrahman Ataa\Graphes\check_graphes\logs.txt', "a") as f:
        f.write(str(e) + "\n")    
print(status)
try:
    if issues == status:
        print("skip sending email")
    else:
        with open(txt_status, 'w') as file:
            for key, value in issues.items():
                file.write(f"{key}:{value}\n")
        if len(issues) == 0:
            down_service = 'All Graphes are working'
        else:
            down_service = '\n'.join([f"{key} : {value}" for key, value in issues.items()])
        content = f"Dear Soc Team,\n\nPlease check the status of Graphes below:\n{down_service}\n\nBR\nAbdelrahman Ataa\nSoc Engineer"
        print(content)
        send_email(content)

except Exception as e: 
    print(e)
    with open(r'\\10.199.199.35\soc team\Abdelrahman Ataa\Graphes\check_graphes\logs.txt', "a") as f:
        f.write(str(e) + "\n")