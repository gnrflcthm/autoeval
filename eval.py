from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from random import randrange
from credentials import USER, PASS

# Evaluation Strategies
RANDOM = 1
RANDOM_HIGH = 2
RANDOM_LOW = 3
ONES = 4
PERFECT = 5

MYUSTE = "https://myuste.ust.edu.ph/student"
MYUSTE_EVAL = "https://myuste.ust.edu.ph/student/evaluateelist?id=collegefaculty"

service = Service("chromedriver.exe")

driver = Chrome(service=service)

def generate_answer(strategy, choices_count):
    if strategy == RANDOM:
        return randrange(0, choices_count)
    elif strategy == RANDOM_HIGH:
        return randrange(0, 2)
    elif strategy == RANDOM_LOW:
        return randrange(choices_count - 2, choices_count - 1)
    elif strategy == ONES:
        return choices_count - 2
    else:
        return 0

def eval(strategy):
    form = driver.find_element(By.TAG_NAME, "form")
    questions = [x.find_element(By.TAG_NAME, "ul") for x in driver.find_elements(By.CLASS_NAME, "tdratingscale")]
    action = ActionChains(driver)
    for question in questions:
        choices = question.find_elements(By.TAG_NAME, "li")
        answer = generate_answer(strategy, len(choices))
        action.click(choices[answer].find_element(By.CLASS_NAME, "ratingtext"))
    action.perform()
    form.submit()
    Alert(driver).accept()

#main
try:

    driver.get(MYUSTE)
    driver.maximize_window()

    # Login
    user = driver.find_element(By.ID, 'txtUsername')
    password = driver.find_element(By.ID, 'txtPassword')
    form = driver.find_element(By.ID, 'form1')

    user.send_keys(USER)
    password.send_keys(PASS)

    form.submit()

    # Exit Program If Invalid Credentials
    if driver.current_url != "https://myuste.ust.edu.ph/student/studentcontrol":
        raise Exception("Invalid Login Credentials.")

    driver.get(MYUSTE_EVAL)

    prof_count = len(driver.find_elements(By.CLASS_NAME, "evaluatee"))

    for x in range(prof_count):
        profs = driver.find_elements(By.CLASS_NAME, "evaluatee")
        for prof in profs:
            # To check if already evaluated
            try:
                link = prof.find_element(By.TAG_NAME, "a")
                link.click()
                eval(RANDOM_HIGH)   # You can Update Strategy Accordingly
            except:
                continue
    sleep(1)
except Exception:
    print(Exception.with_traceback())
finally:
    driver.close()
