# ECHR scraping

Uses selenium to scrape [HUDOC](https://hudoc.echr.coe.int/eng#{%22documentcollectionid2%22:[%22GRANDCHAMBER%22,%22CHAMBER%22]}) and [HUDOC EXEC](https://hudoc.exec.coe.int/eng#{%22EXECDocumentTypeCollection%22:[%22CEC%22]}) websites.

Example:

    from echr_scraping import Case
    from selenium import webdriver

    browser = webdriver.Chrome()

    case = Case("76760/12", browser)

    ## Save to docx file

    case.save_docx("Case_76760_12.docx")

Case items have the following lists of documents:

    case.judgements # Judgements from HUDOC
    case.exec_cases # Cases from HUDOC EXEC
    case.cofm_documents # Committee of ministers documents from HUDOC EXEC
    case.plan_documents # Action plans and reports from HUDOC EXEC
    case.other_documents # Other documents from HUDOC EXEC

Each document is a tuple with a dictionary of the case details and a string for the document contents.

Methods:

    case.get_document_details(browser: webdriver, link: str)
    gets a individual document details. link is the url for the main document page

    case.get_documents(browser: webdriver, url: str)
    gets all documents of a search result. url is the url for the search query

    case.get_highest_court_judgement()
    returns the highest court judgement if one exists

    case.validate_data()
    validates the case data

    case.save_docx(filepath: str)
    saves case to docx file
