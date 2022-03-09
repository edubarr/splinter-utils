"""
BOT em Python para configuração de aluguel via PeakMonsters
"""
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


print("\nSCIDU - BOT para envio de cartas em lote via PeakMonsters\n")

# Carrega as contas do arquivo .env


def loadAccounts():
    load_dotenv()
    userlst = os.getenv("ACCUSERNAME").split(",")
    postinglst = os.getenv("POSTING_KEY").split(",")
    activelst = os.getenv("ACTIVE_KEY").split(",")
    pwlst = list(zip(postinglst, activelst))
    print(str(len(userlst)) + " accounts loaded!\n")
    print(userlst)
    print("\n")
    return dict(zip(userlst, pwlst))


# Inicia o Browser


def startBrowser():
    chrome_service = Service("chromedriver.exe")
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(options=options, executable_path="chromedriver.exe")


def main():
    acc_dict = loadAccounts()

    # Percorre o dicionário
    for user, pw_lst in acc_dict.items():

        # Iniciar Browser como driver
        driver = startBrowser()

        # Definir espera padrão
        wait = WebDriverWait(driver, 60)

        print(user)
        driver.get("https://peakmonsters.com/")

        time.sleep(5)

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[5]/div/div[1]/div')
            )
        )
        driver.find_element(
            By.XPATH, '//*[@id="app"]/div[5]/div/div[1]/div'
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Login']"))
        )
        driver.find_element(By.XPATH, "//a[normalize-space()='Login']").click()

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='Email / Username']")
            )
        )
        elm_user = driver.find_element(
            By.XPATH, "//input[@placeholder='Email / Username']"
        )
        elm_user.clear()
        elm_user.send_keys(user)

        elm_pw = driver.find_element(
            By.XPATH, "//input[@placeholder='Password / Posting Key']"
        )
        elm_pw.clear()
        elm_pw.send_keys(pw_lst[0])

        time.sleep(1)

        driver.find_element(By.XPATH, "//tr[4]//td[2]//button[1]").click()

        time.sleep(2)

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Rent']"))
        )
        driver.find_element(By.XPATH, "//a[normalize-space()='Rent']").click()

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Configure CP Bid']")
            )
        )
        driver.find_element(
            By.XPATH, "//button[normalize-space()='Configure CP Bid']"
        ).click()

        time.sleep(4)

        elm_cp = driver.find_element(
            By.XPATH,
            "//input[@class='form-control text-semibold flex-grow text-right']",
        )
        elm_cp.click()
        elm_cp.send_keys(Keys.CONTROL, "a")
        elm_cp.send_keys(Keys.BACKSPACE)
        elm_cp.send_keys(os.getenv("RENT_BID"))

        elm_min = driver.find_element(
            By.XPATH,
            "//div[@class='sweet-title-slot sweet-modal-overlay theme-dark sweet-modal-clickable is-visible']//div[2]//div[1]//input[1]",
        )
        elm_min.clear()
        elm_min.send_keys(os.getenv("MIN_PW"))

        elm_max = driver.find_element(
            By.XPATH,
            "//div[@class='row content-group-sm']//div[2]//input[1]",
        )
        elm_max.clear()
        elm_max.send_keys(os.getenv("MAX_PW"))
        elm_max.send_keys(Keys.ENTER)

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-xs btn-primary'][normalize-space()='Confirm']"))
        )
        driver.find_element(By.XPATH, "//button[@class='btn btn-xs btn-primary'][normalize-space()='Confirm']").click()



        # driver.find_element(By.XPATH,
        #                     "//li[41]/a/div[1]/input").click()

        # time.sleep(2)

        # cards_rows = len(driver.find_elements(By.XPATH, "//tbody/tr"))

        # if cards_rows == 0:
        #     print("Account doens't seem to have any cards owned!")
        #     driver.close()

        #     print("Waiting 1/2 minute to avoid Peakmonsters Ban!\n")
        #     time.sleep(30)
        #     continue

        # for i in range(cards_rows):
        #     card = driver.find_element(By.XPATH,
        #                                "//tbody/tr[" + str(i + 1) + "]/td[3]/div/div")

        #     card_name = card.text.split()[:2]

        #     card_frame = driver.find_element(By.XPATH,
        #                                      "//tbody/tr[" + str(i + 1) + "]/td[3]/div/a/div")

        #     classes = card_frame.get_attribute('class')

        #     if "monster-img-gold" in classes:
        #         print(card_name)
        #         print("Gold")
        #     else:
        #         print(card_name)

        # wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//table/thead/tr/th[1]/a/i")))
        # # Talvez remover pro headless
        # driver.execute_script("window.scrollTo(0, 0)")
        # driver.find_element(By.XPATH,
        #                     "//table/thead/tr/th[1]/a/i").click()

        # driver.find_element(By.XPATH, "//i[@class='icon-stack3']").click()

        # wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//button[normalize-space()='Transfer']")))
        # driver.find_element(By.XPATH,
        #                     "//button[normalize-space()='Transfer']").click()

        # wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//input[@placeholder='Account Name']")))
        # elm_main_acc = driver.find_element(By.XPATH,
        #                                    "//input[@placeholder='Account Name']")
        # elm_main_acc.clear()
        # elm_main_acc.send_keys(os.getenv("MAIN_ACC"))

        # wait.until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, "//button[@class='btn btn-success btn-xs']")
        #     )
        # )
        # driver.find_element(
        #     By.XPATH, "//button[@class='btn btn-success btn-xs']"
        # ).click()
        # wait.until(
        #     EC.element_to_be_clickable(
        #         (
        #             By.XPATH,
        #             "//div[@class='sweet-modal theme-light has-title has-content is-visible']//button[@class='btn btn-primary btn-xs'][normalize-space()='Confirm']",
        #         )
        #     )
        # )
        # driver.find_element(
        #     By.XPATH,
        #     "//div[@class='sweet-modal theme-light has-title has-content is-visible']//button[@class='btn btn-primary btn-xs'][normalize-space()='Confirm']",
        # ).click()

        time.sleep(3)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Continue']"))
        )
        # Talvez remover pro headless
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element(By.XPATH, "//a[normalize-space()='Continue']").click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']")))
        elm_hive_login = driver.find_element(By.XPATH, "//input[@id='username']")
        elm_hive_login.clear()
        elm_hive_login.send_keys(user)

        elm_hive_pw = driver.find_element(By.XPATH, "//input[@id='password']")
        elm_hive_pw.clear()
        elm_hive_pw.send_keys(pw_lst[1])

        driver.find_element(By.XPATH, "//span[@class='checkbox mr-2 -checked']").click()

        time.sleep(3)

        driver.find_element(By.XPATH, "//button[normalize-space()='Login']").click()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "//button[normalize-space()='Login']").click()
        except:
            print("Login already clicked!")

        time.sleep(3)
        
        # Talvez remover pro headless
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Approve']")
            )
        )
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element(By.XPATH, "//button[normalize-space()='Approve']").click()

        print("Waiting 1/2 minute to avoid Peakmonsters Ban!\n")

        time.sleep(20)

        driver.close()

        time.sleep(20)


if __name__ == "__main__":
    main()
