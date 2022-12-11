from ..XMLdatabase_downloader.GLOBAL_VARS import countries
import os


def clean_file(filepath: str):
    with open(filepath, 'r') as f:
        try:
            contents = f.readlines()
        except UnicodeDecodeError as e:
            return []
    return contents[5:-2]


def main():
    source_directory = "./CSVdatabases"
    assert os.path.exists(source_directory)
    target_directory = "./cleaned_output"
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    for code, country in countries:
        source_folder = f"{source_directory}/{code}_{country}"
        assert os.path.exists(source_folder)
        target_folder = f"{target_directory}/{code}_{country}"
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        with os.scandir(source_folder) as it:
            for source_file in it:
                cleaned_contents = clean_file(source_file.path)
                target_file = source_file.path.replace("CSVdatabases",
                                                       "cleaned_output")
                with open(target_file, "w") as tf:
                    tf.writelines(cleaned_contents)


if __name__ == '__main__':
    main()
