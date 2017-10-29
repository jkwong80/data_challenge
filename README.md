# Table of Contents
1. [Introduction](README.md#introduction)
2. [Description of the Repository](README.md#description-of-the-repository)
3. [Requirements](README.md#requirements)
4. [Installation](README.md#installation)
5. [Running Tests](README.md#running-tests)
6. [Description of Approach](README.md#description-of-approach)
7. [Discussion](README.md#discussion)

# Introduction


A full description of the challenge can be found [here](https://github.com/InsightDataScience/find-political-donors).

Here's a summary of the task taken from that github.

"You’re given one input file, `itcont.txt`. Each line of the input file contains information about a campaign contribution that was made on a particular date from a donor to a political campaign, committee or other similar entity. Out of the many fields listed on the pipe-delimited line, you’re primarily interested in the zip code associated with the donor, amount contributed, date of the transaction and ID of the recipient.

Your code should process each line of the input file as if that record was sequentially streaming into your program. For each input file line, calculate the running median of contributions, total number of transactions and total amount of contributions streaming in so far for that recipient and zip code. The calculated fields should then be formatted into a pipe-delimited line and written to an output file named `medianvals_by_zip.txt` in the same order as the input line appeared in the input file. 

Your program also should write to a second output file named `medianvals_by_date.txt`. Each line of this second output file should list every unique combination of date and recipient from the input file and then the calculated total contributions and median contribution for that combination of date and recipient. 

The fields on each pipe-delimited line of `medianvals_by_date.txt` should be date, recipient, total number of transactions, total amount of contributions and median contribution. Unlike the first output file, this second output file should have lines sorted alphabetical by recipient and then chronologically by date.

Also, unlike the first output file, every line in the `medianvals_by_date.txt` file should be represented by a unique combination of day and recipient -- there should be no duplicates."


# Description of the Repository


Repository Structure

	.
	├── README.md
	├── input
	│   ├── README.md
	│   └── itcont.txt
	├── output
	│   ├── README.md
	│   ├── medianvals_by_date.txt
	│   └── medianvals_by_zip.txt
	├── insight_testsuite
	│   ├── results.txt
	│   ├── run_tests.sh
	│   └── tests
	│       └── test_1
	│           ├── README.md
	│           ├── input
	│           │   └── itcont.txt
	│           └── output
	│               ├── medianvals_by_date.txt
	│               └── medianvals_by_zip.txt
	├── install.sh
	├── run.sh
	├── run_unit_tests.sh
	├── create_plots.sh
	├── requirements.txt
	└── src
	    ├── README.md
	    ├── __init__.py
	    ├── find_political_donors_beta.py
	    ├── find_political_donors_gamma.py
	    ├── find_political_donors_delta.py
	    ├── helpers.py
	    ├── test_lib_helpers.py
	    └── benchmark_median.py

Description of the important files:

* `install.sh` - installs dependencies
* `run.sh` - runs my python script for creating the two txt files
* `run_unit_tests.sh` - runs unit tests
* `requirements.txt` - list of packages to be installed by pip
* `find_political_donors_delta.py` - my main script for generating the txt files
* `find_political_donors_gamma.py` - older version that is retained for historical reasons; does not work
* `find_political_donors_beta.py` - older version that is retained for historical reasons; does not work
* `helpers.py` - helper functions and classes used by find_political_donors_delta.py
* `test_lib_helpers.py` - unit tests
* `benchmark_median.py` - make some benchmark plots comparing two methods of calculating medians
* `create_plots.sh` - runs `benchmark_median.py`; this is optional

# Requirements

Running this package requires the following:

* Python 2.7 and pip python manager.  It will probably work with Python 3 but it has not been tested.
* Ubuntu or OS X.  My script will probably work as is in Windows but this has not been tested.
* Python packages as listed in the requirements.txt file
	* Numpy
	* Matplotlib (if you wish to make some of the diagnostic plots)

If you have installed the Anaconda Python distribution, then my script should work without additional installations.  I recommend using [virtual environments](https://virtualenv.pypa.io/en/stable) to segment your Python environments but that is beyond the scope of this document.  I also recommend using the outstanding virtual environment manager, [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

# Installation
To install the requisite packages, run `./setup.sh`.  This requires Python and pip and should take around a minute to complete.

# Running Tests
I have several unit tests for testing out the various helper functions and classes.  They are located in `/src/tests/test_lib_helpers.py`.

To run the tests:

`./run_unit_tests.sh`

If all the tests pass, the final output should look like this:

```

----------------------------------------------------------------------
Ran 14 tests in 2.222s
```


Run `./run.sh`, to run my script for generating the `medianvals_by_zip.txt` and `medianvals_by_date.txt` files.  You should see an output like this:

```
Line 100000, time elapsed: 3.457, time since last report: 3.455, rate: 28940.210 Hz
Line 200000, time elapsed: 6.838, time since last report: 3.381, rate: 29578.606 Hz
Line 300000, time elapsed: 9.914, time since last report: 3.075, rate: 32517.806 Hz
Line 400000, time elapsed: 13.323, time since last report: 3.410, rate: 29326.169 Hz
Line 500000, time elapsed: 17.596, time since last report: 4.273, rate: 23402.909 Hz
...
...
Line 3900000, time elapsed: 118.217, time since last report: 1.210, rate: 82638.747 Hz
Line 4000000, time elapsed: 121.584, time since last report: 3.366, rate: 29704.522 Hz
Line 4100000, time elapsed: 123.249, time since last report: 1.665, rate: 60048.118 Hz
Line 4200000, time elapsed: 125.006, time since last report: 1.756, rate: 56937.364 Hz
zip file - number of entries skipped: 1997341
date file - number of entries skipped: 1992947
Writing: ./output/medianvals_by_date.txt
All done.
```

Every 100,000 lines processed, it will display a report.  The report values from left to right: the current line number, the time elapsed since the start of the script, the time since the last report, and the rate at which the lines are being processed.  Note that the rate flucuates greatly because of variance in the number of lines being thrown out.  

Run `create_plots.sh` to create some png of plots comparing two methods of calculating the median values. I describe the methods in a later section.

# Description of Approach

## Data Structures
I decided to use a dict of dict to hold the contribution values for the _date file, organized by id and transaction date:
	
	dat_date[id][date] = []

where `[]` is a list.  I used a similar structure to hold the transaction values for the _zip file:
	
	dat_zip[id][zip] = []

For this data structure, I initially had the dicts also hold a list but then later converted to having it store instances of a class designed to calculate medians on streaming values.  This is described in the next section.

## Pseudocode

This is a rough outline of what `find_political_donors_delta.py` is doing

	for line from File:
		parse the line
		determine if we should process for _zip and _date files
		if process for _zip file
			if first time seeing id and zip
				add container (or class instance) to store amount
			add amount to container
			calculate _zip values
			write to _zip file
		if process for _date file
			if first time seeing id and date
				add container to store amount
			add amount to container
	write to _date file
			

I had two concerns: the calculation of the running median and the dynamically changing data structures needed to store contribution values for an indefinite number of id’s, zip codes and dates.  After, some experimentation, I convinced myself that using expanding lists in dicts of dicts to hold the contributions is not a concern.  This should not be a surprise as expanding a dictionary and appending an element to a list are O(1) (amortized) operations.  The numpy median functions is fairly fast on modern computers but for larger arrays, it becomes significant.  For example, it takes 140ms to find the median of 1M floats on an i5-7360U CPU.  Given the significant number of computations that are expected to occur, it should be optimized.  To serve as a baseline, I constructed my first version of the script using a list for each combination of id and zip code and using numpy.median to calculate the value every time a contribution value is appended.  This is expected to be slow as this function must resort the entire list everytime a value is appended.  The time to process the 2016 dataset (828.8 MB; 4,206,727 lines) is about 330 seconds.
Next, I wrote a simple algorithm that maintains two sorted lists of contributions, one for values above the median and another for those below.  This is accomplished by using two min heaps (one of the heaps should be a max heap but the min heap operates as such by making the values negative). This change cuts the run time on the 2016 dataset by about 40% to 170 seconds.  Next, I made some miscellaneous improvements to my helper functions for reading and parsing the input.  This resulted in an additional ~24% reduction in the processing time to 130 seconds (60% reduction from the naive approach).


# Discussion
There is definitely room for improvement.  These are some of the things I would try if I had more time:

* Try to write a median algorithm that takes advantage of the fact that the number of unique contribution values is small.  For example, the number of unique values in the first 20,000 entries is ~750.  The contribution with the highest frequency (~10%) is $250.

* Try to write an algorithm that estimates the median by tracking the distribution of the incoming values in a running histogram instead of retaining all the values to calculate an exact median value.  This, of course, does not solve the problem presented here but would nonetheless be interesting to try out.

