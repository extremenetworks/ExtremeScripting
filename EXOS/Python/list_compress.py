
# list_compress.py
#
# This script takes a string of numerical values and compresses them into a string of condensed numerical ranges
#
#
# Last updated: 06-26-2017

import argparse
import re
# import traceback  #Only used for test cases

"""This script takes a string of numerical values and compresses them into a string of condensed numerical ranges

This script is actually a test/example container for the list_compress() function. EXOS outputs occasionally display
numerical ranges (i.e port numbers and VLAN IDs) inefficiently, consuming valuable screen space.
This list_compress() function will compress the list down to the most efficient string possible.

Note: Slot/Chassis numbers are also supported.

"""


def list_compress(input_lst):
    """ Compresses a list/string of numerical ranges into the most efficient EXOS CLI supported list structure


    :param input_lst: EXOS friendly list string or python list i.e "1:1, 1:2, 1:4-5" or "['1:1', '1:2', '1:4-5']"
    :return: string containing compressed EXOS CLI friendly list of numbers
    """
    def expand_range(in_range):
        """ Expands a range of numbers i.e 1-5

        :param in_range: string containing single port range
        :return: list of integers containing expanded numerical range
        """
        if '-' not in in_range:
            error('Invalid format for range: {0}'.format(in_range))
        expanded = []
        in_range = in_range.split('-')
        first = int(in_range[0])
        last = int(in_range[1])
        if first > last:
            error("Invalid input range {0}-{1}".format(first, last))
        for x in range((last - first) + 1):
            expanded.append(first + x)
        return expanded

    def divide_stack(in_list):
        """ Splits a list of slotted numerical ranges into a dict with key of each slot

        ['1:2', '1:3', '2:1'] would become { 1: ['2', '3'], 2: ['1']}

        :param in_list: list of slotted numerical ranges
        :return: dict with key for each slot and list of numerical strings
        """
        slots = {}
        for entry in in_list:
            # split slot from entry and remove white space and empty list elements
            item = filter(None, entry.replace(' ', '').split(':'))
            # if item does not contain two elements then the slot/port information was incorrect
            if len(item) != 2:
                error('Invalid Slot/Port Combination: \'{0}\''.format(entry))
                continue

            slot = int(item[0])
            if slot in slots:
                slots[slot].append(item[1])
            else:
                slots[slot] = [item[1]]
        return slots

    def compress(fmtd_lst):
        """ Compress a sorted list of integers into a list of strings

        :param fmtd_lst: sorted list of integers
        :return:  list of strings compressed to EXOS CLI-friendly format
        """
        final_lst = []
        # First_seq holds the first sequential value in the active range
        first_seq = None
        # Walk through the sorted list
        for item in fmtd_lst:
            index = fmtd_lst.index(item)
            if index == 0:
                # Check if there is only one entry, if so add to final list
                if index == len(fmtd_lst) - 1:
                    final_lst.append('{0}'.format(item))
                    continue
                # On first entry set first_seq if next entry is sequential
                elif fmtd_lst[index + 1] - item == 1:
                    first_seq = item
                    continue
                # If next entry is not sequential add entry to final list
                final_lst.append('{0}'.format(item))
            # Check for last entry in list
            elif index == len(fmtd_lst) - 1:
                # If last entry is sequential to previous entry append range
                if item - fmtd_lst[index - 1] == 1:
                    final_lst.append('{0}-{1}'.format(first_seq, item))
                # Otherwise append single last entry
                else:
                    final_lst.append('{0}'.format(item))
            # If not first or last entry
            else:
                # Get value of next entry
                next = fmtd_lst[fmtd_lst.index(item) + 1]
                # Get value of previous entry
                prev = fmtd_lst[fmtd_lst.index(item) - 1]
                # If current entry is sequential with both next and prev do nothing
                if next - item == 1 and item - prev == 1:
                    continue
                # If current index is not within 1 of prev or next append it and clear first_seq
                elif next - item != 1 and item - prev != 1:
                    final_lst.append('{0}'.format(item))
                    first_seq = None
                # If current is sequential to prev but not sequential to next append previous range and clear first_seq
                elif next - item != 1 and item - prev == 1:
                    final_lst.append('{0}-{1}'.format(first_seq, item))
                    first_seq = None
                # If next is sequential to current but previous is not set first_seq
                elif next - item == 1 and item - prev != 1:
                    first_seq = item
        return final_lst

    def dedup_list(dup_lst):
        """remove any duplicate entries

        :param dup_lst: list of integers with potential duplicates
        :return: list of integers with duplicates removed
        """
        dedup = []
        for item in dup_lst:
            if item in dedup:
                continue
            dedup.append(item)
        return dedup

    def sort_list(unsort_lst):
        """Sort the list of integers

        :param unsort_lst: unsorted list of integers
        :return: sorted list of integers
        """
        return sorted([int(value) for value in unsort_lst])

    def is_stack(inp_lst):
        """ Check to see if inputted list is a stack (i.e contains slots "1:1")

        :param inp_lst: list of strings
        :return: True if any string contains ":" otherwise False
        """
        for entry in inp_lst:
            if ":" in entry:
                return True
        return False

    def error(error_type):
        """ Raise an error if there is an issue with an inputted value

        :param error_type: error message to be printed
        :return: nothing, raises exception
        """
        raise ValueError(error_type)

    # Determine if inputted value is a string or list of strings
    if type(input_lst) is str:
        # Check to make sure the string is properly formatted (i.e. contains only whitespace, numbers, and :,-
        if not re.match("^[\d\s\-:,]*$", input_lst):
            error("Invalid Character String: \'{0}\'".format(input_lst))
        # split data into lists on "," and remove whitespace and empty list elements
        input_lst = filter(None, [x.replace(' ', '') for x in input_lst.split(',')])
    # Check if inputted data is a list
    elif type(input_lst) is list:
        for item in input_lst:
            # Check to make sure the string is properly formatted (i.e. contains only whitespace, numbers, and :-
            if not re.match("^[\d\s\-:]*$", item):
                error("Invalid Character String: \'{0}\'".format(item))
            # Remove whitespace
            input_lst[input_lst.index(item)] = item.replace(' ', '')
        # Remove any empty list elements
        input_lst = filter(None, input_lst)
    # Data is not list nor string, error out
    else:
        error("Unknown Input Formatting Error")

    out_string = ''
    # Check to see if list contains slot information
    if is_stack(input_lst):
        # Divide the stack into dict
        stack_lst = divide_stack(input_lst)
        # Create dict for finalized stack list
        final_stack_lst = {}
        # Walk through each slot and create list of numerical entries
        for slot in stack_lst:
            # Create dict key for final slot info
            final_stack_lst[slot] = []
            for item in stack_lst[slot]:
                # Check for '-' and expand to numerical values
                if '-' in item:
                    for number in expand_range(item):
                        final_stack_lst[slot].append(number)
                    continue
                final_stack_lst[slot].append(int(item))
            # Sort, deduplicate, and compress final slot info
            final_stack_lst[slot] = compress(dedup_list(sort_list(final_stack_lst[slot])))

        for slot in final_stack_lst:
            # Build the output string from dictionary
            for item in final_stack_lst[slot]:
                out_string += '{0}:{1}, '.format(slot, item)
        return out_string.strip(', ')
    # Inputted value does not contain a stack
    else:
        # Create final list for output string
        final_lst = []
        for item in input_lst:
            # Expand any ranges and add to final list
            if '-' in item:
                for number in expand_range(item):
                    final_lst.append(number)
                continue
            # Add other values to final list
            final_lst.append(int(item))
        # Sort, deduplicate, compres and Build output string from final list
        for item in compress(dedup_list(sort_list(final_lst))):
            out_string += '{0}, '.format(item)
        return out_string.strip(', ')


