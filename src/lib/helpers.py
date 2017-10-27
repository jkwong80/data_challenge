import os, sys
import datetime, time
from calendar import timegm

import numpy as np

import heapq

def CheckZipCode(zipcode):
    """
    This function checks to see if the zip code string is valid by seeing if it has at least 5 digits.
    If any of the characters are not numbers, it will be classified as bad.

    :param zipcode:
    :return:
    """
    # see if there are enough digits
    if (len(zipcode) >= 5):
        # check if numerical
        try:
            int(zipcode)
            return True
        except:
            return False
    else:
        return False

def CheckTransactionDate(trans_dt):
    """
        Returns a boolean indicating whether the MMDDYYYY string is a valid date.
        It uses ConvertTransactionDateToEpochGM to check if can convert to epoch time (GM).

    :param trans_dt:
    :return:
    """
    return ConvertTransactionDateToEpochGM(trans_dt) > 0

def ConvertTransactionDateToEpochGM(date_input):
    """
        Converts the MMDDYYY string to GM epoch time.
        If the input is invalid (e.g. string too short, doesn't have all numbers), then it will return -1
        This will also flag invalid dates like '02292017' (invalid leap year), '13012017' (invalid month) as bad.

    :param date_input:
    :return:
    """
    try:
        temp = timegm(time.strptime(date_input, '%m%d%Y'))
        return temp
    except:
        return -1

def ParseLine(line_in, return_subset = True):
    """

    :param line_in:
    :param return_subset:
    :return:
    """
    line_in_split = line_in.split('|')
    return line_in_split[0], line_in_split[10], line_in_split[13], line_in_split[14], line_in_split[15]


def ParseLineOLD(line_in, return_subset = True):
    """
        Parse the entry and return a dictionary.
        Has option of returning all the fields.

        - I'm not using this any more because slow

    :param line_in:
    :param return_subset:
    :return:
    """
    # names of all the columns
    column_names = ['CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', 'TRANSACTION_TP', 'ENTITY_TP', 'NAME',\
                    'CITY', 'STATE', 'ZIP_CODE', 'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID',\
                    'TRAN_ID', 'FILE_NUM', 'MEMO_CD', 'MEMO_TEXT', 'SUB_ID']

    # subset of columns that are relevant to us
    column_names_subset = ['CMTE_ID', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID']

    line_in_split = line_in.split('|')
    if return_subset:
        entry = {column_names[i]:line_in_split[i] for i in xrange(len(column_names)) if column_names[i] in column_names_subset}
    else:
        entry = {column_names[i]:line_in_split[i] for i in xrange(len(column_names))}
    return entry



def CheckEntry(entry):
    """

    :param entry:
    :return:
    """
    # process for _zip, process _date
    process_mask = [False, False]


    # Considerations #1 and 5
    # - We could this split this so that we can acquire some statistics on entry rejections
    if (entry['OTHER_ID'] != '') or (entry['CMTE_ID'] == '') or (entry['TRANSACTION_AMT'] == ''):
        return process_mask

    # see if the zip code is valid
    process_mask[0] = CheckZipCode(entry['ZIP_CODE'])

    # check the TRANSACTION_AMT
    process_mask[1] = CheckTransactionDate(entry['TRANSACTION_DT'])

    return process_mask





def CalculateTransactionValues(values):
    """
        Calculate the
    :param values: the list of transaction values
    :return:
        tuple of the following
            median of transactions
            total amount of the transactions
            number of transactions
    """
    return np.median(values), sum(values), len(values)


def CreateZipOutputString(trans_median, trans_total, trans_number, id, zipcode):
    """
        Takes a couple inputs to build the string to be written to the _zip.txt file.

    :param trans_median:  The median value of transactions
    :param trans_total:  The total value of all transactions
    :param trans_number:  Number of transactions
    :param id:   CMTE_ID, the id
    :param zipcode: ZIP_CODE but only first 5 characters
    :return:
    """
    return( '%s|%s|%d|%d|%d\n' %(id, zipcode, round(trans_median), trans_number, trans_total))

def CreateDateOutputString(id_write, date_str, trans_median, trans_total, trans_number):
    """

    :param id_write:
    :param dt:
    :param trans_median:
    :param trans_total:
    :param trans_number:
    :return:
    """

    return( '%s|%s|%d|%d|%d\n' %(id_write, date_str, round(trans_median), trans_number, trans_total))


class MedianStreaming(object):
    """
        Class for calculate median of a stream of incoming values, injested one at a time.
        Note that this is not for calculating the median of a finite window size of streaming
        values.
        This is very simple to use.  You just injest a value and it returns the new median value.

    """

    def __init__(self):
        self.left_heap = []
        self.right_heap = []
        self.median_current = 0

    def ingest(self, input):
        if len(self.left_heap) > len(self.right_heap):
            if input < self.median_current:
                # heapq.heappush(self.right_heap, self.left_heap.pop(-1))
                heapq.heappush(self.right_heap, -heapq.heappop(self.left_heap))

                heapq.heappush(self.left_heap, -input)
            else:
                heapq.heappush(self.right_heap, input)

            # the average
            self.median_current = float(-heapq.nsmallest(1, self.left_heap)[0] + heapq.nsmallest(1, self.right_heap)[0]) / 2.0

        # they are equal
        elif len(self.left_heap) == len(self.right_heap):
            if input < self.median_current:
                heapq.heappush(self.left_heap, -input)
                self.median_current = -heapq.nsmallest(1, self.left_heap)[0]
            else:
                heapq.heappush(self.right_heap, input)
                self.median_current = heapq.nsmallest(1, self.right_heap)[0]

        else:  # len(self.left_heap) < len(self.right_heap):
            if input > self.median_current:
                heapq.heappush(self.left_heap, -heapq.heappop(self.right_heap))
                heapq.heappush(self.right_heap, input)
            else:
                heapq.heappush(self.left_heap, -input)
            # the average
            self.median_current = float(-heapq.nsmallest(1, self.left_heap)[0] + heapq.nsmallest(1, self.right_heap)[0]) / 2.0

        return(self.median_current)

    def reset(self):
        self.self.left_heap = []
        self.self.right_heap = []
        self.self.median_current = 0
        self.median_new = None



class ZipStreaming(MedianStreaming):
    def __init__(self):

        MedianStreaming.__init__(self)
        self.total = 0
        self.count = 0

    def ingest(self, input):
        MedianStreaming.ingest(self,input)
        self.total += input
        self.count += 1
        return self.median_current, self.total, self.count

    def GetTotal(self):
        return(self.total)

    def GetCount(self):
        return(self.count)


