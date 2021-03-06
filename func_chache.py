# Creator: Alexander Ryan
# Task allocated by TradeWeb - Mike Byrne

# Tasks:
# System to cache sovereign bonds consiting of a 4 part string
# Add and cancel orders
# Queries:
#   Search for Bond ID
#   Return all Bond IDs above a specified quantity (buy and sell)
#   Total quantity of orders
#   Difference between buy and sell
# Run and compile code
# Tests required

import re


def _trade(trade, cache_ids, cached_trades):
    if not re.fullmatch("ID([0-9])+ Bond[A-Z] '*[BS]'* [1-9][0-9]*", trade):  # Check matched format
        return "Incorrect trade format", True, cached_trades  # Due to wrong input
    trade_id = trade.split(" ")[0]
    if trade_id in cache_ids:
        return "Order ID already present!", True, cached_trades  # Due to wrong input
    cached_trades.append(trade)
    return f"Order cached: {trade}", False, cached_trades  # Success! End trading loop and return to start


def _cancel(cancel_id, cache_ids, cached_trades):
    if not re.fullmatch("ID[0-9]+", cancel_id):  # Check matched format
        return "\nIncorrect cancel format", True, cached_trades  # Due to wrong input
    if cancel_id not in cache_ids:
        return "\nTrade not cached", True, cached_trades  # Due to wrong input
    cached_trades = [order_id for order_id in cached_trades if cancel_id not in order_id]
    return "\nCache canceled", False, cached_trades  # Success! End canceling loop and return to start


def total_q(_input, directions):
    if _input in ("B", "S"):
        return f"{directions.count(_input)}"  # return the number of buy or sell trades
    elif _input == "ALL":
        return f"{len(directions)}"
    else:  # Fail if not B, S, or All
        return "Incorrect input"


def diff_q(directions):
    bought = directions.count("B")  # counts only the buy trades
    sold = len(directions) - bought  # finds sale trades
    return f"Number of trades Bought: {bought} and Sold: {sold}\n"


def quantity_q(quantity, quantities):
    if not re.fullmatch("[1-9][0-9]*", quantity):
        return "Incorrect quantity", True  # Due to wrong format or invalid number
    else:
        # count being the number of trades with a higher quantity value
        count = len([quant for quant in quantities
                     if quantity.isnumeric() and int(quant) > int(quantity)])
        return count, False  # Success, end quantity query loop


def bond_q(bond, bond_ids):
    if not re.fullmatch("Bond[A-Z]+", bond):  # Check format matched
        return "Incorrect format\n", True  # Due to wrong input
    elif bond not in bond_ids:  # Success due to either bond being found or not
        return "False", False
    else:
        return "True", False


def _query(query, queries, bond_ids, quantities, directions):
    if query not in queries:
        return "\nIncorrect query", True
    if query == "bond":  # Bond section
        bonding = True  # Keeping bond query running until success
        while bonding:
            bond = input("Input a Bond_ID in the form 'BondA': ")
            prin, bonding = bond_q(bond, bond_ids)
            print(prin)
            # bonding = bon
        return "", True
    elif query == "quantity":  # Quantity section
        quantifying = True  # Keeping bond query running until success
        while quantifying:
            quantity = input("Input a quantity higher than 0: ")
            prin, quantifying = quantity_q(quantity, quantities)
            print(prin)
            # quantifying = quan
        return "", True
    elif query == "total":  # Total section, enforce upper to normalise
        total = input("Input a direction either All or B or S: ").upper()
        print(total_q(total, directions))
        return "", True

    elif query == "diff":  # Difference section
        print(diff_q(directions))
        return "", True
    else:  # Exit queries
        return "", False


def cacher():
    cached_trades = []  # Store all information
    while True:
        cache_ids = [cache.split(" ")[0] for cache in cached_trades]  # Divide info. into different lists
        bond_ids = [cache.split(" ")[1] for cache in cached_trades]
        directions = [cache.split(" ")[2] for cache in cached_trades]
        quantities = [cache.split(" ")[3] for cache in cached_trades]

        process = input("Would you like to trade, cancel, query or exit: ").lower()  # Normalise with lower
        processes = ("trade", "cancel", "query", "exit")
        if process in processes:  # Make sure only a few options are available

            if process == "trade":  # Adding section
                trading = True  # Sets up an individual while loops to keep trading running until success
                while trading:
                    trade = input("Insert a trade, in the form - ID1 BondD B 10000: ").replace("'", "")  # Clean input
                    prin, trading, cached_trades = _trade(trade, cache_ids, cached_trades)
                    print(prin)
                    # trading = trad

            elif process == "cancel":  # Cancel section
                canceling = True  # Sets up an individual while loops to keep canceling running until success
                while canceling:
                    if len(cached_trades) == 0:
                        print("No trades cached to cancel")
                        canceling = False
                    else:
                        cancel_id = input(f"Please select an Order_ID from the following: "
                                          f"\n {cached_trades} \n In the form 'ID1: ")
                        prin, canceling, cached_trades = _cancel(cancel_id, cache_ids, cached_trades)
                        print(prin)
                        # canceling = can
            elif process == "query":  # Query section
                querying = True  # Keeping the section running until success or exit chosen
                while querying:
                    if len(cached_trades) == 0:  # Check if any trades present before moving on
                        print("No trades cached to query")
                        querying = False  # End while loop
                    else:  # Trades are present
                        query = input(f"\tSearch if a Bond ID is cached - with 'bond'"
                                      f"\n\tBond IDs above a specified quantity (buy and sell)  - with 'quantity'"
                                      f"\n\tTotal number of cached trades - with 'total'"
                                      f"\n\tDifference between buy and sell trades - with 'diff'"
                                      f"\n\tOr Exit - with exit"
                                      f"\nChoose a query from above: ").lower()  # Normalise with lower
                        queries = ('bond', 'quantity', 'total', 'diff', "exit")
                        prin, querying = _query(query, queries, bond_ids, quantities, directions)
                        print(prin)
                        # querying = que
            else:  # Exit program
                break
        else:  # Wrong Input
            print("Wrong input.")
        print(f"\nCurrent Cache:  {cached_trades}\n")  # Show current cached trades


if __name__ == '__main__':
    cacher()
