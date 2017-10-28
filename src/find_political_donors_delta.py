"""

    This processes itcont.txt file and generates the medianvals_by_date.txt and medianvals_by_zip.txt files.

    This is third version of my script.
    - Uses a running median calculator that uses min heaps.
    - speeding up parsing

"""
import sys, time
import numpy as np

# import my helpers
import helpers

line_number_display = 50000000000

def main(input_fullfilename, zip_fullfilename, date_fullfilename):

    # A report in the terminal at this interval.
    DISPLAY_INTERVAL = 100000

    # create data structures for storing values for the zip and date files
    dat_zip = {}
    dat_date = {}

    # create data structures for benchmarking
    benchmarking_line_number = []
    benchmarking_time = []
    benchmarking_skipped_zip = 0
    benchmarking_skipped_date = 0

    line_number = 0
    t_start = time.time()

    # This this structure to prevent lingering opened files if something should fail
    # at the wrong/right spot
    with open(input_fullfilename, 'rb') as fid:

        # Open once to save time
        with open(zip_fullfilename, 'wb') as fid_zip:

            # Iterate over input lines ("stream the data in")
            for lineIn in fid:

                # Display progress report
                if line_number % DISPLAY_INTERVAL == 0:
                    report_index = line_number / DISPLAY_INTERVAL
                    benchmarking_line_number.append(line_number)
                    benchmarking_time.append(time.time())

                    if report_index > 0:
                        t_diff = benchmarking_time[report_index] - benchmarking_time[report_index-1]
                        print('Line %d, time elapsed: %3.3f, time since last report: %3.3f, rate: %3.3f Hz' %(line_number, \
                                benchmarking_time[report_index] - t_start, t_diff, DISPLAY_INTERVAL/t_diff))

                # Parse the input line to id, zip code, date, amount and other id
                id,zipcode,dt,amt,other_id = helpers.ParseLine(lineIn)

                # we don't need the full zip code
                zipcode = zipcode[:5]

                # Considerations #1 and 5
                # - We could this split this so that we can acquire some statistics on entry rejections
                if (other_id != '') or (id == '') or (amt == ''):
                    line_number += 1
                    benchmarking_skipped_zip += 1
                    benchmarking_skipped_date += 1
                    continue
                else:
                    # see if the zip code is valid, and if the date valid
                    process_mask = [helpers.CheckZipCode(zipcode), helpers.CheckTransactionDate(dt)]

                # Check if we can process for zip file
                if process_mask[0]:
                    # see if we are encountering this id for the first time
                    if id not in dat_zip:
                        dat_zip[id] = {}

                    # Determine if this is the first time we are encountering this zip code for this id. If so, then
                    # create the ZipStreaming instance which will track the transaction values and give
                    # us the values we need to write to file.
                    if zipcode not in dat_zip[id]:
                        dat_zip[id][zipcode] = helpers.ZipStreaming()

                    # Now we are ready to the transaction amount to the list
                    trans_median, trans_total, trans_number = dat_zip[id][zipcode].ingest(int(amt))

                    # Create the line to write to file
                    lineOut = helpers.CreateZipOutputString(trans_median, trans_total, trans_number, id, zipcode)
                    # write to file
                    fid_zip.write(lineOut)
                else:
                    benchmarking_skipped_zip += 1


                # Check to see if we can process for the date file
                if process_mask[1]:
                    # Determine if we are encountering this id for the first time
                    if id not in dat_date:
                        dat_date[id] = {}

                    # See if this is the first time we are encountering this date, for this id
                    if dt not in dat_date[id]:
                        dat_date[id][dt] = []

                    # Now we are ready to the transaction amount to the list
                    dat_date[id][dt].append(int(amt))
                else:
                    benchmarking_skipped_date += 1

                line_number += 1

    # print summary fo number of entries skipped
    print('zip file - number of entries skipped: {}'.format(benchmarking_skipped_zip))
    print('date file - number of entries skipped: {}'.format(benchmarking_skipped_date))

    # Now process the date file
    print('Writing: {}'.format(date_fullfilename))
    with open(date_fullfilename, 'wb') as fid_dt:

        # Write in order of id and then by date so that we get the list of ids and sort them
        id_list = dat_date.keys()
        id_list.sort()

        for id_write_index, id_write in enumerate(id_list):

            # get all the dates for a particular id and sort them
            date_list = dat_date[id_write].keys()

            # Convert to epoch times and get the array of indices for sorting it.
            epoch_list = [helpers.ConvertTransactionDateToEpochGM(dtt) for dtt in date_list]
            date_list_arg_sort  = np.argsort(epoch_list)

            # iterate in descending time order for a particular id
            for index_ordered in date_list_arg_sort:

                date_str = date_list[index_ordered]
                # calculate the median, total, # values
                trans_median, trans_total, trans_number = \
                    helpers.CalculateTransactionValues(dat_date[id_write][date_str])

                # create the output line to write
                lineOut = helpers.CreateDateOutputString(id_write, date_str, trans_median, trans_total, trans_number)

                # write to file
                fid_dt.write(lineOut)
    print('All done.')

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Missing arguments.')
        exit
    input_fullfilename = sys.argv[1]
    zip_fullfilename = sys.argv[2]
    date_fullfilename = sys.argv[3]

    main(input_fullfilename, zip_fullfilename, date_fullfilename)