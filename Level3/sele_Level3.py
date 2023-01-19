import imaplib
import email
import fileinput
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

def getUserAndPass():
    user = []
    password = []
    for line in fileinput.input(files ='Hotmailbox-data-txt.txt'):
        us, pas = line.split('|')
        user.append(us)
        password.append(pas[:len(pas)-1])
    return user, password
def getBody(messages):
    if messages.is_multipart():
        body = getBody(messages.get_payload(0))
        return body.decode('utf-8', errors='ignore')
    else:
        return messages.get_payload(None, True)
def getLink(body):
    link = re.findall("href=[\"\'](.*?)[\"\']", body)[0]
    return link.replace('amp;', '')
def veriEmail(driver, user, password):
    host = 'imap-mail.outlook.com'
    imap = imaplib.IMAP4_SSL(host)
    imap.login(user, password)
    imap.select('Inbox')

    tmp, messages = imap.search(None, 'ALL')
    num = messages[0].split()
    msgnum = num[len(num) - 1]
    tmp, data = imap.fetch(msgnum, "(RFC822)")

    message = email.message_from_bytes(data[0][1])
    
    print(f"From: {message.get('From')}")
    print(f"To: {message.get('To')}")
    print(f"Date: {message.get('Date')}")
    
    body = getBody(message)
    body = body.decode('utf-8')
    if 'kteam' not in body:
        link = None
        print(body)
        return 
    else:
        link = getLink(body)
    print('Link: ', link)
    driver.get(link)
    print('Confirm Link Successful')
    imap.close()
    imap.logout()
def get_KeyAPI():
    f = open('keyAPI.txt')
    keyAPI = f.read()
    return keyAPI

def get_siteKey(driver):
    element = driver.find_element(By.CSS_SELECTOR, "#registerForm > fieldset > div:nth-child(6) > button")
    sitekey = element.get_attribute('data-sitekey')
    return sitekey


def solve_Captcha(REQ_URL, url, keyAPI, sitekey):
    payload = {
        'key': keyAPI,
        'method': 'userrecaptcha',
        'googlekey': sitekey,
        'pageurl': url,
        'here': 'now'
    }
    response = requests.post(REQ_URL, data=payload)
    return response
def get_gCaptcha(RES_URL, keyAPI, id):
    payload = {
        'key': keyAPI,
        'action': 'get',
        'id': id
    }
    response = requests.post(RES_URL, data = payload)
    if response.text == 'CAPCHA_NOT_READY':
        print('CAPTCHA NOT READY. Try again in 30s.')
        sleep(30)
        gCaptcha = get_gCaptcha(RES_URL, keyAPI, id)
        return gCaptcha
    if 'OK' in response.text:
        gCaptcha = response.text.split('|')[1]
        return gCaptcha
    else:
        print('Get gCaptcha Failed')
        print(response.text)
        return None
def captcha(url, keyAPI, sitekey):
    BASE_URL = 'http://azcaptcha.com'
    REQ_URL = BASE_URL + '/in.php'
    RES_URL = BASE_URL + '/res.php'
    print('Solving Captcha ...')
    response = solve_Captcha(REQ_URL, url, keyAPI, sitekey)
    if 'OK' in response.text:
        id = response.text.split('|')[1]
        sleep(30)
        gCaptcha = get_gCaptcha(RES_URL, keyAPI, id)
        print('Solve Captcha Successful')
        return gCaptcha
    else:
        print('Solve Captcha Failed')
        print(response.text)

def register(driver, email, userName, password, g_captcha):
    try:
        password = password + '@K'
        element_Email = driver.find_element(By.CSS_SELECTOR, '#Email')
        element_Email.send_keys(email)
        element_UserName = driver.find_element(By.CSS_SELECTOR, '#UserName')
        element_UserName.send_keys(userName)
        element_Password = driver.find_element(By.CSS_SELECTOR, '#Password')
        element_Password.send_keys(password)
        element_RePassword = driver.find_element(By.CSS_SELECTOR, '#ConfirmPassword')
        element_RePassword.send_keys(password)
        btn_Register = driver.find_element(By.CSS_SELECTOR, '#registerForm > fieldset > div:nth-child(6) > button')
        btn_Register.click()

        g_captcha_response = 'document.getElementById("g-recaptcha-response").innerHTML="{gcaptcha}";'.format(gcaptcha = g_captcha)
        driver.execute_script(g_captcha_response);
        driver.execute_script("onRegister('token');");

        print('Register Successful')
        sleep(10)
    except Exception as error:
        print('Register Failed')
        print(error)


emailUserList, passwordList = getUserAndPass()
for i in range(7, len(emailUserList)):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://howkteam.vn/account/register")

    emailUser = emailUserList[i]
    password = passwordList[i]
    print('Email: ', emailUser)
    print('Password: ', password)

    url = 'https://howkteam.vn/account/register'

    keyAPI = get_KeyAPI()
    sitekey = get_siteKey(driver)

    g_captcha = captcha(url, keyAPI, sitekey)
    userName = 'KietKP'+str(i+1)
    register(driver, emailUser, userName, password, g_captcha)
    veriEmail(driver, emailUser, password)
    a = input('Enter to Continue Account...')
