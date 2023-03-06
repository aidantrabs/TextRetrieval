import argparse
import sys
from math import log, floor, pow
from typing import List

ALPHA_NUM = "abcdefghijklmnopqrstuvwxyz23456789"


def is_valid_binary(x: str):
    """
    Description:
        Checks if a string is a valid binary number.

    Parameters:
        x (str): The string to check.

    Returns:
        bool: True if the string is a valid binary number, False otherwise.
    """
    return len(set(x).intersection(ALPHA_NUM)) == 0


def to_unary(x: int):
    """
    Description:
        Converts a number to unary.

    Parameters:
        x (int): The number to convert.

    Returns:
        str: The unary representation of the number.
    """
    return (x - 1) * "0" + "1"


def to_binary(x: int, l: int):
    """
    Description:
        Converts a number to binary.

    Parameters:
        x (int): The number to convert.
        l (int): The length of the binary number.

    Returns:
        str: The binary representation of the number.
    """
    s = "{0:0%db}" % l
    return s.format(x)


def to_binary_no_msb(x: int):
    """
    Description:
        Converts a number to binary without the most significant bit.

    Parameters:
        x (int): The number to convert.

    Returns:
        str: The binary representation of the number.
    """
    b = "{0:b}".format(int(x))
    return b[1:]


def log2(x: int):
    """
    Description:
        Calculates the logarithm of a number to base 2.

    Parameters:
        x (int): The number to calculate the logarithm of.

    Returns:
        int: The logarithm of the number.
    """
    return log(x, 2)


def encode_elias_delta(x: int):
    """
    Description:
        Encodes a number to elias delta.

    Parameters:
        x (int): The number to encode.

    Returns:
        str: The encoded binary number.
    """
    if(x == 0):
        return "0"

    n = 1 + floor(log2(x))
    return to_unary(n) + to_binary_no_msb(x)


def encode_elias_gamma(x: int):
    """
    Description:
        Encodes a number to elias gamma.

    Parameters:
        x (int): The number to encode.

    Returns:
        str: The encoded binary number.
    """
    if(x == 0):
        return "0"

    l = int(log2(x))
    n = 1 + l
    b = x - 2 ** l
    return to_unary(n) + to_binary(b, l)


#TODO: FIX
def decode_elias_delta(x: str):
    """
    Description:
        Decodes a number from elias delta.

    Parameters:
        x (str): The number to decode.

    Returns:
        int: The decoded number.
    """
    if(not is_valid_binary(x)):
        return "ERROR"

    x = list(x)
    k = 0
    while(x[k] == "0"):
        k += 1

    x = x[2*k+1:]
    x.reverse()
    x.insert(0, "1")
    n = 0

    for i in range(len(x)):
        if(x[i] == "1"):
            n = n + pow(2, i)

    return int(n)


def decode_elias_gamma(x: str):
    """
    Description:
        Decodes a number from elias gamma.

    Parameters:
        x (str): The number to decode.

    Returns:
        int: The decoded number.
    """
    if(not is_valid_binary(x)):
        return "ERROR"

    x = list(x)
    k = 0
    while(x[k] == "0"):
        k += 1

    x = x[k:2*k+1]
    n = 0
    x.reverse()

    for i in range(len(x)):
        if(x[i] == "1"):
            n += pow(2, i)

    return int(n)


def main():
    FUNCTION_MAP = {
        "ed": encode_elias_delta,
        "eg": encode_elias_gamma,
        "dd": decode_elias_delta,
        "dg": decode_elias_gamma
    }

    parser = argparse.ArgumentParser(prog="Elias Coding", description="Elias Coding")
    parser.add_argument("--alg", help="The algorithm to use. Can be either 'elias_delta' or 'elias_gamma'.", type=str)
    parser.add_argument("--encode", help="Encode the data.", action="store_true")
    parser.add_argument("--decode", help="Decode the data.", action="store_true")
    parser.add_argument("data", help="The data to encode or decode.", type=str)
    args = parser.parse_args()

    if(args.encode and args.decode):
        print("Error! Cannot encode and decode at the same time.")
        return

    elif(args.encode):
        encode = "e"

    elif(args.decode):
        encode = "d"

    else:
        print("Error! Need to provide an encoding or decoding.")
        return

    if(args.alg == "delta"):
        algo_type = "d"

    elif(args.alg == "gamma"):
        algo_type = "g"

    else:
        print("Error! Need to provide an algorithm.")
        return

    algo = FUNCTION_MAP[f"{encode}{algo_type}"]
    data = [(int(x) if encode == "e" else x) for x in args.data[1:-1].split(",")]
    for num in data:
        print(algo(num))


if (__name__ == "__main__"):
    main()
