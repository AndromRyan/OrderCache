# Creator: Alexander Ryan
# Task allocated by TradeWeb - Mike Byrne

# Tasks:
# System to cache sovereign bonds consisting of a 4 part string
# Add and cancel orders
# Queries:
#   Search for Bond ID
#   Return all Bond IDs above a specified quantity (buy and sell)
#   Total quantity of orders
#   Difference between buy and sell
# Run and compile code
# Tests required

import re


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
                    trade = input("Insert a trade, in the form 'ID1 BondD B 10000': ").replace("'", "")  # Clean up
                    if not re.fullmatch("ID([0-9])+ Bond[A-Z] '*[BS]'* [1-9][0-9]*", trade):  # Check matched format
                        print("Incorrect trade format")
                        continue  # Due to wrong input
                    trade_id = trade.split(" ")[0]
                    if trade_id in cache_ids:
                        print("Order ID already present!")
                        continue  # Due to wrong input
                    cached_trades.append(trade)
                    print(f"Order cached: {trade}")
                    trading = False  # Success! End trading loop and return to start

            elif process == "cancel":  # Cancel section
                canceling = True  # Sets up an individual while loops to keep canceling running until success
                while canceling:
                    if len(cached_trades) == 0:
                        print("No trades cached")
                        canceling = False
                    else:
                        cancel_id = input(f"Please select an Order_ID from the following: "
                                          f"\n {cached_trades} \n In the form 'ID1: ")
                        if not re.fullmatch("ID[0-9]+", cancel_id):  # Check matched format
                            print("\nIncorrect cancel format")
                            continue  # Due to wrong input
                        if cancel_id not in cache_ids:
                            print("\nTrade not cached")
                            continue  # Due to wrong input
                        cached_trades = [order_id for order_id in cached_trades if cancel_id not in order_id]
                        print("Cache canceled")
                        canceling = False  # Success! End canceling loop and return to start

            elif process == "query":  # Query section
                querying = True  # Keeping the section running until success or exit chosen
                while querying:
                    if len(cached_trades) == 0:  # Check if any trades present before moving on
                        print("No trades cached")
                        querying = False  # End while loop
                    else:  # Trades are present
                        query = input(f"\tSearch if a Bond ID is cached - with 'bond'"
                                      f"\n\tBond IDs above a specified quantity (buy and sell)  - with 'quantity'"
                                      f"\n\tTotal number of cached trades - with 'total'"
                                      f"\n\tDifference between buy and sell trades - with 'diff'"
                                      f"\n\tOr Exit - with exit"
                                      f"\nChoose a query from above: ").lower()  # Normalise with lower
                        queries = ('bond', 'quantity', 'total', 'diff', "exit")
                        if query not in queries:
                            print("\nIncorrect query")
                            continue
                        if query == "bond":  # Bond section
                            bonding = True  # Keeping bond query running until success
                            while bonding:
                                bond = input("Input a Bond_ID in the form 'BondA': ")
                                if not re.fullmatch("Bond[A-Z]+", bond):  # Check format matched
                                    print("Incorrect format\n")
                                    continue  # Due to wrong input
                                if bond not in bond_ids:  # Success due to either bond being found or not
                                    print("False\n")
                                else:
                                    print("True\n")
                                bonding = False

                        elif query == "quantity":  # Quantity section
                            quantifying = True  # Keeping bond query running until success
                            while quantifying:
                                quantity = input("Input a quantity higher than 0: ")
                                if (not re.fullmatch("[1-9][0-9]*", quantity)) or (int(quantity) <= 0):
                                    print("Incorrect quantity")  # Due to wrong format or invalid number
                                    continue  # Due to wrong input
                                count = len([quant for quant in quantities
                                             if quantity.isnumeric() and int(quant) > int(quantity)])
                                print(count)  # count being the number of trades with a higher quantity value
                                quantifying = False  # Success, end quantity query loop

                        elif query == "total":  # Total section
                            total = input("Input a direction - All or B or S: ").upper()  # enforce upper to normalise
                            if total in ("B", "S"):
                                print(f"{directions.count(total)}\n")  # return the number of buy or sell trades
                            elif total == "ALL":
                                print(f"{len(directions)}\n")
                            else:  # Fail if not B, S, or All
                                print("Incorrect input")

                        elif query == "diff":  # Difference section
                            bought = directions.count("B")  # counts only the buy trades
                            sold = len(directions) - bought  # finds sale trades
                            print(f"Number of trades Bought: {bought} and Sold: {sold}\n")
                        else:  # Exit queries
                            querying = False
            else:  # Exit program
                break
        else:  # Wrong Input
            print("Wrong input.")
        print(f"\nCurrent Cache:  {cached_trades}\n")  # Show current cached trades


if __name__ == '__main__':
    cacher()
