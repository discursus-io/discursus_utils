from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import random
import urllib.parse
import re
import time

class WebScraper:

    def __init__(self, df_urls, url_field_index):
        """
        Initialization method for the WebScraper class.
        """
        self.urls = list(dict.fromkeys(df_urls.iloc[:,url_field_index]))
        self.soupy_data = ""
        self.content = ""
        self.text_file = ""
        self.site_info = []
        self.url_parts = ""
        self.reg_expres = re.compile(r"www.(.+?)(.com|.net|.org)")
    

    def read_url(self):
        """
        Method which reads in a given url (to the constructor) and puts data
        into a BeautifulSoup context.
        """
        ua_string = 'Content-Audit/2.0'
        for url in self.urls:
            self.url_parts = urllib.parse.urlparse(url)
            req = urllib.request.Request(url)
            req.add_header('User-Agent', ua_string)
            try:
                data = urllib.request.urlopen(req, timeout = 5)
            except Exception as e:
                print(e)
                continue
            self.soupy_data = BeautifulSoup(data, features="html.parser")
            try:
                self.extract_tags(url)
            except Exception as e:
                print(e)
                continue
            time.sleep(random.uniform(1, 3))


    def extract_tags(self, url):
        """
        Searches through self.soupy_data and extracts meta tags such as page
        description and title for inclusion into content audit spreadsheet
        """
        page_info = {}
        page_info['mention_identifier'] = url
        page_info['filename'] = self.url_parts[2]
        try:
            page_info['title'] = self.soupy_data.head.title.contents[0]
        except:
            page_info['title'] = " "
        try:
            page_info['keywords'] = self.soupy_data.find("meta", { "name": "keywords"})["content"]
        except:
            page_info['keywords'] = " "
        try:
            page_info['description'] = self.soupy_data.find("meta", { "name": "description"})["content"]
        except:
            page_info['description'] = " "

        self.site_info.append(page_info)
        self.soupy_data = ""