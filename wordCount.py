"""
computeStatistics.py es el ejercicio 1
"""

import os
import sys
import time


if __name__ == '__main__':
    IS_SUCCESSFUL = False

    out_path = os.path.join(os.getcwd(), 'WordCountResults.txt')

    while not IS_SUCCESSFUL:
        try:
            file = sys.argv[1]
            print(f'Archivo a procesar: {file}')
        except IndexError:
            file = input('Ingrese el nombre del archivo a procesar: ')

        path = os.path.join(os.getcwd(), file)

        if not os.path.exists(path):
            print('El archivo que se ingresó, no existe')
            continue

        start_time = time.time_ns()
        IS_SUCCESSFUL = True
        with open(path, 'r', encoding='utf8') as data_file:
            full_text = data_file.read()

        lines = full_text.split('\n')
        data_list = []

        for line in lines:
            data_list.extend(line.split(' '))

        count_dict = {word:data_list.count(word) for word in data_list}

        ordered_count_dict = dict(sorted(
            count_dict.items(), key=lambda x:x[1], reverse=True))
        OUTPUT_TEXT = 'Word\t/\tFrequency\n'
        WORDS_SUM = 0

        for word, freq in ordered_count_dict.items():
            OUTPUT_TEXT += f'{word}\t/\t{freq}\n'
            WORDS_SUM += freq
        OUTPUT_TEXT += f'Total Words: {WORDS_SUM}'

        print(OUTPUT_TEXT)

        with open(out_path, 'w', encoding='utf8') as results:
            results.write(OUTPUT_TEXT)
        