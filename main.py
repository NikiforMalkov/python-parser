from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.postPdo import PostPdo
from src.database import session
from src.parser import Parser

postPdo = PostPdo(session)

urlCollection = [
    "https://www.instagram.com/failcrew/",
    "https://www.instagram.com/drift_craft/",
    "https://www.instagram.com/rds_gp/",
]

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
    "publicationLink": "div:nth-child(1) > a",
    "publicationTime": "body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > div.k_Q0X.NnvRN > a > time",
    "publicationDescription": ".PpGvg > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)",
    "publicationClosePopupButton": "body > div._2dDPU.vCf6V > button.ckWGn",
}

webDriver = webdriver.Chrome()
post = PostPdo(session)
parserEntity = Parser(webDriver, selectorCollection, post)
parserEntity.login("jar0fgreed", "nnm26957nnm")
for url in urlCollection:
    parserEntity.get_post_row(url)

webDriver.close()

# postPdo.one_by_id(2)
