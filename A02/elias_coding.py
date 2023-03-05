from math import log, floor, pow
import sys

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

    n = 1 + int(log2(x))
    b = x - 2 ** (int(log2(x)))
    l = int(log2(x))
    return to_unary(n) + to_binary(b, l)


def decode_elias_delta(x: int):
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
    while True:
        if(not x[k] == "0"):
            break
        k += 1

    x = x[2*k+1:]
    x.reverse()
    x.insert(0, "1")
    n = 0

    for i in range(len(x)):
        if(x[i] == "1"):
            n = n + pow(2, i)

    return int(n)


def decode_elias_gamma(x: int):
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
    while True:
        if(not x[k] == "0"):
            break

        k = k + 1

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

    try:
        data = (sys.argv[-1])[1:-2].split(",")
    except:
        print("Error. No data argument provided.")
        return

    try:
        algo_type = sys.argv[sys.argv.index("--alg") + 1]
    except:
        print("Error. Need to provide an algorithm.")
        return

    try:
        encode = "e" if "--encode" in sys.argv else "d"
    except:
        print("Error. Need to provide an encoding or decoding.")
        return

    algo = FUNCTION_MAP[f"{encode}{algo_type[0]}"]
    for num in data:
        print(algo(num))

if (__name__ == "__main__"):
    main()
