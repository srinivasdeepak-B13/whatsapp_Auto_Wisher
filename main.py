import datetime
import time
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
'''
we use this take_input method , to take the input from the user 
user enters 'n' -> number of messages he wants to send
and the corresponding date,time,contact type, contact name/contact number, message he wants to send
'''
def take_input():
    global L
    n = int(input("Enter number of messages you want to send : "))
    for i in range(n):
        date = input("Enter Date(YYYY-MM-DD): ")
        for j in range(1):
            L = []
            L.append(int(input("Enter Hour in 24 hour format :")))
            L.append(int(input("Enter Minute:")))
            L.append(input("Enter Contact Type Saved/New :"))
            if L[-1]=='Saved':
                L.append(input("Enter contact name : "))
            else:
                L.append(input("Enter contact number with + and country code : "))
            L.append(input_message())
        events[date].append(L)

'''
we use this input_message method to take multiple or single lines of message input from the user
'''
def input_message():
    print(
        "Enter the message and use the symbol '~' to end the message:\nFor example: Hi, this is a test "
        "message~\n\nYour message: ")
    message = []
    done = False
    while not done:
        temp = input()
        if len(temp) != 0 and temp[-1] == "~":
            done = True
            message.append(temp[:-1])
        else:
            message.append(temp)
    message = "\n".join(message)
    return message

'''
we use this send_messages method to start sending msgs on a particular day
'''
def send_messages():
    global driver
    driver = webdriver.Edge("C:\\Users\\Public\\WebDrivers\\edgedriver_win32\\msedgedriver.exe")
    driver.implicitly_wait(15)
    for i in events:
        if i == date_today:
            events[i].sort()
            for j in events[i]:
                left_time = calculate_sleeptime(j[0], j[1])
                if left_time < 0:
                    print("Message cannot be sended")
                    break
                print("Sending msg for ", j[3], 'after ', left_time, 'seconds')
                time.sleep(left_time)
                if j[2] == 'Saved':
                    sendMessage_savedContact(j[3], j[4])
                else:
                    sendMessage_newContact(j[3], j[4])
        else:
            print("Cannot send the message today")

'''
we use this calculate_sleeptime method to calculate the difference between the current time and
the sending time of that msg, by calculating this difference we will know the sleep time
'''
def calculate_sleeptime(time_hour, time_min):
    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format")
    if time_hour == 0: time_hour = 24
    call_sec = (time_hour * 3600) + (time_min * 60)
    current_time = time.localtime()
    current_hour = current_time.tm_hour
    current_minute = current_time.tm_min
    current_second = current_time.tm_sec
    if current_hour == 0: current_hour = 24
    current_to_second = (current_hour * 3600) + (current_minute * 60) + current_second
    left_time = call_sec - current_to_second
    return left_time

'''
we use this message to send the msg to a saved contact
'''
def sendMessage_savedContact(target, msg):
    link = "https://web.whatsapp.com"
    driver.get(link)
    driver.implicitly_wait(30)
    ct = 0
    while ct != 5:
        try:
            user = driver.find_element_by_xpath("//span[@title='{}']".format(target))
            user.click()
            s = 1
            while s > 0:
                input_box = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]')
                type_msg_in_inputbox(input_box, msg)
                print("Message sent successfully")
                s -= 1
            break
        except Exception as e:
            ct += 1
            time.sleep(1)

'''
we use this method to send the msg to a phone number , that phone number should
contain the country code as well
'''
def sendMessage_newContact(phoneNumber, msg):
    try:
        link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(phoneNumber)
        driver.get(link)
        driver.implicitly_wait(15)
        s = 1
        while s > 0:
            input_box = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]')
            type_msg_in_inputbox(input_box, msg)
            print("Message sent successfully")
            s -= 1
    except Exception as e:
        print("Message not sent ", e)

'''
we use this method to type our text message into the whatsapp input text box
'''
def type_msg_in_inputbox(input_box, message):
    for ch in message:
        if ch == "\n":
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
        else:
            input_box.send_keys(ch)
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)


    
    
events = defaultdict(list)
date_today = str(datetime.date.today())
print(date_today)
take_input()
print(events)
send_messages()
