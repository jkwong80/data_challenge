# Table of Contents
1. [Introduction](README.md#introduction)
2. [Description of the Repository](README.md#description-of-the-repository)
3. [Requirements](README.md#requirements)
4. [Installation](README.md#installation)
5. [Running Tests](README.md#running-tests)
6. [Description of Approach](README.md#description-of-approach)
7. [Discussion](README.md#discussion)
8. [Conclusion](README.md#conclusion)

# Introduction


A full description of the challenge can be found [here](https://github.com/InsightDataScience/find-political-donors).

Here's good summary of the task taken from that github.

"You’re given one input file, `itcont.txt`. Each line of the input file contains information about a campaign contribution that was made on a particular date from a donor to a political campaign, committee or other similar entity. Out of the many fields listed on the pipe-delimited line, you’re primarily interested in the zip code associated with the donor, amount contributed, date of the transaction and ID of the recipient.

Your code should process each line of the input file as if that record was sequentially streaming into your program. For each input file line, calculate the running median of contributions, total number of transactions and total amount of contributions streaming in so far for that recipient and zip code. The calculated fields should then be formatted into a pipe-delimited line and written to an output file named `medianvals_by_zip.txt` in the same order as the input line appeared in the input file. 

Your program also should write to a second output file named `medianvals_by_date.txt`. Each line of this second output file should list every unique combination of date and recipient from the input file and then the calculated total contributions and median contribution for that combination of date and recipient. 

The fields on each pipe-delimited line of `medianvals_by_date.txt` should be date, recipient, total number of transactions, total amount of contributions and median contribution. Unlike the first output file, this second output file should have lines sorted alphabetical by recipient and then chronologically by date.

Also, unlike the first output file, every line in the `medianvals_by_date.txt` file should be represented by a unique combination of day and recipient -- there should be no duplicates."

# Description of the Repository


The directory structure for your repo should look like this:

	.
	├── README.md
	├── input
	│   ├── README.md
	│   ├── itcont.txt
	│   ├── itcont_2016_full.txt
	│   └── itcont_short.txt
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
	├── output
	│   ├── README.md
	│   ├── medianvals_by_date.txt
	│   └── medianvals_by_zip.txt
	├── requirements.txt
	├── run.sh
	├── run_unit_tests.sh
	├── setup.sh
	├── src
	    ├── README.md
	    ├── __init__.py
	    ├── benchmarks.py
	    ├── explore_data_file.py
	    ├── find_political_donors_beta.py
	    ├── find_political_donors_delta.py
	    ├── find_political_donors_gamma.py
	    ├── lib
	    │   ├── __init__.py
	    │   ├── helpers.py
	    ├── streaming_median.py
	    └── tests
	        ├── __init__.py
	        └── test_lib_helpers.py


# Installation
To install the requisite packages, run `./setup.sh`.  This requires Python and pip.

# Running Tests
I have several unit tests for testing out the various helper functions and classes.  They are located in `/src/tests/test_lib_helpers.py`.

To run the tests:

`./run_unit_tests.sh`

```
If all the tests pass, the final output should look like this:

----------------------------------------------------------------------
Ran 14 tests in 2.222s
```

# Description of Approach

One of the concerns I had was the calculation of the running median and the dynamically changing structures needed to store an indefinite number of id’s, zip codes and datas.  After, some experimentation, I convinced myself that having expanding lists to hold contributions really isn’t a concern.  This shouldn’t be a surprises as appending an element to a list is a O(1) (amortized) operation.  The running median is fairly fast on a modern computer with the built-in numpy function (np.median) but for larger arrays, it becomes significant and, given the significant number of computations that are expected to occur, it should be optimized. Nonetheless, I constructed my first version of main function using a list for each combination of id and zip code and using np.median to calculate the value every time a contribution value is appended.  This is expected to be slow as this function must resort the entire list.  The time to process the 2016 dataset (828.8 MB; 4,206,727 lines) is about 330 seconds.
Next, I wrote a simple algorithm that maintains two sorted lists of contributions for values, one for values above the median and another for those below.  This is accomplished by using two min heaps (one of the heaps should be a max heap but the min heap operates as such by making the values negative.)  This change cuts the run time on the 2016 dataset by about 40% to 170 seconds.  Next I made some miscellaneous improvements to my helper functions which parse the lines from the input text file.  This resulted in an additional ~24% reduction in the processing time (60% reduction from the naive approach) to 130 seconds.

# Discussion

# Conclusion
