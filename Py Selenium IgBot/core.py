"""
core
"""
from instagramUserInfo import UserInfo
import time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

class Ig(UserInfo):
    """
    represents each account
    """
    PATH = ""
    def __init__(self):
        """
        required variables for each class
        :return: None
        """
        # self.username = username
        # self.password = password
        # self.random_copy_user = random_copy_user
        self.follower_list = []
        self.unfollower_list = []
        self.follow_counter = 0
        self.unfollow_counter = 0
        self.from_private = 0
        self.from_follow = 0
        self.from_business = 0
        self.from_name = 0
        self.already_follow = 0
         
    def openBrowser(self):
        """
        opens tab for selenium
        :return: None
        """
        self.browser_profile = webdriver.ChromeOptions()
        self.browser_profile.add_experimental_option("prefs" , {"intl.accept_languages":"en,en_US"})
        self.browser = webdriver.Chrome(self.PATH , chrome_options=self.browser_profile)

    def login(self):
        """
        login and log in to the site
        :return: None
        """
        self.browser.get("https://www.instagram.com/accounts/login/")
        try:
            WebDriverWait(self.browser , 15 ).until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input")))
        except:
            pass
        self.browser.find_element_by_css_selector("#loginForm > div > div:nth-child(1) > div > label > input").send_keys(self.username)
        self.browser.find_element_by_css_selector("#loginForm > div > div:nth-child(2) > div > label > input").send_keys(self.password + Keys.ENTER)
        time.sleep(3)

    def getFollowers(self , max , copyUser):
        """
        gets accounts to be followed
        :param max:
        :param copyUser:
        :return: None
        """
        time.sleep(3)
        try:    
            self.browser.get(f"https://www.instagram.com/{copyUser}/")
            try:
                WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span")))
            except:
                pass
            self.browser.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(2) > a").click()          
            try:
                WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='f1fd5e5cc921d2c']/div/div/span/a")))
            except:
                pass
            dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
            follower_count = len(dialog.find_elements_by_css_selector("li"))

            print(f"first count: {follower_count}")

            action = webdriver.ActionChains(self.browser)            
            dialog.click()

            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            
            dialog.click()

            while follower_count < max:
                dialog.click()
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                time.sleep(1)

                new_count = len(dialog.find_elements_by_css_selector("li"))

                if follower_count != new_count:
                    follower_count = new_count
                    print(f"new count: {new_count}")
                else:
                    break
            
            followers = dialog.find_elements_by_css_selector("li")
            print("__________Accounts to follow__________")
            i = 0
            for user in followers:
                link = user.find_element_by_css_selector("a").get_attribute("href")  
                print(link)          
                self.follower_list.append(link)            
                i += 1
                if i == max:
                    break

            # to save followed users to the file
            with open("followers.txt", "w",encoding="UTF-8") as file:
                for item in self.follower_list:
                    file.write(item.split("/")[3] + "\n")
        except:
            self.banDetection()
              
    def follow(self):
        """
        clicks the follow button and checks
        :return: None
        """
        try:
            for i in self.follower_list:
                user = i.split("/")[3]
                if self.check(user) == True:
                    self.browser.get("https://www.instagram.com/{0}/".format(user))
                    try:
                        WebDriverWait(self.browser , 2 ).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR ,
                             "#react-root > section > main > div > header > section > div.nZSzR > div.BY3EC > div > span > span.vBF20._1OSdk > button")))
                    except:
                        pass
                    if self.browser.find_element_by_tag_name("button").text != "Mesaj Gönder":
                        self.browser.find_element_by_tag_name("button").click()
                        self.follow_counter +=1
                    else:
                        self.already_follow +=1
        except:
            self.banDetection()
    
    def check(self , user):
        """
        takes the account information to be followed and
         checks with the determined values
        :param user:
        :return: Bool
        """
        self.browser.get(f"https://www.instagram.com/{user}/?__a=1")
        try:
            WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located((By.XPATH, "/html/body/pre")))
        except:         
            pass
        try:
            html = self.browser.find_element_by_xpath("/html/body/pre")
            user_info_dict = json.loads(html.text)
      
            is_private_account = user_info_dict['graphql']['user']['is_private']
            if is_private_account == True:
                self.from_private +=1
                return False

            is_business_account = user_info_dict['graphql']['user']['is_business_account']
            if is_business_account == True:
                self.from_business +=1
                return False

            full_name = user_info_dict['graphql']['user']['full_name']
            black_names_list = ["jpg" , "business" , "admin" , "meme" , "fan" , "page" , "fashion" , "cat" , "dog" ,
                "music" , "photo" , "moments" , "ig" , "travel" , "health" , "hot" , "girl" , "nature" , "sexy" , 
                "account" , "best" , "quotes" , "ladie" , "car" , "tik" , "tok" , "women" , "fit" , "bird" , "money" ,
                "personal" , "blog" , "edit" , "stuff" , "art" , "food" , "funny" , "funy" , "cute" , "anime" , "life" ,
                "hd" , "men" , "lux" , "home" , "moment" , "love"]
            x = full_name.split()
            for i in x:
                if i.lower() in black_names_list:
                    self.from_name +=1
                    return False
            
            bookmark = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
                "Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h",
                "i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
                "0","1","2","3","4","5","6","7","8","9","_",".","-",","]
            for i in bookmark:
                x_1 = user.split(i)
                for i in x_1:
                    if i in black_names_list:
                        self.from_name +=1
                        return False

            followers = user_info_dict['graphql']['user']['edge_followed_by']['count']
            that_person_follows = user_info_dict['graphql']['user']['edge_follow']['count']
            if followers > 3000 or followers < 10 or that_person_follows < 10 or that_person_follows > 2000:
                self.from_follow +=1
                return False
            else:
                return True    
        except:
            self.banDetection()

    def unfollow(self):
        """
        clicks the follow button and checks
        :return: None
        """
        try:
            for i in self.unfollower_list:
                user = i.split("/")[3]
                self.browser.get(f"https://www.instagram.com/{user}/")
                try:
                    WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR ,
                         "#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div:nth-child(2) > div > span > span.vBF20._1OSdk > button"
                         )))
                except:
                    pass

                unFollowButton = self.browser.find_element_by_css_selector(
                    "#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div:nth-child(2) > div > span > span.vBF20._1OSdk > button")
                unFollowButton.click()
                try:
                    WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[1]")))
                except:         
                    pass
                self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
                self.unfollow_counter +=1
        except:
            print("unfollow bozuldu")
            self.banDetection()

    def getFollowUp(self , max , myAccount):
        """
        gets the desired number of followers from the main account
        :param max:
        :param myAccount:
        :return: None
        """
        time.sleep(3)
        try:    
            self.browser.get(f"https://www.instagram.com/{myAccount}/")
            try:
                WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span")))
            except:
                pass
            self.browser.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(3) > a").click()          
            try:
                WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='f1fd5e5cc921d2c']/div/div/span/a")))
            except:
                pass
            dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
            follower_count = len(dialog.find_elements_by_css_selector("li"))

            print(f"first count: {follower_count}")

            action = webdriver.ActionChains(self.browser)            
            #dialog.click()
            self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li[1]").click()

            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li[6]").click()
            #dialog.click()

            while follower_count < max:
                dialog.click()
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                time.sleep(1)

                new_count = len(dialog.find_elements_by_css_selector("li"))

                if follower_count != new_count:
                    follower_count = new_count
                    print(f"new count: {new_count}")
                else:
                    break
            
            followers = dialog.find_elements_by_css_selector("li")
            print("__________Accounts to unfollow__________")
            i = 0
            for user in followers:
                link = user.find_element_by_css_selector("a").get_attribute("href")  
                print(link)          
                self.unfollower_list.append(link)            
                i += 1
                if i == max:
                    break

            # with open("followers.txt", "w",encoding="UTF-8") as file:
            #     for item in self.follower_list:
            #         file.write(item.split("/")[3] + "\n")
        except:
            self.banDetection()
    
    def selfControl(self):
        """
        checks the main account
        :return: Bool
        """
        self.browser.get(f"https://www.instagram.com/{self.username}/?__a=1")
        try:
            WebDriverWait(self.browser , 5 ).until(EC.presence_of_element_located((By.XPATH, "/html/body/pre")))
        except:         
            pass
        try:
            html = self.browser.find_element_by_xpath("/html/body/pre")
            user_info_dict = json.loads(html.text)
        
            followers = user_info_dict['graphql']['user']['edge_followed_by']['count']
            that_person_follows = user_info_dict['graphql']['user']['edge_follow']['count']
            if followers > 3000:
                self.done()
            elif that_person_follows < 600:
                return False
        except:
            self.banDetection()
        
    def out(self):
        """
        closes the opened tab and prints the checklist
        :return: None
        """
        self.counter()
        self.browser.close()

    def banDetection(self):
        """
        suspend the main account when detecting ban
        :return: None
        """
        print("ban detection")
        # there will be no transaction for 2 hours for the banned account
    
    def counter(self):
        """
        creates checklist
        :return: None
        """
        print("number of unfollowed accounts =" , self.unfollow_counter)
        print("number of followed accounts   =" , self.follow_counter)
        print("from private  =" , self.from_private)
        print("from follow   =" , self.from_follow)
        print("from business =" , self.from_business)
        print("from name     =" , self.from_name)
        print("already following =" , self.already_follow)
        self.follow_counter = 0
        self.unfollow_counter = 0
        self.from_private = 0
        self.from_follow = 0
        self.from_business = 0
        self.from_name = 0
        self.already_follow = 0
    
    def done(self):
        print("-------------------------------------Done------------------------------------------")


    def main(self):
        """
        main
        :return: None
        """
        t0 = time.clock()
        self.openBrowser()
        self.login()
        #if self.selfControl() != True:
            #self.getFollowUp(20 , self.username)
            #self.unfollow()
        self.getFollowers(100, self.random_copy_user)
        self.follow()
        self.out()
        t1 = time.clock()
        print(f"t0 is {t0}")
        print(f"t1 is {t1}")
        print(f"total time {t1 - t0}")
    

# loop for work with multiple accounts in a row
bot1 = Ig()
user_list = ["", ""]  # account names
password = ""  # this is a variable assignment, keep it blank
for user in user_list:
    file1 = open("passwords.txt" , "r+")
    list1 = file1.readlines()
    file1.close()
    for acc in list1:
        if user == acc.split(",")[0]:
            password = acc.split(",")[1]
    bot1.getCopy(user , password)
    bot1.main()