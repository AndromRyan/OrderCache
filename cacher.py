# Creator: Alexander Ryan
# Task allocated by TradeWeb - Mike Byrne
# Started: 20/08/2020 - 14:48
# Ended:

# System to cache sovereign bonds consiting of a 4 part string
# Order can be canceled by order ID
# Orders can have multiple bond IDs

# Tasks:
# Add and cancel orders
# Queries:
#   Search for Bond ID
#   Return all Bond IDs above a specified quantity (buy and sell)
#   Total quantity of orders
#   Difference between buy and sell
# Run and compile code
# Tests required

import re
import sys
import getopt
import pandas

# import pickle

"""
flag system
    -a --add "order string" 
    -c --cancel "order_id"
    -b --bond "bond_id"
    -q --quantity "1000"
    -t --total
    -d --difference
"""
"""
Flow
    on load read file and store locally self.cache
    -a take the string, slpit into 4 parts, search cache for order_id, if exist error, if not add to end
    -c take order_id, search cache for id, if present remove from cache if not error
    -b take bond_id, search bond_id in cache collum, if exist return true else false
    -q take quantity, search quantity in cache collum, if found return all bond_ids with a greater quantity
    -t return total number of trades
    -d return difference of buy and sell
"""

"""
pandas as collum search is easy and fast
pickle the data each time to store 
"""


def print_help():
    # Help statement on -h flag
    help_width = 78
    print(f'''\n      |{help_width * "="}|
      |                     Help statement for cacher.py -...                        |
      |\t-h or --help               \t To print help statement                     |
      |\t-a --add "[order strings]" \t Add orders to the cache                     |
      |\t-c --cancel "order_id"     \t Cancel a specific order by ID               |
      |\t-b --bond "bond_id"        \t Search if bond_id is present                |
      |\t-q --quantity "1000"       \t Return all bond_ids with a greater quantity |
      |\t-t --total                 \t Return how many transaction present         |
      |\t-d --difference            \t Return difference of buy and sell trades    |
      |\t-s --show                  \t Shows all cached trades                     |''')
    print("      |" + (help_width * "=") + "|\n")


def system_input(pandas):
    # Read the arguments from command line
    full_cmd_arguments = sys.argv

    # Keep all but the first
    argument_list = full_cmd_arguments[1:]
    # print(argument_list)

    short_options = "ha:c:b:q:td"
    long_options = ["help", "add=", "cancel=", "bond=", "quantity=", "total", "difference"]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)

    # Evaluate given options
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print_help()
        elif current_argument in ("-a", "--add"):
            print("Enabling caching mode")
            cache_adder(pandas, current_value)
        elif current_argument in ("-c", "--cancel"):
            print("Adding locat: (%s)" % current_value)
        elif current_argument in ("-b", "--bond"):
            print("Adding dir: (%s)" % current_value)
        elif current_argument in ("-q", "--quantity"):
            print("Enabling Auto directory mode from: (%s)" % current_value)
        elif current_argument in ("-t", "--total"):
            print("Enabling special output mode (%s)" % current_value)
        elif current_argument in ("-d", "--difference"):
            print("Enabling special output mode (%s)" % current_value)

    return cache_pandas


def pandas_add(data_frame, order):
    [order_id, bond_id, direction, quantity] = order.split(" ")
    new_row = {"Order_ID": order_id, "Bond_ID": bond_id, "Direction": direction, "Quantity": int(quantity)}
    if order_id in data_frame["Order_ID"].values:
        print(f"Error - orderID: {order_id} already used - no changes made ## WORK on")
    else:
        data_frame = data_frame.append(new_row, ignore_index=True)
        print(f"Cached : {new_row}")
    return data_frame


def pandas_cancel(data_frame, order_id):
    data_frame = data_frame[data_frame.Order_ID != order_id]
    return data_frame


def cache_adder(data_frame, add_list):
    add_list = add_list.replace("'", "")
    add_stripped = add_list.replace(" ", "")
    if add_stripped.isalnum():
        add_trade = add_list
        data_frame = pandas_add(data_frame, add_trade)
    elif ("[" == add_list[0]) and ("]" == add_list[-1]):
        add_list = add_list[1:-1]
        print(add_list.split(","))
    else:
        print("IOError - invalid trade/s")



cached_dict = {"Order_ID": ["ID1", "ID2", "ID3", "ID4", "ID5"],
               "Bond_ID": ["BondA", "BondB", "BondA", "BondB", "BondC"],
               "Direction": ['B', 'S', 'B', 'B', 'B'],
               "Quantity": [1000, 1500, 500, 1000, 2000]}

cache_pandas = pandas.DataFrame(data=cached_dict)
# cache_pandas = pandas_add(cache_pandas, "ID6", "BondA", "B", 3444)
# cache_pandas = pandas_cancel(cache_pandas, "ID1")
# print(cache_pandas)
system_input(cache_pandas)
print(cache_pandas)
trade = "ID6 BondD 'B' 8888"
