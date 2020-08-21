import re


def cache():
    cached_trades = []
    caching = True
    while caching:
        process = input("Would you like to trade, cancel, query or exit: ").lower()
        processes = ["trade", "cancel", "query", "exit"]

        cache_ids = []
        bond_ids = []
        directions = []
        quantities = []
        for _cache in cached_trades:
            cache_split = _cache.split(" ")
            cache_ids.append(cache_split[0])
            bond_ids.append(cache_split[1])
            directions.append(cache_split[2])
            quantities.append(cache_split[3])

        if process in processes:

            # Adding section
            if process == "trade":
                trading = True
                while trading:
                    trade = input("Please insert a trade, in the form 'ID1 BondD B 10000': ")
                    if re.fullmatch("ID([0-9])+ Bond[A-Z] '*(B|S)'* [1-9][0-9]*", trade):
                        trade_id = trade.split(" ")[0]
                        if trade_id not in cache_ids:
                            cached_trades.append(trade)
                            print(f"Order cached: {trade}")
                            trading = False
                        else:
                            print("Order ID already present!")
                    else:
                        print("Incorrect trade format")

            # Cancel section
            elif process == "cancel":
                canceling = True
                while canceling:
                    if len(cached_trades) == 0:
                        print("No trades cached")
                        canceling = False
                    else:
                        cancel_id = input(f"Please select an Order_ID from the following: "
                                          f"\n {cached_trades} \n In the form 'ID1: ")
                        if re.fullmatch("ID([0-9])+", cancel_id):
                            if cancel_id in cache_ids:
                                canceling = False
                                for _cache in cached_trades:
                                    if cancel_id in _cache:
                                        cached_trades.remove(_cache)
                                        print("Cache canceled")
                                    else:
                                        print("Test")
                            else:
                                print("\nTrade not cached")
                        else:
                            print("\nIncorrect cancel format")

            # Query section
            elif process == "query":
                querying = True
                while querying:
                    if len(cached_trades) == 0:
                        print("No trades cached")
                        querying = False
                    else:
                        query = input(
                                      f"\tSearch if a Bond ID is cached - with 'bond'"
                                      f"\n\tBond IDs above a specified quantity (buy and sell)  - with 'quantity'"
                                      f"\n\tTotal number of cached trades - with 'total'"
                                      f"\n\tDifference between buy and sell trades - with 'diff'"
                                      f"\n\tOr Exit - with exit"
                                      f"\nChoose a query from above: ")
                        queries = ['bond', 'quantity', 'total', 'diff', "exit"]
                        if query in queries:

                            # Bond section
                            if query == "bond":
                                bonding = True
                                while bonding:
                                    bond = input("Input a Bond_ID in the form 'BondA': ")
                                    if re.fullmatch("Bond[A-Z]", bond):
                                        if bond in bond_ids:
                                            print("True\n")
                                        else:
                                            print("False\n")
                                        bonding = False
                                    else:
                                        print("Incorrect format\n")

                            # Quantity section
                            elif query == "quantity":
                                quantity = input("Input a quantity higher than 0")
                                if quantity.isnumeric():
                                    print(quantity)
                                else:
                                    print("Incorrect quantity")

                            # Total section
                            elif query == "total":
                                total = input("Input a direction either All or B or S: ").upper()
                                if total in ("B", "S"):
                                    print(f"{directions.count(total)}\n")
                                elif total == "ALL":
                                    print(f"{len(directions)}\n")
                                else:
                                    print("Incorrect input")

                            # Difference section
                            elif query == "diff":
                                bought = directions.count("B")
                                sold = len(cached_trades) - bought
                                print(f"Number of trades Bought: {bought} and Sold: {sold}\n")
                            else:
                                print("Exiting queries")
                                querying = False
                        else:
                            print("\nIncorrect query")
            else:
                print("Exit")
                caching = False
        else:
            print("Wrong input.")
        print(f"\nCurrent Cache:  {cached_trades}\n")


cache()
