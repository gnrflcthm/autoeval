from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from random import randrange
from credentials import USER, PASS

# Evaluation Strategies
RANDOM = 1
RANDOM_HIGH = 2
RANDOM_LOW = 3
ONES = 4
PERFECT = 5

SSS = "https://esurvey.ust.edu.ph/userlogin"

service = Service("chromedriver.exe")

driver = Chrome(service=service)

def generate_answer(strategy: int, choices_count: int, ignore_not_applicable = True) -> int:
    if ignore_not_applicable:
        choices_count -= 1

    if strategy == RANDOM:
        return randrange(0, choices_count)
    elif strategy == RANDOM_HIGH:
        return randrange(0, 2)
    elif strategy == RANDOM_LOW:
        return randrange(choices_count - 2, choices_count)
    elif strategy == ONES:
        return choices_count - 2
    else:
        return 0

def eval(strategy: int):
    submit_btn = driver.find_element(By.XPATH, '//*[@id="tblSurveyQuestionId"]/p/input[2]')
    sections = driver.find_elements(By.CLASS_NAME, "survey-details")
    action = ActionChains(driver)
    for section in sections:
        table: WebElement = section.find_element(By.TAG_NAME, "table")
        questions = table.find_element(By.TAG_NAME, "tbody").find_elements(By.CLASS_NAME, "radio-col")
        for question in questions:
            choices = question.find_elements(By.TAG_NAME, "input")
            answer = generate_answer(strategy, len(choices))
            action.click(choices[answer])
        try:
            select = Select(table.find_element(By.TAG_NAME, "select"))
            answer = generate_answer(strategy, len(select.options) - 1)
            select.select_by_index(answer + 1)
        except:
            continue
    action.perform()
    submit_btn.click()

#main
if __name__ == "__main__":
    try:
        driver.get(SSS)
        driver.maximize_window()

        # Login
        user = driver.find_element(By.XPATH, '/html/body/section/div/div/div[2]/div/form/div[1]/input')
        password = driver.find_element(By.XPATH, '/html/body/section/div/div/div[2]/div/form/div[2]/input')
        form = driver.find_element(By.XPATH, '/html/body/section/div/div/div[2]/div/form')

        user.send_keys(USER)
        password.send_keys(PASS)

        form.submit()

        # Exit Program If Invalid Credentials
        if driver.current_url != "https://esurvey.ust.edu.ph/surveylist":
            raise Exception("Invalid Login Credentials.")

        # Open SSS Evalutaion
        sss_form_button = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div[2]/div/div/table/tbody/tr[1]/td[2]/form/button")
        sss_form_button.click()

        # Evaluate
        eval(RANDOM_HIGH)

        sleep(1)

    except Exception:
        print(Exception.with_traceback())

    finally:
        driver.close()
