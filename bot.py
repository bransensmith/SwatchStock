import smtplib
from email.message import EmailMessage

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

product_list = []

txt_link_path = 'ProductsList.txt'


def txt_file_procedures(option):
    if option == 'Load':

        # when loading list from txt always remove empty space
        with open(txt_link_path) as reader, open(txt_link_path, 'r+') as writer:
            for line in reader:
                if line.strip():
                    writer.write(line)
            writer.truncate()

        with open(txt_link_path, "r") as load:
            data = load.read()
            data_list = data.split("\n")

            # dont append empty values to internal list
            for element in data_list:
                if element:
                    product_list.append(element)

    elif option == 'Update':

        print('Updating list file:', txt_link_path)

        with open(txt_link_path, "w") as update:
            for item in product_list:
                if item:
                    update.write(item + "\n")


def email_notify(subject, body):
    msg = EmailMessage()
    msg.set_content(body)

    msg['subject'] = subject
    msg['to'] = ''

    user = ''
    msg['from'] = user
    password = ''

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


def main():
    error_count = 0

    # load list with txt links
    txt_file_procedures('Load')

    # count original list len for exit check
    error_count_check = len(product_list)

    # clean list of empty elements

    while len(product_list) != 0:

        for i in product_list:

            driver.get(i)

            try:
                WebDriverWait(driver, 30).until(
                    ec.element_to_be_clickable((By.CLASS_NAME, "b-pdp-button_add"))).click()
                email_notify('[INVENTORY ALERT]', i)

                product_list.remove(i)

            except TimeoutException:
                continue

            # either bad link or pop-up arose
            except ElementClickInterceptedException:
                error_count += 1
                product_list.remove(i)

    # if we failed because of error(s)
    if error_count == error_count_check:
        email_notify('[Script Alert]', 'Script FAILED by exceeding exception count limit.')

    elif error_count == 0:
        email_notify('[Script Alert]', 'ALL notifications were sent successfully.')

    elif error_count < error_count_check:
        email_notify('[Script Alert]', 'SOME notifications were sent successfully other may have failed.')

    # list end procedure for driver.
    txt_file_procedures('Update')

    driver.close()
    driver.quit()


if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=chrome_options)

    main()
