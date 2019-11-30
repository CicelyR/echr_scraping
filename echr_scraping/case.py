from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
import unicodedata
from retry import retry

DELAY = 60 # seconds

class Case:
    def __init__(self, application_no, browser):
        self.application_no = application_no
        self.hudoc_url = (f"https://hudoc.echr.coe.int/eng#{{%22fulltext%22:[%22{self.application_no}%22],"
                "%22languageisocode%22:[%22ENG%22],%22respondent%22:[%22GBR%22],"
                "%22documentcollectionid2%22:[%22GRANDCHAMBER%22,%22CHAMBER%22],"
                "%22typedescription%22:[%2215%22]}")
        self.exec_url = ("https://hudoc.exec.coe.int/eng#{{%22EXECDocumentTypeCollection%22:[%22res%22],"
                f"%22EXECLanguage%22:[%22ENG%22],%22EXECAppno%22:[%22{application_no}%22]}}")
        self.case_details, self.judgement = self.get_case_details(browser, self.hudoc_url)
        self.exec_details, self.resolution = self.get_case_details(browser, self.exec_url)

    @retry(exceptions=ElementClickInterceptedException, tries=5, delay=5)
    def get_case_details(self, browser, url):
        browser.get(url)
        case_details = {}
        case_link = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.headlineContaniner > a')))
        case_link.click()
        _ = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#document > div.content p')))
        document_div = BeautifulSoup(browser.page_source).select_one("div#document")
        case_details_tab = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li#notice > a')))
        case_details_tab.click()
        WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#notice > div.content > div')))
        case_details_div = BeautifulSoup(browser.page_source).select_one("div#notice")
        for div in case_details_div.select("div.row"):
            heading = div.select_one("div.noticefieldheading").text
            value = [d.text.strip() for d in div.select("div.noticefieldvalue div")]
            case_details[heading] = value
        document = "\n".join([unicodedata.normalize("NFKC", d.get_text()) for d in document_div.select("div.content div p")])
        return case_details, document
    

    
    