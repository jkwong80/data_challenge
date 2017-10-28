"""
Various helper functions and classes for parsing and checking values, creating output strings and for calculating
the running median.

Note that this this file was originally in /src/lib but has been moved as I was uncertain about whether or not
subdirectories were allowed for the /src folder

"""

import time, heapq
from calendar import timegm
import numpy as np

class MedianStreaming(object):
    """
        Class for calculate median of a stream of incoming values, ingested one at a time.
        Note that this is not for calculating the median of a finite window size of streaming
        values.
        How to use: ingest a value and it returns the new median value.

        10/27/2017, John Kwong

    """

    def __init__(self):
        self.left_heap = []
        self.right_heap = []
        self.median_current = 0

    def ingest(self, input):
        """
        This method is for taking in another value and returning a new median value.

        :param input: streaming number [number]
        :return:  the new median value [number]
        """
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
        """
        This method clears all the fields so that you can reuse your instance for a new set of streaming values.

        :return: Nothing
        """
        self.left_heap = []
        self.right_heap = []
        self.median_current = 0


class ZipStreaming(MedianStreaming):
    """
        Class specifically for generating the median, total contributions and number of contributions for
        streaming contribution values.

        This class inherits from MedianStreaming.

    """
    def __init__(self):
        MedianStreaming.__init__(self)
        self.total = 0
        self.count = 0

    def ingest(self, input):
        """
        The contribution values are ingested with this method and the new median, total and number of contributions are
        returned.

        :param input:  the contribution value [number]
        :return:  tuple of current median, total contributions, number of contributions [number, number, number]
        """
        MedianStreaming.ingest(self,input)
        self.total += input
        self.count += 1
        return self.median_current, self.total, self.count

    def GetTotal(self):
        """
        Get the total contributions.

        :return:   total contributions (sum)
        """
        return(self.total)

    def GetCount(self):
        """
        Get the number of contributions

        :return:   number of contributions
        """
        return(self.count)





def CheckZipCode(zipcode):
    """
    This function checks to see if the zip code string is valid by seeing if it has at least 5 digits.
    If any of the characters are not numbers, it will be classified as bad.

    :param zipcode:  the zip code [string]
    :return:  zip code valid [bool]
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

    :param trans_dt:  transaction date [string]
    :return:  transaction date valid [bool]
    """
    return ConvertTransactionDateToEpochGM(trans_dt) > 0

def ConvertTransactionDateToEpochGM(date_input):
    """
    Converts the MMDDYYY string to GM epoch time.
    If the input is invalid (e.g. string too short, doesn't have all numbers), then it will return -1
    This will also flag invalid dates like '02292017' (invalid leap year), '13012017' (invalid month) as bad.

    :param date_input:  transaction date [string]
    :return:  the epoch in GM; returns -1 if the transaction date is invalid [int]
    """
    try:
        temp = timegm(time.strptime(date_input, '%m%d%Y'))
        return temp
    except:
        return -1

def ParseLine(line_in):
    """
    This function parses a line from the itcont.txt file and returns a tuple containing the following columns:
    'CMTE_ID', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID'

    See this website for expected line format:
    http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml

    I originally used a function that would parse the whole line into a dictionary containing all the values but this
    was abandoned as this was much slower and unnecessary.


    :param line_in: a line from the contributions file [string]
    :return:  tuple containing 'CMTE_ID', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID'
    """
    line_in_split = line_in.split('|')
    return line_in_split[0], line_in_split[10], line_in_split[13], line_in_split[14], line_in_split[15]


def ParseLineOLD(line_in, return_subset = True):
    """
        Parse the entry and return a dictionary.
        Has option of returning all the fields.

        - I'm not using this any more because it's slow.

    :param line_in:  line from the contributions file [strng]
    :param return_subset:  whether or not to return only the subset of fields needed for this task[bool]
    :return: dictionary of the values [dict]
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
    - Not used by main script anymore - it's been left here in case someone wants to run the older find_political_donors_XX.py scripts

    This function accepts and entry dictionary generated by ParseLineOLD and determines how we should process the it.
    This function has been ABANDONED and its logic has been directly embedded in find_political_donors_delta.py to speed
    things up.

    :param entry: a parsed entry [dict]
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
        Calculates the median, sum and count of the transactions give a list of such values

    :param values: transaction values [list]
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
    Create an output line for the medianvals_by_date.txt file

    :param id_write: id [string]
    :param dt:  date of the transaction [string]
    :param trans_median:  median of transactions [int]
    :param trans_total:  total of transactions [int]
    :param trans_number: number of transactions [int]
    :return:  an output line for the medianvals_by_date.txt file [string]
    """

    return( '%s|%s|%d|%d|%d\n' %(id_write, date_str, round(trans_median), trans_number, trans_total))

