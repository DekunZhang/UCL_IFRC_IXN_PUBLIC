import dill
import os


class Dumper:
    def __init__(self):
        current_folder = os.path.dirname(os.path.realpath(__file__))
        self.__cache_folder = f"{current_folder}/caches"
        if not os.path.exists(self.__cache_folder):
            os.makedirs(self.__cache_folder)

    def cache(self, obj, name):
        with open(self.__get_cache_path(name), 'wb') as f:
            dill.dump(obj, f)

    def __get_cache_path(self, name):
        return f"{self.__cache_folder}/{name}"

    def has_cache(self, name):
        return os.path.exists(self.__get_cache_path(name))

    def load(self, name):
        if not self.has_cache(name):
            raise FileNotFoundError(
                f"Object cache with name '{name}' does not exist.")
        with open(self.__get_cache_path(name), 'rb') as f:
            return dill.load(f)

    def get_cache_folder(self):
        return self.__cache_folder
