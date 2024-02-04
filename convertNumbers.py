"""
convertNumbers.py es el ejercicio 2
"""

import os
import sys
import time


def hexadecimal_values_conversion(dec_value: int) -> str:
    """
    Function that converts a single decimal value to hexadecimal equivalent
    """
    if dec_value < 10:
        hex_value = str(dec_value)
    elif dec_value == 10:
        hex_value = 'A'
    elif dec_value == 11:
        hex_value = 'B'
    elif dec_value == 12:
        hex_value = 'C'
    elif dec_value == 13:
        hex_value = 'D'
    elif dec_value == 14:
        hex_value = 'E'
    else:
        hex_value = 'F'

    return hex_value


def hexadecimal_digit_inverter(digit: int) -> str:
    """
    Inverts the digit in hexadecimal value
    """
    if digit in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        inverted_digit = hexadecimal_values_conversion(15-int(digit))
    elif digit == 'A':
        inverted_digit = '5'
    elif digit == 'B':
        inverted_digit = '4'
    elif digit == 'C':
        inverted_digit = '3'
    elif digit == 'D':
        inverted_digit = '2'
    elif digit == 'E':
        inverted_digit = '1'
    else:
        inverted_digit = '0'
    return inverted_digit


def hexadecimal_conversion(dec_number: int) -> str:
    """
    Converts a number on decimal to hexadecimal
    """
    decimal = abs(dec_number)

    if decimal <= 15:
        hexadecimal = hexadecimal_values_conversion(int(dec_number))
    else:
        hexadecimal = ''

    while decimal > 15:
        quotient, remainder = divmod(decimal, 16)
        decimal = int(quotient)
        new_digit = hexadecimal_values_conversion(int(remainder))
        hexadecimal = f'{new_digit}{hexadecimal}'
        if decimal <= 15:
            new_digit = hexadecimal_values_conversion(decimal)
            hexadecimal = f'{new_digit}{hexadecimal}'

    return hexadecimal


def negative_hexadecimal_conversion(decimal: str) -> str:
    """
    Converts hexadecimal to negative hexadecimal
    """
    ref_hexadecimal = hexadecimal_conversion(abs(decimal)-1)
    negative_hexadecimal = ''

    for _ in range(10-len(ref_hexadecimal)):
        negative_hexadecimal += 'F'

    for digit in ref_hexadecimal:
        negative_hexadecimal += hexadecimal_digit_inverter(digit)

    return negative_hexadecimal


def binary_add_one(binary: str) -> str:
    """
    This function adds 1 to a binary
    """
    binary_plus_one = ''
    carry = 1

    for bit in binary[::-1]:
        if bit == '0':
            binary_plus_one = f'{carry}{binary_plus_one}'
            carry = 0
        else:
            if carry == 0:
                binary_plus_one = f'{1}{binary_plus_one}'
                carry = 0
            else:
                binary_plus_one = f'{0}{binary_plus_one}'
                carry = 1
    return binary_plus_one


def negative_binary(binary: str) -> str:
    """
    This function converts a binary to its negative
    """
    ref_binary = ''
    for _ in range(10-len(binary)):
        ref_binary += '1'

    for bit in binary:
        if bit == '1':
            ref_binary += '0'
        else:
            ref_binary += '1'

    neg_binary = binary_add_one(ref_binary)
    return neg_binary


def binary_conversion(dec_number: int) -> str:
    """
    Converts a number on decimal to binary
    """
    decimal = abs(dec_number)

    if decimal <= 1:
        binary = str(int(dec_number))
    else:
        binary = ''

    while decimal > 1:
        quotient, remainder = divmod(decimal, 2)
        decimal = int(quotient)
        binary = f'{int(remainder)}{binary}'
        if decimal == 1:
            binary = f'1{binary}'

    if dec_number < 0:
        binary = negative_binary(binary)

    return binary


if __name__ == '__main__':
    IS_SUCCESSFUL = False

    out_path = os.path.join(os.getcwd(), 'ConvertionResults.txt')

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
            try:
                number = float(no_comma_data)
                numbers.append(number)
            except ValueError:
                no_endline_data = data.replace('\n', '')
                print(f'El dato {no_endline_data} no representa un número')

        binary_numbers = [binary_conversion(number) for number in numbers]
        hexadecimal_numbers = []
        OUTPUT_TEXT = \
            'Decimal Number\t\tBinary Number\t\t\t\tHexadecimalNumber\n'
        print(OUTPUT_TEXT)
        for value in numbers:
            if value >= 0:
                positive_hex = hexadecimal_conversion(value)
                hexadecimal_numbers.append(positive_hex)
            else:
                negative_hex = negative_hexadecimal_conversion(value)
                hexadecimal_numbers.append(negative_hex)

        for dec, bina, hexa in zip(
                numbers, binary_numbers, hexadecimal_numbers):
            current_line = f'{int(dec)}'
            LEN_DEC = len(str(int(dec)))
            for _ in range((20-LEN_DEC)//4):
                current_line += '\t'
            current_line += bina
            for _ in range((36-len(bina))//4):
                current_line += '\t'
            current_line += f'{hexa}\n'
            print(current_line)
            OUTPUT_TEXT += current_line

        end_time = time.time_ns()
        time_delta = end_time - start_time

        print(f'El tiempo de ejecución fue de {time_delta} nanosegundos,\
 equivalente a {time_delta/1_000_000_000} segundos.')
        OUTPUT_TEXT += 'Execution time: {time_delta/1_000_000_000} s'

        with open(out_path, 'w', encoding='utf8') as results:
            results.write(OUTPUT_TEXT)
