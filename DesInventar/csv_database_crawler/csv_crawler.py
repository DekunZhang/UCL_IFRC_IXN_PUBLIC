import os
import time

from bs4 import BeautifulSoup
import requests
import logging
from requests import HTTPError

from .Country import Country
from .object_dumper import Dumper
from .Disasters import Disaster, Disasters


class CSVCrawler:
    COUNTRY_CACHE_FILE = 'country_list.pkl'
    DISASTERS_CACHE_FILE = 'disasters.pkl'
    DATABASES_DIRECTORY = f"{os.path.dirname(os.path.realpath(__file__))}/CSVdatabases"

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
        self.__dumper.cache(country_list, CSVCrawler.COUNTRY_CACHE_FILE)
        return country_list

    def __get_disaster_types_for_all_countries(self):
        country_list = self.__dumper.load(CSVCrawler.COUNTRY_CACHE_FILE) \
            if self.__dumper.has_cache(CSVCrawler.COUNTRY_CACHE_FILE) \
            else self.__get_country_list()
        country_disasters_dict = {}
        for country in country_list:
            cache_folder = self.__dumper.get_cache_folder()
            cache_name = f"disasters/{country.get_name()}_{country.get_country_code()}.pkl"
            disasters = self.__dumper.load(cache_name) \
                if self.__dumper.has_cache(cache_name) \
                else self.__get_disaster_types(country)
            logging.info(f"Adding disasters for {country.get_name()}")
            country_disasters_dict[country] = disasters
        self.__dumper.cache(country_disasters_dict, CSVCrawler.DISASTERS_CACHE_FILE)
        return country_disasters_dict

    def __get_disaster_types(self, country):
        logging.info(f"Retrieving disasters of {country.get_name()}")
        html_text = CSVCrawler.get_html_text(country.get_url())
        soup = BeautifulSoup(html_text, "lxml")
        disaster_selection = soup.find("select", attrs={"name": "eventos"})
        raw_disasters = CSVCrawler.remove_newlines(disaster_selection.contents)
        cleaned_disaster_tags = raw_disasters[1:]
        disasters = Disasters(country)
        for disaster_tag in cleaned_disaster_tags:
            name_en = disaster_tag.string.strip()
            query_key = disaster_tag['value']
            disasters.add_disaster(Disaster(name_en=name_en, query_key=query_key))
        disasters.rename_duplicate_disasters()
        cache_folder = self.__dumper.get_cache_folder()
        country_cache_folder = f"{cache_folder}/disasters"
        if not os.path.exists(country_cache_folder):
            os.makedirs(country_cache_folder)
        self.__dumper.cache(disasters, f"disasters/{country.get_name()}_{country.get_country_code()}.pkl")
        return disasters

    @staticmethod
    def generate_url(country: Country, disaster: Disaster):
        base_url = "https://www.desinventar.net/DesInventar/stats_spreadsheet.jsp?bookmark=1&countrycode="
        middle_url = "&maxhits=100&lang=EN&logic=AND&sortby=0&frompage=/definestats.jsp&bSum=Y&_stat="
        query_data_stat = "fichas.fechano"
        latter_url = ",,&nlevels=1&_variables="
        wanted_data_types = "1,fichas.muertos,fichas.heridos,fichas.desaparece,fichas.vivdest,fichas.vivafec," \
                     "fichas.damnificados,fichas.afectados,fichas.reubicados,fichas.evacuados,fichas.valorus," \
                     "fichas.valorloc,fichas.nescuelas,fichas.nhospitales,fichas.nhectareas,fichas.cabezas," \
                     "fichas.kmvias&_eventos="
        return base_url + country.get_country_code() + middle_url + query_data_stat + latter_url + wanted_data_types \
            + disaster.query_key

    def run(self):
        logging.basicConfig(level=logging.INFO)
        country_disasters_dict = self.__dumper.load(CSVCrawler.DISASTERS_CACHE_FILE) \
            if self.__dumper.has_cache(CSVCrawler.DISASTERS_CACHE_FILE) \
            else self.__get_disaster_types_for_all_countries()
        for country, disasters in country_disasters_dict.items():
            country_directory = f"{CSVCrawler.DATABASES_DIRECTORY}/{country.get_name()}_{country.get_country_code()}"
            if not os.path.exists(country_directory):
                os.makedirs(country_directory)
            for disaster in disasters:
                filepath = f"{country_directory}/{disaster.name}.csv"
                if os.path.exists(filepath):
                    logging.info(f"Exist: {filepath}, skip")
                else:
                    logging.info(f"Downloading: {filepath}")
                    r = requests.get(CSVCrawler.generate_url(country, disaster))
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    time.sleep(0.1)

