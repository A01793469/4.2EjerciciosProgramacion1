"""
computeStatistics.py es el ejercicio 1
"""

import os
import sys
import time
import math


def check_scientific_notation(num: float):
    """
    Check of the number to be on scientific notation.
    """
    if str(num)[-3] in ['+','-']:
        out_num = int(num)
    else:
        out_num = num
    return out_num


def mean_computation(mean_numbers: list) -> float:
    """
    Function that computes the mean value of a list of numbers
    """
    full_sum = sum(mean_numbers)
    mean = check_scientific_notation(full_sum/len(mean_numbers))
    return mean


def median_computation(median_numbers:list) -> float:
    """
    Function that computes the median value of a list of numbers
    """
    median_numbers.sort()
    amount_of_numbers = len(median_numbers)
    if amount_of_numbers % 2:
        median = check_scientific_notation(
            median_numbers[amount_of_numbers//2])
    else:
        prev_number = median_numbers[amount_of_numbers//2]
        next_number = median_numbers[(amount_of_numbers//2) + 1]
        median = check_scientific_notation((prev_number+next_number)/2)
    return median


def mode_computation(mode_numbers:list) -> (int, list):
    """
    Function that computes the mode value/s of a list of numbers
    """
    max_freq = 1
    numbers_frequency = []
    passed_numbers = []
    for mode_number in mode_numbers:
        frequency = mode_numbers.count(mode_number)

        if mode_number not in passed_numbers:
            passed_numbers.append(mode_number)
        else:
            continue

        if frequency > max_freq:
            max_freq = frequency
            numbers_frequency = [mode_number]
        elif frequency == max_freq:
            numbers_frequency.append(mode_number)

    if len(numbers_frequency) == len(mode_numbers):
        out_frequency = []
    else:
        out_frequency = numbers_frequency
    return max_freq, out_frequency


def variance_computation(variance_numbers: list) -> float:
    """
    Function that computes the variance value of a list of numbers
    """
    amount_values = len(variance_numbers)
    mean_value = mean_computation(variance_numbers)
    summatory = 0

    for variance_number in variance_numbers:
        delta = variance_number - mean_value
        delta_squared = delta ** 2
        summatory += delta_squared
    variance = check_scientific_notation(summatory/amount_values)
    return variance


def standard_deviation_computation(standard_deviation_numbers: list) -> float:
    """
    Function that computes the standard deviation value of a list of numbers
    """
    variance = variance_computation(standard_deviation_numbers)
    standard_deviation = check_scientific_notation(math.sqrt(variance))

    return standard_deviation


if __name__ == '__main__':
    IS_SUCCESSFUL = False

    print('Los decimales serán separados por puntos ".", mientras que las\
 comas se detectarán como separadores de miles, millares, etc.')

    out_path = os.path.join(os.getcwd(), 'StatisticsResults.txt')

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
            lines = data_file.readlines()

        data_list = []

        for line in lines:
            data_list.extend(line.split(' '))

        numbers = []
        for data in data_list:
            no_comma_data = data.replace(',','')
            if not no_comma_data[-1].isdigit():
                no_comma_data = no_comma_data[:-1]
            try:
                number = float(no_comma_data)
                numbers.append(number)
            except ValueError:
                no_endline_data = data.replace('\n', '')
                print(f'El dato {no_endline_data} no representa un número')

        mean_val = mean_computation(numbers)
        median_val = median_computation(numbers)
        print(f'La cantidad de valores es: {len(numbers)}')
        print(f'El promedio de los valores es: {mean_val}')
        print(f'La mediana de los valores es: {median_val}')
        freq, mode_nums = mode_computation(numbers)
        std_dev_val = standard_deviation_computation(numbers)
        variance_val = variance_computation(numbers)

        if freq == 1:
            TIMES_AGG = 'vez'
            if len(mode_nums) == 1:
                MODES_STR = str(mode_nums[0])
            else:
                MODES_STR = 'No mode'
        else:
            TIMES_AGG = 'veces'
            MODES_STR = ''
            for ix, mode_num in enumerate(mode_nums):
                if ix:
                    MODES_STR += ', '
                MODES_STR += str(mode_num)

        if len(mode_nums) == 1:
            MODE_AGG = 'moda'
        else:
            MODE_AGG = 'modas'

        if not mode_nums:
            print(f'No hay moda, todos los valores se repiten {freq}\
 {TIMES_AGG}.')
        else:
            print(f'Hay {len(mode_nums)} {MODE_AGG}, que se repite {freq}\
 {TIMES_AGG}: {MODES_STR}')

        print(f'La desviación estandar de los valores: {std_dev_val}')
        print(f'La varianza de los valores es: {variance_val}')

        end_time = time.time_ns()
        time_delta = end_time - start_time

        print(f'El tiempo de ejecución fue de {time_delta} nanosegundos,\
 equivalente a {time_delta/1_000_000_000} segundos.')
        output_text = \
            f'''
            Mean: {mean_val}
            Median: {median_val}
            Mode: {MODES_STR}
            Standard Deviation: {std_dev_val}
            Variance: {variance_val}
            Execution time: {time_delta/1_000_000_000} s
            '''

        with open(out_path, 'w', encoding='utf8') as results:
            results.write(output_text)
        