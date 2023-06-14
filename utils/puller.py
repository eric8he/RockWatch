import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import undetected_chromedriver as uc

class Puller:
    def __init__(self, base_url: str, search_pre: str, search_post: str, cell_class: str, name_class: str, loc_class: str, wrap_req: bool=False):
        self.base_url = base_url
        self.search_pre = search_pre
        self.search_post = search_post
        self.cell_class = cell_class
        self.name_class = name_class
        self.loc_class = loc_class
        self.wrap_req = wrap_req

    def __init__(self, options):
        self.base_url = options["base_url"]
        self.search_pre = options["search_pre"]
        self.search_post = options["search_post"]
        self.cell_class = options["cell_class"]
        self.name_class = options["name_class"]
        self.loc_class = options["loc_class"]
        self.wrap_req = options["wrap_req"]


    def search_query(self, query: str):
        url_merged = self.base_url + self.search_pre + query + self.search_post
        if self.wrap_req:
            options = Options()
            options.headless = True
            browser = uc.Chrome(options=options)
            browser.get(url_merged)
            rq = browser.page_source
            browser.close()
        else:
            rq = requests.get(url_merged).content

        soup = BeautifulSoup(rq, 'html.parser')
        items = soup.find_all(class_=self.cell_class)

        items_proc = [(self.recurse_max(item.find(class_=self.name_class)), self.recurse_max(item.find(class_=self.loc_class)), item.find('img')['src'], item.find('a')['href']) for item in items]

        return items_proc
    
    def recurse_max(self, soup_tag):
        if type(soup_tag) == NavigableString:
            return soup_tag

        i = 0
        while soup_tag.contents[i] == "\n":
            i += 1
        
        return self.recurse_max(soup_tag.contents[i])