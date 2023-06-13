from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tp_logger import logger

import time
import datetime as dt
import constants

#Global variables
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 30)
all_part_key = []
all_part_dict = {}
csv_title = []
delay_searching_time = [1, 1.2, 1.4, 1.6, 1.8, 2]
current_time = int(dt.datetime.now().timestamp() * 1000)

def searching_pn_automation():
    #init browser
    # driver = webdriver.Firefox()
    # wait = WebDriverWait(driver, 30)

    #Read csv file
    read_csv_file()

    #Init browser
    driver.get(constants.URL_DEFAULT)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    try:
        login_if_needed()

        search_part_number()

        logger.info("##### Searching done #####")

        driver.quit()
    except Exception as e:
        logger.error(f"Searching done with unknown error: %s", str(e))
        driver.quit()
    

def login_if_needed():
    logger.info("##### Login Step #####")
    currentURL = driver.current_url
    if currentURL.__contains__("/auth/login"):
        user = driver.find_element(By.XPATH, "//input[@inputid='username']")
        password = driver.find_element(By.XPATH, "//input[@inputid='password1']")

        user.send_keys(constants.USER_DEFAULT)
        password.send_keys(constants.PASSWORD_DEFAULT)

        signin_button = driver.find_element(By.XPATH, "//button[@aria-label='Sign In']")
        signin_button.click()
        time.sleep(1)

        login_timeout = 5.0
        input_group = None
        while login_timeout > 0:
            try:
                input_group = driver.find_element(By.XPATH, "//div[@class='p-inputgroup']")
            except Exception as e:
                logger.error("Trying to find input group %s", str(e))
                None

            login_timeout -= 0.5
            time.sleep(0.5)
        
        #try to redirect to search part url
        if input_group == None:
            driver.get(constants.URL_SEARCH_PART_BROWSER)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='p-inputgroup']")))
    else:
        None

def read_csv_file():
    import csv
    
    logger.info("##### Read CSV Step #####")

    with open(f"./resources/{constants.CSV_FILE_NAME}.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        is_title_row = True
        has_found_title = False
        for row in reader:
            if not has_found_title:
                if row[0] == "Item Number" and row[1] == "Quantity" and row[2] == "Part Reference" and row[3] == "AMZ_PN":
                    has_found_title = True
                else:
                    continue
            else:
                None
            
            if has_found_title:
                if is_title_row:
                    csv_title.extend(row)
                    is_title_row = False
                else:
                    part_number = row[3]
                    if not all_part_dict.__contains__(part_number):
                        all_part_key.append(row[3])
                        all_part_dict[row[3]] = row
                    else:
                        logger.warning("[DUPLICATED] [PART_NUMBER] %s [ORDER] %s", part_number, row[0])
            else:
                None

def search_part_number():
    import random

    logger.info("##### Search Step #####")

    error_reason = ""
    if all_part_dict.__len__() == 0:
        logger.error("No number part")
        return
        
    #find all parts button
    all_part_button = driver.find_element(By.XPATH, "//button[@aria-label='All parts']")
    all_part_button.click()
        
    for x in all_part_key:
        delay_time = delay_searching_time[random.randint(0, delay_searching_time.__len__() - 1)]
        time.sleep(delay_time)

        logger.info("[%s] Searching [Order] %s [Delay] %.2f [PART_NUMBER] %s", x, all_part_dict[x][0], delay_time, x)
        
        timeout_find_input_search = 5
        found_input_search = False
        while timeout_find_input_search > 0:
            try:
                input_group = driver.find_element(By.XPATH, "//div[@class='p-inputgroup']")
                search_input = input_group.find_element(By.TAG_NAME, "input")
                search_button = input_group.find_element(By.TAG_NAME, "button")

                search_input.clear()
                search_input.send_keys(x)
                search_button.click()
                found_input_search = True
                break
            except:
                None
            
            time_out_find_input_search -= 1
            time.sleep(1)

        if found_input_search:
            timeout_find_search_result = 10
            found = False
            while timeout_find_search_result > 0:
                timeout_find_search_result -= 0.5
                time.sleep(0.5)
                try:
                    result_component = driver.find_element(By.XPATH, "//div[@class='col-12']/div[@class='grid']/div[@class='col-12']/div[@class='p-dataview p-component p-dataview-grid']")
                    if result_component != None:
                        found = True
                        break
                except:
                    try:
                        no_part_found_component = driver.find_element(By.XPATH, "//div[@class='col-12']/div[@class='grid']/div[@class='col-12']/p[contains(text(), 'No part found')]")
                        if no_part_found_component != None:
                            found = False
                            error_reason = "PART NOT FOUND"
                            break
                    except:
                        None
                    
            if found:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    from selenium.webdriver.common.keys import Keys

                    parent = driver.find_element(By.XPATH, "//li[@class='col-12 px-0 flex align-items-center gap-3']")
                    all_button = parent.find_elements(By.TAG_NAME, "button")
                    if all_button.__len__() == 0 or all_button == None:
                        found = False
                        error_reason = "CANNOT FOUND DATASHEET BUTTON"
                    else:
                        datasheet_button = all_button[0]
                        if not datasheet_button.is_enabled():
                            found = False
                            error_reason = "DATASHEET NOT FOUND"
                        else:
                            action_chains = ActionChains(driver)
                            action_chains.key_down(Keys.COMMAND).click(datasheet_button).key_up(Keys.COMMAND).perform()

                            time.sleep(2)
                            driver.switch_to.window(driver.window_handles[1])
                            wait.until(EC.presence_of_element_located((By.XPATH, "//body/div[@id='outerContainer']/div[@id='mainContainer']")))
                            content_type = driver.execute_script("return window.navigator.contentType || document.contentType || ''")
                            logger.info("[%s] Download PDF content-type: %s", x, content_type)
                            if content_type != "application/pdf":
                                found = False
                                error_reason = "DATASHEET NOT FOUND"

                            time.sleep(2)
                            if driver.set_window_position != 0:
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                            else:
                                None
                except Exception as e:
                    logger.error("[%s] error while loading datasheet %s", x, str(e))
                    found = False
                    error_reason = "ERROR WHILE LOADING DATASHEET"
                    time.sleep(1)
                    if driver.set_window_position != 0:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    else:
                        None
            else:
                error_reason = error_reason if error_reason.__len__() else "TIMEOUT"

            if not found:
                write_output(all_part_dict[x] + [error_reason])
            else:
                None
        else:
            logger.error("[%s] Cannot found searching input component", x)
            write_output(all_part_dict[x] + "INPUT COMPONENT NOT FOUND")
        
def write_output(row):
    if row.__len__() > 0:
        import csv
        import os
        
        folder_path = f"./resources/{constants.CSV_FILE_NAME}_results"
        output_path = f"{folder_path}/{current_time}_output.csv"
        os.makedirs(folder_path, exist_ok=True)
        if os.path.exists(output_path):
            with open(output_path, "a", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(row)
        else:
            with open(output_path, "w", newline='') as csv_file:
                writer = csv.writer(csv_file)
                if csv_title.__len__() > 0:
                    writer.writerow(csv_title + ["ERROR"])
                    writer.writerow(row)
                else:
                    None
    else:
        None