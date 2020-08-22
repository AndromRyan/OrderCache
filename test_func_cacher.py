import unittest
import func_chache as fc
from unittest.mock import patch


class TestTwCache(unittest.TestCase):
    def test_trade(self):
        # Input new order
        self.assertEqual(fc._trade("ID1 BondD B 10000", [], []),
                         ("Order cached: ID1 BondD B 10000", False, ["ID1 BondD B 10000"]))
        # Input new order
        self.assertEqual(fc._trade("ID2 BondD B 10000", ["ID1"], ["ID1 BondD B 10000"]),
                         ("Order cached: ID2 BondD B 10000", False, ["ID1 BondD B 10000", "ID2 BondD B 10000"]))
        # Input same ID as previous
        self.assertEqual(fc._trade("ID1 BondD B 10000", ["ID1", "ID2"], ["ID1 BondD B 10000", "ID2 BondD B 10000"]),
                         ("Order ID already present!", True, ["ID1 BondD B 10000", "ID2 BondD B 10000"]))
        # Input order with wrong structure
        self.assertEqual(fc._trade("id Bondc b $10000", ["ID1", "ID2"], ["ID1 BondD B 10000", "ID2 BondD B 10000"]),
                         ("Incorrect trade format", True, ["ID1 BondD B 10000", "ID2 BondD B 10000"]))
        # Input order with 'B'
        self.assertEqual(fc._trade("ID3 BondA 'B' 10000", ["ID1", "ID2"], ["ID1 BondD B 10000", "ID2 BondD B 10000"]),
                         ("Order cached: ID3 BondA 'B' 10000", False,
                          ["ID1 BondD B 10000", "ID2 BondD B 10000", "ID3 BondA 'B' 10000"]))

    def test_cancel(self):
        # Cancel valid id
        self.assertEqual(fc._cancel("ID1", ["ID1", "ID2", "ID3"],
                                    ["ID1 BondD B 10000", "ID2 BondD B 10000", "ID3 BondA 'B' 10000"]),
                         ("\nCache canceled", False, ["ID2 BondD B 10000", "ID3 BondA 'B' 10000"]))
        # Cancel invalid id
        self.assertEqual(fc._cancel("ID4", ["ID2", "ID3"],
                                    ["ID2 BondD B 10000", "ID3 BondA 'B' 10000"]),
                         ("\nTrade not cached", True, ["ID2 BondD B 10000", "ID3 BondA 'B' 10000"]))
        # Incorrect cancel id format
        self.assertEqual(fc._cancel("id 1", ["ID1", "ID2", "ID3"],
                                    ["ID1 BondD B 10000", "ID2 BondD B 10000", "ID3 BondA 'B' 10000"]),
                         ("\nIncorrect cancel format", True,
                          ["ID1 BondD B 10000", "ID2 BondD B 10000", "ID3 BondA 'B' 10000"]))
        # Cancel invalid id format
        self.assertEqual(fc._cancel("id1", ["ID1", "ID2", "ID3"],
                                    ["ID1 BondD B 10000", "ID2 BondD B 10000", "ID3 BondA 'B' 10000"]),
                         ("\nIncorrect cancel format", True,
                          ["ID1 BondD B 10000", "ID2 BondD B 10000", "ID3 BondA 'B' 10000"]))
        # Cancel invalid id - no cache. Function works but doesnt get to this point in algo, due to previous checks
        self.assertEqual(fc._cancel("ID4", [], []),
                         ("\nTrade not cached", True, []))

    def test_bond(self):
        # Search if a bond is in the cache
        self.assertEqual(fc.bond_q("BondA", ["BondA", "BondA", "BondB"]), ("True", False))
        # Search if a bond is in the cache
        self.assertEqual(fc.bond_q("BondB", ["BondA", "BondA", "BondB"]), ("True", False))
        # Search if a bond is in the cache, but bond is invalid
        self.assertEqual(fc.bond_q("BondC", ["BondA", "BondA", "BondB"]), ("False", False))
        # Search if a bond is in the cache, but format of bond_id is invalid
        self.assertEqual(fc.bond_q("bondb", ["BondA", "BondA", "BondB"]), ("Incorrect format\n", True))
        # Search if a bond is in the cache, but format of bond_id is invalid
        self.assertEqual(fc.bond_q("dsbjfsj", ["BondA", "BondA", "BondB"]), ("Incorrect format\n", True))
        # Search if a bond is in the cache, but format of bond_id is invalid
        self.assertEqual(fc.bond_q("1hj2jv", ["BondA", "BondA", "BondB"]), ("Incorrect format\n", True))

    def test_quantity(self):
        # search for negative value
        self.assertEqual(fc.quantity_q("-1", ["1000", "500", "2000"]), ("Incorrect quantity", True))
        # search for alpha value
        self.assertEqual(fc.quantity_q("sfbsdh", ["1000", "500", "2000"]), ("Incorrect quantity", True))
        # search for 0
        self.assertEqual(fc.quantity_q("0", ["1000", "500", "2000"]), ("Incorrect quantity", True))
        # search for a value resulting in 2
        self.assertEqual(fc.quantity_q("501", ["1000", "500", "2000"]), (2, False))
        # search for a value resulting in 3
        self.assertEqual(fc.quantity_q("1", ["1000", "500", "2000"]), (3, False))
        # search for a value resulting in 1
        self.assertEqual(fc.quantity_q("1001", ["1000", "500", "2000"]), (1, False))
        # search for a value greater than highest known value
        self.assertEqual(fc.quantity_q("2001", ["1000", "500", "2000"]), (0, False))

    def test_total(self):
        # User input is forced to upper in algo before reaching function, only test caps
        # check for total buy trades in caps
        self.assertEqual(fc.total_q("B", ["B", "S", "B", "B", "B", "S"]), "4")
        # check for total sale trades in caps
        self.assertEqual(fc.total_q("S", ["B", "S", "B", "B", "B", "S"]), "2")
        # check for total trades in caps
        self.assertEqual(fc.total_q("ALL", ["B", "S", "B", "B", "B", "S"]), "6")
        # errors on non specifed arguments
        self.assertEqual(fc.total_q("DHBVDD", ["B", "S", "B", "B", "B", "S"]), "Incorrect input")
        # all is valid but space errors
        self.assertEqual(fc.total_q("ALL ", ["B", "S", "B", "B", "B", "S"]), "Incorrect input")
        # b is valid but space error
        self.assertEqual(fc.total_q("B ", ["B", "S", "B", "B", "B", "S"]), "Incorrect input")

    def test_diff(self):
        # Cancel invalid id format
        self.assertEqual(fc.diff_q(['B']), "Number of trades Bought: 1 and Sold: 0\n")
        # Cancel invalid id format
        self.assertEqual(fc.diff_q(["B", "B", "B", "B", "B", "B"]), "Number of trades Bought: 6 and Sold: 0\n")
        # Cancel invalid id format
        self.assertEqual(fc.diff_q(["S", "S", "S", "B"]), "Number of trades Bought: 1 and Sold: 3\n")

    def test_query(self):
        # Tests the query function, require inputs to be mocked up before. Due to the flow of the code,
        # each prints result in terminal. ALl output the same, as it keeps the while loop going except for exit
        queries = ('bond', 'quantity', 'total', 'diff', "exit")
        with patch('builtins.input', return_value='BondD'):  # Test bond
            self.assertEqual(fc._query('bond', queries, ['BondD'], ['10000'], ['B']), ('', True))
        with patch('builtins.input', return_value='BondA'):  # Test bond
            self.assertEqual(fc._query('bond', queries, ['BondD'], ['10000'], ['B']), ('', True))
        with patch('builtins.input', return_value='100'):  # Test quantity
            self.assertEqual(fc._query('quantity', queries, ['BondD'], ['10000'], ['B']), ('', True))
        with patch('builtins.input', return_value='10001'):  # Test quantity
            self.assertEqual(fc._query('quantity', queries, ['BondD'], ['10000'], ['B']), ('', True))
        with patch('builtins.input', return_value='B'):  # Test total
            self.assertEqual(fc._query('total', queries, ['BondD'], ['10000'], ['B']), ('', True))
        with patch('builtins.input', return_value='S'):  # Test total
            self.assertEqual(fc._query('total', queries, ['BondD'], ['10000'], ['B']), ('', True))
        self.assertEqual(fc._query('diff', queries, ['BondD'], ['10000'], ['B']), ('', True))  # Test difference
        self.assertEqual(fc._query('exit', queries, ['BondD'], ['10000'], ['B']), ('', False))  # Test exit

    def test_cacher(self):
        # Other tests carried out before, test of exit required
        with patch('builtins.input', return_value='exit'):  # Test exit
            self.assertEqual(fc.cacher(), None)


if __name__ == '__main__':
    unittest.main()
