from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from sys import argv
from getpass import getpass


#Get user Input
def userInput():
    while True:
        EMAIL = input("Enter your Email: ").strip()
        PASSWORD = getpass("Enter your password: ")
        choice = 'y'
        while True:
            choice = input("Do you want to view your password?y/n\n")
            if (choice == 'y'):
                print(PASSWORD)
                choice = input("Do you want to change your password?y/n")
                if (choice == 'y'):
                    PASSWORD = getpass("Enter your password")
            break
        break

    return EMAIL, PASSWORD
    


driver = webdriver.Chrome('chromedriver.exe')


#chrome_options = Options()
#chrome_options.add_argument("--incognito")
def login(EMAIL, PASSWORD):
    
    driver.get("https://strive-ttu.campus.eab.com/home/staff")
    #driver.set_window_size(1200,1200)

    userName = driver.find_element_by_id("userNameInput")
    passWord = driver.find_element_by_id("passwordInput")

    #Perform login

    userName.send_keys(EMAIL)
    passWord.send_keys(PASSWORD)
    passWord.send_keys(Keys.RETURN)
# Go to staff profile and select each element


def fillForm(final, rowCount):
    '''
    Select the student ID
    Click on Actions and Add appointment summary
    Fill out details
    '''
    #Step 1
    driver.find_element_by_xpath(final+"[{}]/td[1]".format(rowCount)).click()

    #Step 2
    
    action = driver.find_element_by_xpath("//*[@id=\"recent_appointments\"]/div[3]/div[1]/a").click()

    driver.find_element_by_xpath("//*[@id=\"action-list-name--1\"]/div[1]/a").click()
    
    time.sleep(7)  #Wait for the iframe to load

    #Step 3
    
    homework = driver.find_element_by_xpath("//*[@id=\"evaluation_assignment_description\"]")
    homework.send_keys("Homework")

    driver.switch_to.frame(driver.find_element_by_xpath("//*[@id=\"evaluation_comment_ifr\"]"))
    
    elem_iframe = driver.find_element_by_xpath("/html/body/p")
    elem_iframe.send_keys("Assisted student with their academic needs during their visit.")

    driver.switch_to.default_content()

    #Submit the form

    driver.find_element_by_xpath("//*[@id=\"submit_button\"]").click()
    
    

    
def checkBox():
    
    final = "//*[@id=\"recent_appointments\"]/div[4]/table/tbody/tr"
    check_id = driver.find_elements_by_xpath(final)     
    value = len(check_id) + 1
    for i in range(1, value):
        if (driver.find_element_by_xpath(final+"[{}]/td[9]".format(i)).get_attribute("class") == "c"):
            #Start filling the form
            print("Incomplete report found")
            fillForm(final, i)
            driver.refresh()
        else:
            print ("Report Completed")


def movePage():
    page_limit = int(input("How many pages have incomplete reports?"))

    number_of_pages = int(driver.find_element_by_xpath("//*[@id=\"recent_appointments\"]/div[5]/div[1]/a[contains(text(),'Next')]/preceding-sibling::a[1]").text)
    
    while True:
        if (page_limit > number_of_pages):
            print("Bro you don't have that many reports. You have {} number of pages".format(number_of_pages))
            page_limit = int(input("How many pages have incomplete reports?"))
        else:
            break

    for i in range(1, page_limit+1):
        checkBox()
        if (i+1 <=number_of_pages):
            driver.find_element_by_xpath("//*[@id=\"recent_appointments\"]/div[5]/div[1]/a[contains(text(),'{}')]".format(i+1)).click()
            time.sleep(3)  #Wait for the page to load

    driver.close()




def main():
    email, password = userInput()
    login(email, password)
    movePage()
    

if __name__ == "__main__":
    main()


