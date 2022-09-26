import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

# login info
USER_NAME = ""
PW = ""

# coupon clipper bot
def couponClipper():
    # time stamp
    print("Start task at: " + str(datetime.now()))

    # initialize webdriver
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.safeway.com/account/sign-in.html")
    driver.maximize_window()

    # input username
    userName = driver.find_element(By.ID, 'label-email')
    userName.clear()
    userName.send_keys(USER_NAME)

    # input password
    passWord = driver.find_element(By.ID, 'label-password')
    passWord.clear()
    passWord.send_keys(PW)

    # click sign in
    signInButton = driver.find_element(By.ID, 'btnSignIn')
    signInButton.click()
    time.sleep(3)

    # navigate to coupon page
    safewayForU = driver.find_element(By.XPATH,
                                      '/html/body/div[2]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[3]/nav/li[2]/a')
    safewayForU.click()
    time.sleep(2)

    # load all coupons
    try:
        while driver.find_element(By.XPATH, '//*[@id="coupon-grid_0"]/div/div[4]/button'):
            loadMore = driver.find_element(By.XPATH, '//*[@id="coupon-grid_0"]/div/div[4]/button')
            loadMore.click()
            time.sleep(0.5)
    except:
        print('All coupons loaded. \n')

    # get id of all available coupons
    html = driver.page_source
    res = html.split()
    el = []
    for i in res:
        if (i.startswith("id=\"couponAddBtn")):
            el.append(i[4: len(i) - 1])

    # clip all coupons
    clippedCounter = 0
    try:
        for i in el:
            element = driver.find_element(By.ID, i)
            driver.execute_script("arguments[0].click();", element)
            clippedCounter += 1
    except Exception:
        print(Exception)

    print('New coupons found: ' + str(len(el)))
    print("Clipped: " + str(clippedCounter))

    driver.quit()

    # time stamp
    print("Finish task at: " + str(datetime.now()))

    # recurring schedule
    schedule.every().day.at("00:01").do(couponClipper)

    while True:
        schedule.run_pending()
        time.sleep(1)
        couponClipper();