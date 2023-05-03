import argparse
import math
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
    return "1" * x + "0"

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
    r = bin(x)[2:]
    if (len(r) <= l):
        r = r.zfill(l)

    else:
        r = r[-l:]

    return r

def log2(x: int):
    """
    Description:
        Calculates the logarithm of a number to base 2.

    Parameters:
        x (int): The number to calculate the logarithm of.

    Returns:
        int: The logarithm of the number.
    """
    return int(math.log(x, 2))

def pow2(x: int):
    """
    Description:
        Calculates the power of a number to base 2.

    Parameters:
        x (int): The number to calculate the power of.

    Returns:
        int: The power of the number.
    """
    return int(math.pow(2, x))

def encode_elias_delta(x: int):
    """
    Description:
        Encodes a number to elias delta.

    Parameters:
        x (int): The number to encode.

    Returns:
        str: The encoded binary number.
    """
    if (x == 1):
        return "0"

    kd = log2(x)
    kdd = log2(kd + 1)
    kdr = (kd + 1) - pow2(kdd)
    return to_unary(kdd) + " " + to_binary(kdr, kdd) + " " + to_binary(x, kdd)

def encode_elias_gamma(x: int):
    """
    Description:
        Encodes a number to elias gamma.

    Parameters:
        x (int): The number to encode.

    Returns:
        str: The encoded binary number.
    """
    if (x == 1):
        return "0"

    kd = log2(x)
    return to_unary(kd) + " " + to_binary(x, kd)

def decode_elias_delta(x: str):
    """
    Description:
        Decodes a binary number from elias delta.

    Parameters:
        x (str): The binary number to decode.

    Returns:
        int: The decoded integer.
    """
    x = x.replace(" ", "")
    if (not is_valid_binary(x)):
        return "ERROR"

    kdd = x.find("0" if x[0] == "1" else "1")
    if (kdd == -1):
        return "ERROR"

    kdd_b = x[kdd+1:2*kdd+1]
    kd_b = x[kdd+kdd+1:]
    kd = len(kd_b)
    kr = int(x[-kd:], 2)
    kdr = int(kdd_b, 2)
    
    if (len(x) != kd + (2 * kdd) + 1):
        return "ERROR"

    kdd_compare = log2(kd + 1)
    kdr_compare = (kd + 1) - pow2(kdd_compare)
    kdd_b_compare = to_binary(kdr_compare, kdd_compare)
    print(kdd, kdd_compare, kdr, kdr_compare, kdd_b, kdd_b_compare)
    if (kdd != kdd_compare or kdr != kdr_compare or kdd_b != kdd_b_compare):
        return "ERROR"

    return kr + 2 ** kd

def decode_elias_gamma(x: str):
    """
    Description:
        Decodes a number from elias gamma.

    Parameters:
        x (str): The number to decode.

    Returns:
        int: The decoded number.
    """
    x = x.replace(" ", "")
    if (not is_valid_binary(x)):
        return "ERROR"

    if (x == "0"):
        return 1

    kd = x.find("0" if x[0] == "1" else "1")
    if (kd == -1 or len(x) != kd*2 + 1):
        return "ERROR"

    try:
        kr = x[kd+1:(kd * 2)+1]
    except:
        return "ERROR"

    return 2**kd + int(kr, 2)

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
    parser.add_argument("data", help="The data to encode or decode.")
    args = parser.parse_args()

    if (args.encode and args.decode):
        print("Error! Cannot encode and decode at the same time.")
        return

    elif (args.encode):
        encode = "e"

    elif (args.decode):
        encode = "d"

    else:
        print("Error! Need to provide an encoding or decoding.")
        return

    if (args.alg == "delta"):
        algo_type = "d"

    elif (args.alg == "gamma"):
        algo_type = "g"

    else:
        print("Error! Need to provide an algorithm.")
        return

    algo = FUNCTION_MAP[f"{encode}{algo_type}"]
    data = [(int(x) if encode == "e" else x) for x in args.data[1:-1].split(",")]
    for num in data:
        print(algo(num))

    return

if (__name__ == "__main__"):
    main()