def main():
    """Converts inputted arguments and executes list_compress function

    :return: Prints compressed numerical ranges to screen
    """

    parser = argparse.ArgumentParser(prog='list_compress.py', description = "Compress a string of numerical values into ranges")
    parser.add_argument("lst", help="List of values.  Should be enclosed in quotes "
                                        "(i.e. list_compress.py \"1:1, 1:2, 1:3, 1:4-10\")")

    args = parser.parse_args()
    input_lst = args.lst

    print list_compress(input_lst)


    """
    # Text Cases and Code for Executing Test
    string_test = [
        ['  , 1, 4, 3, 5, 6, 10, 12, 11, 13, 15, 8, 17, 19, 20, 21, 24, 26, 31-33', '1, 3-6, 8, 10-13, 15, 17, 19-21, 24, 26, 31-33'],
        ['1:1,1:2, 1:2, 1:4,1:3,2:1,2:2,  2:3,2:5,  3:1-5', '1:1-4, 2:1-3, 2:5, 3:1-5'],
        ['1001, 1003,  1005, 1004, 1002, 1006, 2001, 2003, 2004, 2002, 2006','1001-1006, 2001-2004, 2006'],
        ['1:1, 1:3,  2:3, 2:1, 3:3, 1:2,2:2, 3:2, 3:4, 3:6','1:1-3, 2:1-3, 3:2-4, 3:6'],
        [['1', '2', '3', '4', '5', '6', '10', '11', '12', '13'], '1-6, 10-13'],
        [['1:1', ' 1:2','1:3','2:1','2:2 ','2:3','2:5', '3:1-5', '10:1'], '1:1-3, 2:1-3, 2:5, 3:1-5, 10:1'],
        [['1001', '1003',  '1005', '1004', '1002', '1006', '2001', '2003', '2004', '2002', '2006'], '1001-1006, 2001-2004, 2006'],
        [[ ' ',  '1:1 ', ' 1:3', '2:3', '2:1', '3:3', '1:2', '2:2', '3:2', '3:4', '3:6'], '1:1-3, 2:1-3, 3:2-4, 3:6'],
        # # Bad Data that can't be handled, raises exceptions
        # [[1, 2, 3, 4, 5, 6, 10, 11, 12, 13], ['1-6', '10-13']],
        # [['1', '2', '3', '4' '5', '6', '10', '11' '12', '13'], '1-6, 10-13'],
        # [['1:1', '1:2', '1:3', '2:1', '2:2', '2:3', '2:5', '3:1-5', '1:'], ['1:1-3', '2:1-3', '2:5', '3:1-5']],
        # [[1001, '1003', 1005, '1004', '1002', '1006', '2001', '2003', '2004', '2002', '2006'], ['1001-1006', '2001-2004', '2006']],
    ]

    for item in string_test:
        try:
            if list_compress(item[0]) == item[1]:
                print 'PASS'
                continue
            print 'Test String: {0}'.format(item[0])
            print 'FAIL Final String: {0}'.format(list_compress(item[0]))
        except ValueError as e:
            print 'FAIL Error: {0}'.format(e)
        except Exception as e:
            print 'Other Error: {0}'.format(e)
            traceback.print_exc()
    """

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        pass
