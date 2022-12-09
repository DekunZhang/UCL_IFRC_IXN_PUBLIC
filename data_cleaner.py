import os
from glob import glob
from pathlib import Path

SOURCE_DIRECTORY = "CSVdatabases"
TARGET_DIRECTORY = "cleaned_databases"
DATABASES_FOLDER = f"{os.getcwd()}/{SOURCE_DIRECTORY}"
CLEANED_FOLDER = f"{os.getcwd()}/{TARGET_DIRECTORY}"


def clean_file_contents(contents: list[str]):
    return contents[4:-2]


def clean_all_databases():
    database_files = glob(f"{DATABASES_FOLDER}/**/*.csv")
    for raw_data_file in database_files:
        target_directory = os.path.dirname(raw_data_file).replace(SOURCE_DIRECTORY, TARGET_DIRECTORY)
        target_file = raw_data_file.replace(SOURCE_DIRECTORY, TARGET_DIRECTORY)
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        with open(raw_data_file, 'r') as source:
            with open(target_file, 'w') as destination:
                destination.writelines(clean_file_contents(source.readlines()))


def remove_empty_databases():
    cleaned_data_files = glob(f"{CLEANED_FOLDER}/**/*.csv")
    for cleaned_data_file in cleaned_data_files:
        delete = False
        with open(cleaned_data_file, 'r') as f:
            if len(f.readlines()) < 2:
                delete = True
        if delete:
            Path(cleaned_data_file).unlink()


if __name__ == '__main__':
    clean_all_databases()
    remove_empty_databases()
