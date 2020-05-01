#!/usr/bin/python3


class BitMap():
    '''This builds provides common utilites to build out a value to
    binary mapping.
    Methods:
        add_map - Adds a key (string) and a integer value to the map.

        map - Returns the binary string of the value associated with the key
              specified.
        validate_bit_count - verifies that the value passed for the number of
                             bits for the map is an integer.
    '''
    def __init__(self):
        return

    def add_map(self, key, value):
        self.mapping[key] = value
        return

    def map(self, key):
        if key not in self.mapping.keys():
            raise ValueError('Unknown key is not present.')
        return format(self.mapping[key], self.bit_format)

    def validate_bit_count(self, bit_count):
        if not isinstance(bit_count, int) or isinstance(bit_count, bool):
            raise TypeError('bit_count must be an integer.')
        if bit_count not in range(1, 32):
            raise ValueError('bit_count must be between 1 and 32 bits.')
        self.bit_format = '0{}b'.format(bit_count)
        return


def main():
    pass


if __name__ == '__main__':
    main()
