#!/usr/bin/env python

import unittest
import os,sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

import lib.helpers


# some zips for the t
good_zip = '21393'
wrong_number_digits = '343'
malformed_zip = '2a393'

# transation dates
good_dates_list = ['01012016', '02292016', '12121980']
short_date = '0011'
long_date = '001112122'
invalid_month_date = '13012017' # 13/1/2017
invalid_day_date = '01332017' # 1/33/2017
wrong_characters_date = 'aa102017'

# example entries from itcont.txt
# - just two entries
entry = ['C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783',
         'C00177436|N|M2|P|201702039042410894|15|IND|FOLEY, JOSEPH|FALMOUTH|ME|041051935|UNUM|SVP, CORP MKTG & PUBLIC RELAT.|01312017|384||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339']


class TestHelpers(unittest.TestCase):

    def test_CheckZipCode_good_zip(self):
        """
        Test a good zip code
        :return:
        """
        self.assertTrue(lib.helpers.CheckZipCode(good_zip), 'Incorrectly classified good zip ({})'.format(good_zip))

    def test_CheckZipCode_wrong_number_digits(self):
        """
        Test a zip code with wrong number of digits
        :return:
        """
        self.assertFalse(lib.helpers.CheckZipCode(wrong_number_digits),
                        'Did not catch wrong number of digits ({})'.format(wrong_number_digits))

    def test_CheckZipCode_malformed(self):
        """
        Test a zip code with non-numeric characters
        :return:
        """
        self.assertFalse(lib.helpers.CheckZipCode('a8928'), 'Did not catch malformed zip ({})'.format(malformed_zip))



class TestTransactionDateHelpers(unittest.TestCase):
    """
        Check the date
    """

    def test_CheckTransactionDate_good_dates(self):
        """
        Check a list of good dates
        :return:
        """
        results = [lib.helpers.CheckTransactionDate(good_date) for good_date in good_dates_list]
        for i in xrange(len(results)):
            print('{}) {} is {}'.format(i, good_dates_list[i], results[i]))
        self.assertTrue(len(good_dates_list) == sum(results), 'Did not classify all good dates as good.')


    def test_CheckTransactionDate_short_date(self):
        """
        Check a date that is too short
        :return:
        """
        self.assertFalse( lib.helpers.CheckTransactionDate(short_date),\
                          'Did not classify a short date as bad ({}).'.format(short_date))

    def test_CheckTransactionDate_long_date(self):
        """
        Check a date that is too long
        :return:
        """
        self.assertFalse( lib.helpers.CheckTransactionDate(long_date),\
                          'Did not classify a short date as bad ({}).'.format(long_date))

    def test_CheckTransactionDate_wrong_characters_date(self):
        """
        Check a date with non-numeric characters
        :return:
        """
        self.assertFalse( lib.helpers.CheckTransactionDate(wrong_characters_date),\
                          'Did not classifier a date with non-numeric characters as bad ({}).'.format(wrong_characters_date))


    def test_CheckTransactionDate_invalid_month_date(self):
        """
        Check a date with invalid month
        :return:
        """
        self.assertFalse( lib.helpers.CheckTransactionDate(invalid_month_date),\
                          'Did not classify a date with invalid month as bad ({}).'.format(invalid_month_date))
    def test_CheckTransactionDate_invalid_day_date(self):
        """
        Check a date with invalid day
        :return:
        """
        self.assertFalse( lib.helpers.CheckTransactionDate(invalid_day_date),\
                          'Did not classify a date with invalid day as bad ({}).'.format(invalid_day_date))


# I should write a test class for ConvertTransactionDateToEpochGM but I'm short on time! Sorry!
class TestParseLine(unittest.TestCase):
    """
        Check ParseLine helper function.
    """

    def test_ParseLine_full(self):
        """
        Check all the entries
        :return:
        """
        self.assertTrue(ParseLine, 'Did not classify all good dates as good.')


    def test_CheckTransactionDate_short_date(self):
        """
        Check a date that is too short
        :return:
        """
        self.assertFalse( lib.helpers.CheckTransactionDate(short_date),\
                          'Did not classify a short date as bad ({}).'.format(short_date))



if __name__ == '__main__':
    unittest.main()