"""
    First version.

    No attempt yet to do anything smart about the running median calculation.

"""
import sys
import time

import numpy as np

import helpers


def main(input_fullfilename, zip_fullfilename, date_fullfilename):

    DISPLAY_INTERVAL = 100000

    # create data structures for storing values for the zip and date files
    dat_zip = {}
    dat_date = {}

    # create data structures for benchmarking
    benchmarking_line_number = []
    benchmarking_time = []
    benchmarking_skipped_zip = 0
    benchmarking_skipped_date = 0

    # This this structure to prevent lingering opened files if something should fail
    # at the wrong/right spot

    line_number = 0
    t_start = time.time()
    with open(input_fullfilename, 'rb') as fid:

        # Open once to save time
        with open(zip_fullfilename, 'wb') as fid_zip:

            for lineIn in fid:
                # lineIn = fid.readline()
                entry = helpers.ParseLine(lineIn)
                process_mask = helpers.CheckEntry(entry)

                if line_number % DISPLAY_INTERVAL == 0:
                    report_index = line_number / DISPLAY_INTERVAL
                    benchmarking_line_number.append(line_number)
                    benchmarking_time.append(time.time())


                    if report_index > 0:
                        t_diff = benchmarking_time[report_index] - benchmarking_time[report_index-1]
                        print('Line {}, time elapsed: {}, time since last report: {}, rate: {} Hz'.format(line_number, \
                                benchmarking_time[report_index] - t_start, t_diff, DISPLAY_INTERVAL/t_diff))
                    else:
                        print('Line {}, time elapsed: {}'.format(line_number, \
                                benchmarking_time[report_index] - t_start))

                line_number += 1

                # getting some values out just so that the code is easier to read
                id = entry['CMTE_ID']
                # Only consider the first five digits
                zip = entry['ZIP_CODE'][:5]
                dt = entry['TRANSACTION_DT']
                # print(entry)

                # check if we can process for zip file
                if process_mask[0]:
                    # see if encountering this id for the first time
                    if id not in dat_zip:
                        dat_zip[id] = {}

                    # See if this is the first time encountering this zip, for this id
                    if zip not in dat_zip[id]:
                        dat_zip[id][zip] = []

                    # now we are ready to the transaction amount to the list
                    # ??float or int
                    # dat_zip[id][zip].append(float(entry['TRANSACTION_AMT']))
                    dat_zip[id][zip].append(int(entry['TRANSACTION_AMT']))

                    # Calculate the median
                    # (This is the function I would modify (along the data structures) if I wanted to
                    # use faster running median calculators)
                    trans_median, trans_total, trans_number = helpers.CalculateTransactionValues(dat_zip[id][zip])

                    lineOut = helpers.CreateZipOutputString(trans_median, trans_total, trans_number, entry)
                    # print(lineOut)
                    fid_zip.write(lineOut)
                else:
                    benchmarking_skipped_zip += 1

                # Check to see if we can process for the date file
                if process_mask[1]:
                    # see if encountering this id for the first time
                    if id not in dat_date:
                        dat_date[id] = {}

                    # See if this is the first time encountering this zip, for this id
                    if dt not in dat_date[id]:
                        dat_date[id][dt] = []

                    # now we are ready to the transaction amount to the list
                    # dat_date[id][dt].append(float(entry['TRANSACTION_AMT']))
                    dat_date[id][dt].append(int(entry['TRANSACTION_AMT']))
                else:
                    benchmarking_skipped_date += 1

    print('zip file - number of entries skipped: {}'.format(benchmarking_skipped_zip))
    print('date file - number of entries skipped: {}'.format(benchmarking_skipped_date))

    # print(dat_zip)

    with open(date_fullfilename, 'wb') as fid_dt:

        # write in order of id and then by date
        id_list = dat_date.keys()

        id_list.sort()

        for id_write_index, id_write in enumerate(id_list):
            # get all the dates and sort them
            date_list = dat_date[id_write].keys()

            # Convert to epoch times
            epoch_list = [helpers.ConvertTransactionDateToEpochGM(dtt) for dtt in date_list]
            date_list_arg_sort  = np.argsort(epoch_list)

            for index_ordered in date_list_arg_sort:

                date_str = date_list[index_ordered]
                # calculate the median, total, # values
                trans_median, trans_total, trans_number = \
                    helpers.CalculateTransactionValues(dat_date[id_write][date_str])

                lineOut = helpers.CreateDateOutputString(id_write, date_str, trans_median, trans_total, trans_number)
                # print(lineOut)
                fid_dt.write(lineOut)

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Missing arguments.')
        exit
    input_fullfilename = sys.argv[1]
    zip_fullfilename = sys.argv[2]
    date_fullfilename = sys.argv[3]

    main(input_fullfilename, zip_fullfilename, date_fullfilename)