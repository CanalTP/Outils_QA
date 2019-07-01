import os
import datetime as dt
import re

from spam_comparator import SpamComparator


def request_path_input():
    while True:
        path = input('Dans quel dossier avez vous déposé les CSV à extraire?'
                     ' Par defaut, nous les chercherons à la racine de ce script.')

        if not path:
            path = DIRECTORY_PATH

        if os.path.isdir(path):
            return path
        print("Ce chemin n'existe pas.\n")


def request_date_input():
    while True:
        date = input("A partir de quand souhaitez vous extraire les envois CSV d'Alert Trafic? (Format AAAAMMJJ)")
        try:
            return dt.datetime.strptime(date, '%Y%m%d')
        except ValueError:
            print('Le format de date doit être AAAAMMJJ')

def request_days_input():
    while True:
        days = input('Combien de jours voulez vous consulter? (Defaut : 1)')
        if not days:
            days = 1

        try:
            return abs(int(days))
        except ValueError:
            print('Ce n est pas un nombre valide. \n')



def request_file_for_result_input():
    while True:
        file = input('Quel nom voulez-vous pour le fichier de resultats .txt qui sera deposé à la racine? '
                     '(Defaut : results)')
        if not file:
            file = "results"
        file += '.txt'

        try:
            file = re.search("^[\w,\s-]", file)
            return file.string
        except AttributeError:
            print('Certains caractères ne sont pas valides.\n')


def main():
    print('Bienvenu dans Spam Comparator!\n')

    path = request_path_input()
    date = request_date_input()
    days = request_days_input()
    file_name_for_result = request_file_for_result_input()

    spam_comparator = SpamComparator(path, date, days, file_name_for_result)
    spam_comparator.run()


if __name__ == '__main__':
    DIRECTORY_PATH = './'
    main()
