from selenium import webdriver
from selenium.webdriver.support.ui import Select

from datetime import datetime
import smtplib

# Simple script written to automate the renewal of
# UBC U-PASS's using Selenium,

# email account to send attempt email from
SENDER_EMAIL = 'test@gmail.com'
SENDER_PASSWORD = 'email_password'

# location of selenium chromedriver,
# expected to be in the same directory
CHROME_WEB_DRIVER = 'chromedriver.exe'

# CWL logins, ('username', 'password')
AUTH_PAIRS = [('ssc_username', 'ssc_password')]

# emails to be sent a confirmation email to
RECIPIENTS = ['recp_email@gmail.com']


def send_email(user, pwd, recipient, subject, body):
    """
    function to send email to recipient
    :param user: email address of sender
    :param pwd: password of sender
    :param recipient: email to send to
    :param subject: subject of email
    :param body: body to include in email
    :return: nothing
    """
    gmail_user = user
    gmail_pwd = pwd
    from_name = user
    to_line = recipient if type(recipient) is list else [recipient]
    subject_line = subject
    body_text = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (from_name, ", ".join(to_line), subject_line, body_text)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(from_name, to_line, message)
    server.close()


def get_upass(web_driver, username, password):
    """
    using selenium, click through web browser and renew the u-pass
    :param web_driver: instantiated web driver
    :param username: CWL username
    :param password: CWL password
    :return: nothing
    """
    web_driver.get('https://upassbc.translink.ca/')
    assert 'U-Pass' in web_driver.title

    drop_down = Select(web_driver.find_element_by_id('PsiId'))
    drop_down.select_by_value('ubc')

    go_button = web_driver.find_element_by_id('goButton')
    go_button.click()

    web_driver.find_element_by_id('j_username').send_keys(username)
    web_driver.find_element_by_id('password').send_keys(password)

    web_driver.find_element_by_name('action').click()

    web_driver.find_element_by_id('chk_1').click()
    web_driver.find_element_by_id('requestButton').click()


if __name__ == '__main__':
    usernames = ','.join(creds[0] for creds in AUTH_PAIRS)

    msg = 'Attempt to request U-PASS for username: %s \n\n on %s' % (usernames, datetime.now())

    for recp in RECIPIENTS:
        send_email(SENDER_EMAIL, SENDER_PASSWORD, recp, 'U-PASS Attempt', msg)

    for pair in AUTH_PAIRS:
        driver = webdriver.Chrome()
        get_upass(driver, pair[0], pair[1])
        driver.close()
