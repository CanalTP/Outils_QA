import os
import datetime as dt
import csv


class SpamComparator:
    def __init__(self,path, date, days, file_name_for_result):
        self.path = path
        self.date = date
        self.days = days
        self.file_name_for_result = file_name_for_result

    def run(self):
        print('Spam Comparator running...')
        dates = get_range_date(self.date, self.days)
        files_by_date = sort_files_by_date(self.path, dates)
        print('Files sorted by date...')
        files_by_date = total_result_by_day_and_device(files_by_date)
        print('Generate result file')
        generate_results_file(files_by_date, self.file_name_for_result)


def generate_results_file(result_dict, file_name):
    with open(file_name, 'w') as file:
        for date, devices in result_dict.items():
            for device, nb_sent in devices.items():
                file.write(';'.join((date, device, str(nb_sent) + '\n')))


def total_result_by_day_and_device(files_by_date):
    """
    Aggrege les informations récupérées en nombre d'envois par mobile & date, plutot que par fichier csv.
    :param list_result: les date + mobile + nb d'envoi de chaque csv.
    :return: un dictionnaire au format {date:{mobile:nb_envois}}
    """

    device_row = 1
    total_results = dict()
    for date, files in files_by_date.items():
        total_results[date] = dict()
        for file in files:
            with open(file) as csv_file:
                csv_file = csv.reader(csv_file, delimiter=";", quoting=csv.QUOTE_NONE)
                for row in csv_file:
                    try:
                        total_results[date][row[device_row]] += 1
                    except KeyError:
                        total_results[date][row[device_row]] = 1
    print(f'final total results is {total_results}')
    return total_results


def sort_files_by_date(path, dates):
    '''

    :param path: where Alert Trafic files are
    :param dates: files we want to get
    :return: dict with files by wanted date
    '''
    files_by_date = {}
    for file in os.listdir(path):
        if file.lower().endswith('.csv'):
            for date in dates:
                date = date.strftime("%Y%m%d")
                if date in file:
                    try:
                        files_by_date[date].append(file)
                    except KeyError:
                        files_by_date[date] = []
                        files_by_date[date].append(file)
    return files_by_date


def get_range_date(date, days):
    dates = []
    for day in range(days):
        dates.append(date + dt.timedelta(day))

    return dates
