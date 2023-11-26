from urllib import response
import requests

print('Program \'wycina\' z podanego pliku linki https z koncowka \'.py\'\nNastepnie pobiera zawartosc znajdujaca sie w danych adresach do folderu uruchomienia programu.\nFinalnie wystarczy \'przesunac\' pobrane pliki do okienka, gdzie dodaje sie wyszukiwarki torrent.\nPlik ktory ja analizuje to \'Unofficial-search-plugins.mediawiki\' pobrany z github-a: \'https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins\'\n')

file_input_name = input('Podaj nazwe pliku do analizy:\n')
file_output_name = 'search engines.txt'

f_read = open(file_input_name, 'r')
f_write = open(file_output_name, 'w')

for line in f_read:
    #print(line)
    if (line.find('.py') != -1):
        print('3')
        f_write.write(line[line.find('https'):line.find('.py') + 3] + '\n')
print('4')
f_read.close()
f_write.close()

f_read = open(file_output_name, 'r')
for line in f_read:
    print('5')
    
    response = requests.get(line[:-1])

    open(line[line.rfind('/') + 1:-1], 'wb').write(response.content)