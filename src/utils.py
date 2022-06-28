import math


def binary_to_int(binary_value):
    """
    The convention we use is the one of least significant bit at the left
    :param binary_value: The binary representation of the value to be transformed
    :return:
    """
    return sum([binary_value[i] * (2 ** i) for i in range(len(binary_value))])


def int_to_binary(value):
    """
    The convention we use is the one of least significant bit at the left
    :param value: value to be transformed into binary
    :return: a list containing the binary representation of value
    """

    # The log does not provide the correct result for 0
    if value == 0:
        return [0]

    length = math.floor(math.log(value, 2)) + 1
    l = [0] * length
    for i in list(range(length)):
        if value % 2 == 0:
            l[i] = 0
        else:
            value -= 1
            l[i] = 1
        value = value / 2
    return l


def split_list(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


if __name__ == "__main__":
    print(int_to_binary(2))
