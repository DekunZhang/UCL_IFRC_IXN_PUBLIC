from itertools import groupby

import requests
import time
import os
from ..XMLdatabase_downloader.GLOBAL_VARS import countries


def get_actual_url(code: str, is_querying_disaster_type: bool,
                   disaster_name: str = None):
    # actual_url = base_url + COUNTRY_CODE + middle_url + (query_disaster_stat | query_data_stat)
    # + latter_url + (query_disaster_name | (query_data + disaster_name))
    base_url = "https://www.desinventar.net/DesInventar/stats_spreadsheet.jsp?bookmark=1&countrycode="
    middle_url = "&maxhits=100&lang=EN&logic=AND&sortby=0&frompage=/definestats.jsp&bSum=Y&_stat="
    query_disaster_stat = "eventos.nombre_en"
    query_data_stat = "fichas.fechano"
    latter_url = ",,&nlevels=1&_variables="
    query_disaster_name = "1"
    query_data = "1,fichas.muertos,fichas.heridos,fichas.desaparece,fichas.vivdest,fichas.vivafec," \
                 "fichas.damnificados,fichas.afectados,fichas.reubicados,fichas.evacuados,fichas.valorus," \
                 "fichas.valorloc,fichas.nescuelas,fichas.nhospitales,fichas.nhectareas,fichas.cabezas," \
                 "fichas.kmvias&_eventos="
    return base_url + code + middle_url + (
        query_disaster_stat if is_querying_disaster_type else query_data_stat) \
        + latter_url + (
            query_disaster_name if is_querying_disaster_type else query_data + disaster_name)


def get_disaster_csv(code, disaster_filename):
    disaster_url = get_actual_url(code, True)
    r = requests.get(disaster_url)
    print(f"Downloading: {disaster_filename}")
    with open(disaster_filename, 'wb') as f:
        f.write(r.content)


def get_disaster_types(file_csv: str):
    with open(file_csv, "r") as disaster_file:
        contents = disaster_file.readlines()
    contents = contents[5:-2]
    return list(map(lambda line: line.split("\t")[0].split('/')[0], contents))


def get_each_disaster_data(code, disaster, data_dir):
    uniq_disaster, disaster_group = disaster
    for i, d in enumerate(disaster_group):
        data_filename = f"{data_dir}/{d}.csv" if i == 0 else f"{data_dir}/{d}_{i}.csv"
        data_url = get_actual_url(code, False, d)
        if os.path.exists(data_filename):
            print(f"Exist: {data_filename}, skip")
        else:
            print(f"Downloading: {data_filename}")
            r = requests.get(data_url)
            with open(data_filename, 'wb') as f:
                f.write(r.content)
            time.sleep(1)


def get_all_data_by_country(disaster_dir, code, country, directory):
    disaster_filename = f"{disaster_dir}/{code}_{country}.csv"
    if not os.path.exists(disaster_filename):
        get_disaster_csv(code, disaster_filename)
    else:
        print(f"Exist: {disaster_filename}, skip")
    data_dir = f"{directory}/{code}_{country}"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    disaster_types = get_disaster_types(disaster_filename)

    def sort_func(elem: str):
        return elem.upper()

    disaster_types.sort(key=sort_func)
    uniq_disasters = []
    disaster_groups = []
    for k, g in groupby(disaster_types, key=sort_func):
        disaster_groups.append(list(g))
        uniq_disasters.append(k)
    disasters = zip(uniq_disasters, disaster_groups)
    for disaster in disasters:
        get_each_disaster_data(code, disaster, data_dir)


def main():
    directory = "./CSVdatabases"
    disaster_dir = f"{directory}/disasters"
    if not os.path.exists(disaster_dir):
        os.makedirs(disaster_dir)
    for (code, country) in countries:
        get_all_data_by_country(disaster_dir, code, country, directory)


if __name__ == '__main__':
    main()
