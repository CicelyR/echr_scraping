from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import unicodedata

DELAY = 30 # seconds

class Case:
    def __init__(self, application_no, browser):
        self.application_no = application_no
        self.case_details = {}
        self.get_case_details(browser)

    def get_case_details(self, browser):
        url = (f"https://hudoc.echr.coe.int/eng#{{%22fulltext%22:[%22{self.application_no}%22],"
                "%22languageisocode%22:[%22ENG%22],%22respondent%22:[%22GBR%22],"
                "%22documentcollectionid2%22:[%22GRANDCHAMBER%22,%22CHAMBER%22],"
                "%22typedescription%22:[%2215%22]}")
        browser.get(url)
        elem = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.headlineContaniner > a')))
        elem.click()
        judgement_div = BeautifulSoup(browser.page_source).select_one("div#document")
        elem = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li#notice > a')))
        elem.click()
        elem = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#notice > div.content > div')))
        case_details_div = BeautifulSoup(browser.page_source).select_one("div#notice")
        for div in case_details_div.select("div.row"):
            heading = div.select_one("div.noticefieldheading").text
            value = [d.text.strip() for d in div.select("div.noticefieldvalue div")]
            self.case_details[heading] = value
        self.judgement = "\n".join([unicodedata.normalize("NFKC", d.get_text()) for d in judgement_div.select("div.content div p")])

    
    