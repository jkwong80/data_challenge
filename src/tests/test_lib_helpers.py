#!/usr/bin/env python

import unittest
import os, sys, time
import numpy as np

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
entries = ['C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783',
         'C00177436|N|M2|P|201702039042410894|15|IND|FOLEY, JOSEPH|FALMOUTH|ME|041051935|UNUM|SVP, CORP MKTG & PUBLIC RELAT.|01312017|384||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339']

expected_parsed_values = []
expected_parsed_values.append(('C00629618', '90017', '01032017', '40', 'H6CA34245'))
expected_parsed_values.append( ('C00177436', '041051935', '01312017', '384', ''))


class TestZipCodeHelpers(unittest.TestCase):
    """
    Test the CheckZipCode zip code checking function.

    """

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
        Check the CheckTransactionDate function which determines if a MMDDYYYY date string is valid.
    """


    def test_CheckTransactionDate_good_dates(self):
        """
        Check a list of good dates
        :return:
        """
        print('Testing CheckTransactionDate')

        results = [lib.helpers.CheckTransactionDate(good_date) for good_date in good_dates_list]
        for i in xrange(len(results)):
            print('{}) {} is {}'.format(i, good_dates_list[i], results[i]))
        self.assertTrue(len(good_dates_list) == sum(results), 'Did not classify all good dates as good.')


    def test_CheckTransactionDate_short_date(self):
        """
        Check a date that is too short
        :return:
        """
        print('Testing CheckTransactionDate')

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
        See if examples are being parsed properly
        :return:
        """

        print('Testing ParseLine')

        results = [lib.helpers.ParseLine(entries[i]) == expected_parsed_values[i] for i in xrange(len(entries))]

        for i in xrange(len(results)):
            print('{}) {} parsed propely: {}'.format(i, entries[i], results[i]))
        self.assertTrue(len(entries) == sum(results), 'Did not properly parse all the entries.')


class TestMedianStreaming(unittest.TestCase):
    """
        Check MedianStreaming class.

    """


    def test_MedianStreaming_check_heaps(self):
        """
        Test to make sure that MedianStreaming is creating the left (max heap) and right (min heap) properly

        :return: Nothing
        """

        print('Testing MedianStreaming heap sizes')

        NUMBER_VALUES = 10
        integers_list = np.arange(NUMBER_VALUES)

        running_medians = np.zeros(NUMBER_VALUES)

        median_streaming = lib.helpers.MedianStreaming()

        for i in xrange(len(integers_list)):
            running_medians[i] = median_streaming.ingest(integers_list[i])

        self.assertTrue(len(median_streaming.left_heap) == 5, 'Left heap size is wrong')
        self.assertTrue(len(median_streaming.right_heap) == 5, 'Right heap size is wrong')
        self.assertEqual(median_streaming.left_heap, [-4, -3, -1, 0, -2], 'Left heap is wrong')
        self.assertEqual(median_streaming.right_heap, [5, 6, 8, 7, 9], 'Right heap is wrong')


    def test_MedianStreaming_test_reset(self):
        """
        Test to make sure that MedianStreaming is creating the left (max heap) and right (min heap) properly

        :return: Nothing
        """

        print('Testing MedianStreaming reset method')

        NUMBER_VALUES = 10
        integers_list = np.arange(NUMBER_VALUES)

        running_medians = np.zeros(NUMBER_VALUES)

        median_streaming = lib.helpers.MedianStreaming()

        for i in xrange(len(integers_list)):
            running_medians[i] = median_streaming.ingest(integers_list[i])

        # reset the values
        median_streaming.reset()

        self.assertTrue(median_streaming.left_heap == [], 'Left heap is not empty after reset.')
        self.assertTrue(median_streaming.right_heap == [], 'Right heap is not empty after reset.')
        self.assertTrue(median_streaming.median_current == 0, 'Left heap is not empty after reset.')

    def test_MedianStreaming_injest(self):
        """
        Calculate the median values for a stream of values using an instance of the MedianStreaming class and compare it
        with a brute force method using numpy

        :return: Nothing
        """

        print('Testing MedianStreaming ingest method')

        NUMBER_VALUES = 1000
        random_integers_list = np.random.randint(0, 1000, NUMBER_VALUES)

        # store the running_medians and run times
        running_medians = {}
        run_times = {}
        for algo_name in ['no_heaps', 'with_heaps']:
            running_medians[algo_name] = np.zeros(NUMBER_VALUES)
            run_times[algo_name] = np.zeros(NUMBER_VALUES)

        # no heaps
        algo_name = 'no_heaps'
        # this hold list of random integers at each step
        current_list_of_values = []
        t_start = time.time()
        for i in xrange(NUMBER_VALUES):
            # add a value to the list
            current_list_of_values.append(random_integers_list[i])
            running_medians[algo_name][i] = np.median(current_list_of_values)
            run_times[algo_name][i] = time.time()
        run_times[algo_name] = run_times[algo_name] - run_times[algo_name][0]
        print('Time Elapsed: %3.3f' %(time.time() - t_start))

        # with class that uses heaps
        algo_name = 'with_heaps'
        median_streaming = lib.helpers.MedianStreaming()
        t_start = time.time()

        for i in xrange(NUMBER_VALUES):
            running_medians[algo_name][i] = median_streaming.ingest(random_integers_list[i])
            run_times[algo_name][i] = time.time()
        print('Time Elapsed: %3.3f' %(time.time() - t_start))

        run_times[algo_name] = run_times[algo_name] - run_times[algo_name][0]
        print('Are the running median values equal?: {}'.format(np.all(running_medians['no_heaps'] == running_medians['with_heaps'])))
        self.assertTrue(np.all(running_medians['no_heaps'] == running_medians['with_heaps']), 'The median values are not equal')


