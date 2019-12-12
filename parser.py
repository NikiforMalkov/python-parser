from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from postPdo import PostPdo
from database import session
import time

postPdo = PostPdo(session)

selectorCollection = {
    "loginButton": "#react-root > section > main > article > div.rgFsT > div:nth-child(2) > p > a",
    "loginField": "#react-root > section > main > div > article > div > div:nth-child(1) > div > form > "
                  "div:nth-child(2) > div > label > input ",
    "passwordField": "#react-root > section > main > div > article > div > div:nth-child(1) > div > form > "
                     "div:nth-child(3) > div > label > input ",
    "singInButton": "#react-root > section > main > div > article > div > div:nth-child(1) > div > form > "
                    "div:nth-child(4) ",
    "publication": "#react-root > section > main > div > div._2z6nI > article:nth-child(2) > div:nth-child(1) > "
                   "div > div:nth-child(2) > div",
    "publicationRow": "#react-root > section > main > div > div._2z6nI > article:nth-child(2) > div"
                      "> div > div ",
    "publicationCollection": "#react-root > section > main > div > div._2z6nI > article:nth-child(2) > div > div > "
                             "div > div > a",
    "publicationImage": "div:nth-child(1) > a > div > div.KL4Bh > img",
    "targetPublication": " a > div > div._9AhH0 ",
    "publicationDiv": " div > div._9AhH0 ",
    "test": "#react-root > section > main > div > div._2z6nI > article:nth-child(2) > div:nth-child(1) > div > "
            "div> div> a > div > div._9AhH0",
    "publicationLink": "div:nth-child(1) > a",
    "publicationTime": "body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > div.k_Q0X.NnvRN > a > time",
    "publicationDescription": ".PpGvg > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)",
    "publicationClosePopupButton": "body > div._2dDPU.vCf6V > button.ckWGn",
}

webDriver = webdriver.Chrome()


# TODO: обдумать куда это перенести или сделать менее трудозатратный вариант
def get_url_collection(href):
    collection = str(href).split(",")
    trash_collection = [
        "amp;", " 640w", " 480w", " 320w", " 240w", " 150w"
    ]
    for i in range(0, len(collection)):
        for j in range(0, len(trash_collection)):
            collection[i] = str(collection[i]).replace(trash_collection[j], "")
    # print(collection)
    return collection


class Parser(object):

    def __init__(self, driver):
        self.driver = driver
        self.cookie_collection = None

    def login(self, user_login, user_password):
        self.driver.get("https://www.instagram.com/")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selectorCollection["loginButton"]))
            )
            login_button = self.driver.find_element_by_css_selector(selectorCollection["loginButton"])
            login_button.click()
        finally:
            assert "No results found." not in self.driver.page_source

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selectorCollection["loginField"]))
            )
            login_filed = self.driver.find_element_by_css_selector(selectorCollection["loginField"])
            password_field = self.driver.find_element_by_css_selector(selectorCollection["passwordField"])
            sing_in_button = self.driver.find_element_by_css_selector(selectorCollection["singInButton"])
            login_filed.send_keys(user_login)
            password_field.send_keys(user_password)
            sing_in_button.click()
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#react-root > section > main > section > div.COOzN > div.m0NAq > div > div.RR-M-._2NjG_"
                ))
            )
        finally:
            assert "No login text selector found"

    def get_post_row(self, link):
        self.driver.get(link)
        try:
            check_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selectorCollection["publication"]))
            )

            publication_collection = self.driver.find_elements_by_css_selector(
                selectorCollection["publicationCollection"]
            )
            for publication in publication_collection:
                self.get_post(publication, selectorCollection)
        finally:
            assert "No publications on the page"

    def get_post(self, publication, selector_collection):
        publication_div = publication.find_element_by_css_selector(selector_collection["publicationDiv"])
        publication_div.click()
        # time.sleep(1)
        check_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector_collection["publicationDescription"]))
        )
        description = self.driver.find_element_by_css_selector(selector_collection["publicationDescription"])
        link = publication.get_attribute("href")
        date = self.driver.find_element_by_css_selector(selector_collection["publicationTime"])
        image_tag = self.driver.find_element_by_css_selector(selector_collection["publicationImage"])
        url_collection = get_url_collection(image_tag.get_attribute("srcset"))

        if postPdo.one_by_link(link) is None:
            postPdo.add_post(
                description.get_attribute("innerHTML"),
                url_collection[0],
                link,
                date.get_attribute("datetime")
            )
        close_popup_button = self.driver.find_element_by_css_selector(
            selector_collection["publicationClosePopupButton"]
        )
        close_popup_button.click()


urlCollection = [
    "https://www.instagram.com/failcrew/",
    "https://www.instagram.com/drift_craft/",
    "https://www.instagram.com/rds_gp/",
]

parser = Parser(webDriver)
parser.login("jar0fgreed", "nnm26957nnm")
for url in urlCollection:
    parser.get_post_row(url)


# postPdo.one_by_id(2)
# driver.close()
