# Credit goes to...
# https://github.com/quakerpunk/content-audit/blob/origin/content_audit.py

from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import random
import urllib.parse
import re
import time

class ContentAuditor:

    def __init__(self, df_urls, url_field_index):
        """
        Initialization method for the ContentAuditor class.
        """
        self.urls = df_urls.iloc[:,url_field_index]
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
            # print ("Parsing %s" % line_url)
            self.url_parts = urllib.parse.urlparse(url)
            req = urllib.request.Request(url)
            req.add_header('User-Agent', ua_string)
            try:
                data = urllib.request.urlopen(req, timeout = 5)
            except:
                continue
            self.soupy_data = BeautifulSoup(data, features="html.parser")
            try:
                self.extract_tags(url)
            except:
                continue
            time.sleep(random.uniform(1, 3))
        print("End of extraction")


    def extract_tags(self, url):
        """
        Searches through self.soupy_data and extracts meta tags such as page
        description and title for inclusion into content audit spreadsheet
        """
        page_info = {}
        page_info['mention_identifier'] = url

        for tag in self.soupy_data.find_all('meta', attrs={"name": True}):
            try:
                page_info[tag['name']] = tag['content']
            except:
                page_info[tag['name']] = ''
        page_info['title'] = self.soupy_data.head.title.contents[0]
        page_info['filename'] = self.url_parts[2]
        try:
            page_info['name'] = self.soupy_data.h3.get_text()
        except:
            page_info['name'] = ''
        self.add_necessary_tags(page_info, ['keywords', 'description', 'title'])
        self.site_info.append(page_info)
        self.soupy_data = ""


    def add_necessary_tags(self, info_dict, needed_tags):
        """
        This method insures that missing tags have a null value
        before they are written to the output spreadhseet.
        """
        for key in needed_tags:
            if key not in info_dict:
                info_dict[key] = " "
        return info_dict