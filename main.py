from tqdm import tqdm
from genericpath import exists
from urllib import response
import requests
import os


#Return opereraiting system (windows or linux) path separator
def check_sys(cwd):
    temp = str(cwd)
    if temp.find('\\') != -1:
        return '\\'
    elif temp.find('/') != -1:
        return '/'

#Write progress bar
def write_progress(how_much_done, how_much_to_check, message):
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Calculate the progress percentage
    progress_percentage = (how_much_done / how_much_to_check) * 100

    # Print the message and create a tqdm progress bar
    print(message)
    with tqdm(total=how_much_to_check, desc='Progress ' + str("{0:.2f}".format(progress_percentage)) + '%', position=0, leave=True, dynamic_ncols=True) as pbar:
        # Simulate processing each step
        for _ in range(how_much_done):
            pbar.update(round(how_much_done / 20))
    print()

#Writes python files to new directory
def makes_py1(file_name):
    # Opening file with the addresses of the search engines and writing them in a new file
    with open(file_name, 'r') as file:
        lines = file.readlines()
    file_output_name = 'search_engines.txt'    
    with open(file_output_name, 'w') as f_write:
        for i, line in enumerate(lines):
            write_progress(i, len(lines), 'Looking for .py files names')
            if '.py' in line:
                f_write.write(line[line.find('https'):line.find('.py') + 3] + '\n')

    # Making a new directory
    search_engines_dir = os.path.join(os.getcwd(), 'search engines')
    if not exists(search_engines_dir):
        os.makedirs(search_engines_dir)

    # Opening file with the addresses and writing .py files in the new directory
    with open(file_output_name, 'r') as f_read:
        lines = f_read.readlines()
    for i, line in enumerate(lines):
        write_progress(i, len(lines), 'Writing .py files in folder "search engines"')
        response = requests.get(line[:-1])
        filename = os.path.join(search_engines_dir, line[line.rfind('/') + 1:-1])
        open(filename, 'wb').write(response.content)

#Display program description
print('Program \'wycina\' z podanego pliku linki https z koncowka \'.py\'\nNastepnie pobiera zawartosc znajdujaca sie w danych adresach do folderu uruchomienia programu.\nFinalnie wystarczy \'przesunac\' pobrane pliki do okienka, gdzie dodaje sie wyszukiwarki torrent.\nPlik ktory ja analizuje to \'Unofficial-search-plugins.mediawiki\' pobrany z github-a: \'https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins\'\n')

#Choosing program option, 1 - manual, 2 - auto, based on old link
option = input('Wybierz opcje:\n1\tPodanie pliku do analizy\n2\tProba automatuczna\n')
match (option):
    #Manual option - input file name with python scripts names
    case '1':
        file_input_name = input('Podaj nazwe pliku do analizy:\n')
        try:
            makes_py1(file_input_name)
        except:
            print('Nie udalo sie otworzyc pliku\nSprawdz czy podano poprawną nazwę pliku')
    #Auto option - download file from github
    case '2':
        ok = True
        try:
            url = 'https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins#plugins-for-public-sites'
            html_f = open('temp.txt', 'w')
            for line in requests.get(url).text.split('\n'):
                html_f.write(line + '\n')
            html_f.close()
        except:
            ok = False
            print('Nie udalo sie pobrac pliku')
        if ok:
            try:
                makes_py1('temp.txt')
                print('Skrypt został wykonany pomyslnie, pluginy sa w nowym folderze\n')
            except:
                print('Nie udalo sie wykonac skryptu automatycznie\nSprawdz czy adres html w kodzie jest poprawny')
#Cleaning, removing temp files
try:
    os.remove('temp.txt')
    os.remove('search_engines.txt')
except:
    print('Nie udalo sie usunac plikow tymczasowych')
