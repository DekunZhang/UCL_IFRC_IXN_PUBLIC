from itertools import groupby

from .Country import Country


class Disaster:
    def __init__(self, name_en: str, query_key: str):
        self.__name_en = name_en.replace('/', '+')
        self.__query_key = query_key

    @property
    def name(self):
        return self.__name_en

    def set_new_name(self, new_name):
        self.__name_en = new_name

    @property
    def query_key(self):
        return self.__query_key


class Disasters:
    def __init__(self, country: Country):
        self.__country = country
        self.__disaster_list: list[Disaster] = []

    def add_disaster(self, disaster: Disaster):
        self.__disaster_list.append(disaster)

    def rename_duplicate_disasters(self):
        disaster_names_list = [d.name.upper() for d in self.__disaster_list]
        for i, d in enumerate(self.__disaster_list):
            total_count = disaster_names_list.count(d.name.upper())
            count = disaster_names_list[:i].count(d.name.upper())
            d.set_new_name(f"{d.name}_{str(count + 1)}" if total_count > 1 else d.name)

    def __iter__(self):
        return iter(self.__disaster_list)