class TestZipStreaming(unittest.TestCase):
    """
        Check ZipStreaming class.

    """

    def test_ZipStreaming_ingest(self):
        """
        Check that the median, total, and count values from the ZipStreaming ingest function works as should.  The results
        are compared with a brute force method using numpy functions.  Also check the GetCount and GetTotal methods.

        :return:
        """

        print('Testing ZipStreaming ingest method')

        NUMBER_VALUES = 1000
        random_integers_list = np.random.randint(0, 1000, NUMBER_VALUES)

        # store the running_medians and run times
        running_medians = {}
        running_total = {}
        running_count = {}

        run_times = {}
        for algo_name in ['no_heaps', 'with_heaps']:
            running_medians[algo_name] = np.zeros(NUMBER_VALUES)
            running_total[algo_name] = np.zeros(NUMBER_VALUES)
            running_count[algo_name] = np.zeros(NUMBER_VALUES, dtype = np.int64)

            run_times[algo_name] = np.zeros(NUMBER_VALUES)

        # no heaps
        algo_name = 'no_heaps'
        # this hold list of random integers at each step
        current_list_of_values = []
        t_start = time.time()
        for i in xrange(NUMBER_VALUES):
            # add a value to the list
            current_list_of_values.append(random_integers_list[i])
            running_medians[algo_name][i] = np.median(current_list_of_values)
            running_total[algo_name][i] = np.sum(current_list_of_values)
            running_count[algo_name][i] = len(current_list_of_values)

            run_times[algo_name][i] = time.time()
        run_times[algo_name] = run_times[algo_name] - run_times[algo_name][0]
        print('Time Elapsed: %3.3f' %(time.time() - t_start))

        # with class that uses heaps
        algo_name = 'with_heaps'
        zip_streaming = lib.helpers.ZipStreaming()
        t_start = time.time()

        for i in xrange(NUMBER_VALUES):
            running_medians[algo_name][i], running_total[algo_name][i], running_count[algo_name][i] = \
                zip_streaming.ingest(random_integers_list[i])
            run_times[algo_name][i] = time.time()
        print('Time Elapsed: %3.3f' %(time.time() - t_start))

        run_times[algo_name] = run_times[algo_name] - run_times[algo_name][0]

        # print(running_medians[algo_name][-10:])
        # print(running_total[algo_name][-10:])
        # print(running_count[algo_name][-10:])

        print('Are the running median values equal?: {}'.format(np.all(running_medians['no_heaps'] == running_medians['with_heaps'])))
        print('Are the running total values equal?: {}'.format(np.all(running_total['no_heaps'] == running_total['with_heaps'])))
        print('Are the running count values equal?: {}'.format(np.all(running_count['no_heaps'] == running_count['with_heaps'])))


        self.assertTrue(np.all(running_medians['no_heaps'] == running_medians['with_heaps']), 'The median values are not equal')
        self.assertTrue(np.all(running_total['no_heaps'] == running_total['with_heaps']), 'The total values are not equal')
        self.assertTrue(np.all(running_count['no_heaps'] == running_count['with_heaps']), 'The count values are not equal')
        self.assertTrue(np.all(zip_streaming.GetCount() == running_count['with_heaps'][-1]), 'The GetCount() value is wrong')
        self.assertTrue(np.all(zip_streaming.GetTotal() == running_total['with_heaps'][-1]), 'The GetTotal() value is wrong')



if __name__ == '__main__':
    unittest.main()