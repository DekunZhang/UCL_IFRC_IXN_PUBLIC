from bs4 import BeautifulSoup
import bs4
import requests
from requests import HTTPError

from .Country import Country
from .object_dumper import Dumper


class CSVCrawler:
    COUNTRY_CACHE_NAME = 'country_list.pkl'

    def __init__(self):
        self.__index_url = "https://www.desinventar.net/DesInventar/index.jsp"
        self.__base_url = "https://www.desinventar.net"
        self.__dumper = Dumper()

    @staticmethod
    def remove_newlines(contents):
        return list(filter(lambda tr: tr != '\n', contents))

    @staticmethod
    def get_html_text(url) -> str:
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except HTTPError:
            return ""

    def __get_country_list(self):
        html_text = CSVCrawler.get_html_text(self.__index_url)
        soup = BeautifulSoup(html_text, "lxml")
        # soup.body.table.table.tr['class'] != 'bodydarklight'
        raw_data = CSVCrawler.remove_newlines(soup.body.table.table.children)
        # remove table title: 'Country/Region'
        raw_list_country_tags = raw_data[1:]
        country_tags_cleaned = [CSVCrawler.remove_newlines(c) for c in raw_list_country_tags]
        """
        list of td:
            <td width=30>&nbsp;</td>    --> index 0
            <td nowrap>                 --> index 1 -> lst[1]
                    <a                  --> lst[1].a -> a['name'] = " Albania"
                        class="blackLinks" 
                        href="/DesInventar/profiletab.jsp?countrycode=alb&continue=y"> Albania
                    </a>&nbsp;&nbsp;&nbsp;
                    <a  class="greyText" ...
                    <a  class="greyText" ...
            </td>
            <td nowrap>1851 - 2022</td>
            <td></td>
            <td nowrap> ... Profile</a></td>
        """
        country_list = [Country(url=self.__base_url + lst[1].a['href'], name=lst[1].a.string.strip())
                        for lst in country_tags_cleaned]
        self.__dumper.cache(country_list, CSVCrawler.COUNTRY_CACHE_NAME)
        return country_list

    def __set_disaster_types_for_all_countries(self):
        if self.__dumper.has_cache(CSVCrawler.COUNTRY_CACHE_NAME):
            country_list = self.__dumper.load(CSVCrawler.COUNTRY_CACHE_NAME)
        else:
            country_list = self.__get_country_list()
        for country in country_list:
            html_text = CSVCrawler.get_html_text(country.get_url())
            soup = BeautifulSoup(html_text, "lxml")
            disaster_selection = soup.find("select", attrs={"name": "eventos"})
            disasters_cleaned = CSVCrawler.remove_newlines(disaster_selection.contents)
            

    def run(self):
        self.__set_disaster_types_for_all_countries()
