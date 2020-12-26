"""
automatically retrieves the photo or video from the file and shares it
"""

import autoit
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


userlist = ["", ""]
PATH = ""

def login(driver , username , password):
    try:
        WebDriverWait(driver , 3 ).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='react-root']/section/main/article/div/div/div/div[2]/button")))
    except:
        pass
    #sleep(2)
    driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/div[2]/button").click()
    try:
        WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,"//input[@name='username']")))
    except:
        pass
    driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.send_keys(password)
    password_input.submit()
    #sleep(2)

def close_reactivated(driver):
    try:
        try:
            WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,"//*[@id='react-root']/section/main/div/div/div/button")))
        except:
            pass
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/button").click()       
    except:
        pass

def close_notification(driver):
    try: 
        try:
            WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div/div/div/div[3]/button[2]")))
        except:
            pass
        close_noti_btn = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
        close_noti_btn.click()
    except:
        pass

# def close_add_to_home():
#     sleep(3) 
#     close_addHome_btn = driver.find_element_by_xpath("//button[contains(text(),'Cancel')]")
#     close_addHome_btn.click()
#     sleep(1)

def openPath(driver , image_path):
    try:
        WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,"//div[@role='menuitem']")))
    except:
        pass
    driver.find_element_by_xpath("//div[@role='menuitem']").click()
    sleep(1.5)
    autoit.win_active("Aç")
    autoit.win_wait_active("Aç" , 3)
    autoit.control_send("Aç","Edit1",image_path)
    sleep(1)
    autoit.control_send("Aç","Edit1","{ENTER}")

def share(driver , caption):
    try:
        WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,"//*[@id='react-root']/section/div[2]/div[2]/div/div/div/button[1]/span")))
    except:
        pass
    driver.find_element_by_xpath("//*[@id='react-root']/section/div[2]/div[2]/div/div/div/button[1]/span").click()
    try:
        WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,
            "//*[@id='react-root']/section/div[1]/header/div/div[2]/button")))
    except:
        pass
    driver.find_element_by_xpath("//*[@id='react-root']/section/div[1]/header/div/div[2]/button").click()

    try:
        WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,
            "//*[@id='react-root']/section/div[2]/section[1]/div[1]/textarea")))
    except:
        pass

    driver.find_element_by_xpath("//*[@id='react-root']/section/div[2]/section[1]/div[1]/textarea").send_keys(caption)

    try:
        WebDriverWait(driver , 3 ).until(EC.presence_of_element_located((By.XPATH,
            "//*[@id='react-root']/section/div[1]/header/div/div[2]/button")))
    except:
        pass

    driver.find_element_by_xpath("//*[@id='react-root']/section/div[1]/header/div/div[2]/button").click()

def close(driver):
    sleep(5)
    driver.close()

def main():
    try:
        for username in userlist:
            file1 = open("passwords.txt" , "r+")
            list1 = file1.readlines()
            file1.close()
            for acc in list1:
                if username == acc.split(",")[0]:
                    password = acc.split(",")[1]

            file1 = open(f"{PATH}\\{username}\\control.txt" , "r")
            lines = file1.readlines()
            photo_path = lines[0]
            photo_path = photo_path[:-1]
            lines.remove(lines[0])
            file1.close()

            file2 = open(f"{PATH}\\{username}\\control.txt" , "w")
            for line in lines:
                file2.write(line)
            file2.close()

            image_path = f"{PATH}\\{username}\\{photo_path}.jpg"
            file1 = open(f"{PATH}\\{username}\\caption.txt", "r")
            caption = file1.readlines()

            #for specific explanation sections
            # if username == "":
            #     first_obj = caption[0]
            #     caption[0] = first_obj[:-1] + photo_path + "\n"

            mobile_emulation = { "deviceName": "Pixel 2" }
            opts = webdriver.ChromeOptions()
            opts.add_experimental_option("mobileEmulation", mobile_emulation)
            driver = webdriver.Chrome(executable_path=f"{PATH}\\chromedriver.exe",options=opts)
            main_url = "https://www.instagram.com"
            driver.get(main_url)

            login(driver , username , password)
            close_reactivated(driver)
            close_notification(driver)
            #close_add_to_home()
            openPath(driver , image_path)
            share(driver , caption)
            sleep(5)
            close(driver)
            print(f"{username} There was a problem on your account")
    except:
        print(f"{username} There was a problem on your account")
main()
print("Done")