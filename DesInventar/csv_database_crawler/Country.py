class Country:
    def __init__(self, url: str, name: str):
        self.__url = url
        self.__name = name
        self.__country_code = url.split('countrycode=')[1].split('&')[0]

    def get_url(self):
        return self.__url

    def get_name(self):
        return self.__name

    def get_country_code(self):
        return self.__country_code
