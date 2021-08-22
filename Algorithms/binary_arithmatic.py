from typing import cast


def get_binary(decimal, binary=[]):
    if decimal >= 1:
        get_binary(decimal // 2)
    binary.append(decimal % 2)
    return binary

def get_decimal(binary):
    decimal_sum = 0
    for b,i in zip(binary,range(len(binary)-1,-1,-1)):
        decimal_sum +=  (b * (2 ** i))
    return decimal_sum

try:
    decimal = int(input("Enter decimal number: "))
    binary_conversion = get_binary(decimal)
    print(binary_conversion)
    decimal_conversion = get_decimal(binary_conversion)
    print(decimal_conversion)
except ValueError:
    print("Invalid Input!")
