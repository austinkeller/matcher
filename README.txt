                              Matcher
What is it?
-----------
Matcher is a tool that matches an individual to others based on a
defined range of similarity. To achieve this, matcher begins with an
individual and a pool of potential candidates. Then, the pool is
trimmed by removing mismatches using several metrics of both numeric
and categorical data that define similarity.

Installation
------------
This version of Matcher requires Python 2.7.6, which may be downloaded 
here:

  https://www.python.org/download/releases/2.7.6/ 

The core package requires no installation and can be run directly from
the Matcher directory.

Running
-------
Select run_matcher.py to run with default values. Sort order and error
ranges may be specified by running matcher with the parameters
sortOrder and errorRanges.

Documentation
-------------
Matcher uses two raw data inputs: patient-list.csv and
skeleton-list.csv.

The three outputs of Matcher are Counts_Table.csv,
Remaining_Table.csv, and anomaly_log.csv. Counts_Table provides a
summary of the results by showing both the value of each metric and
the corresponding pool size after applying that
metric. Remaining_Table.csv shows the pool after matching for every
individual. Anomaly_log.csv will fill with data that Matcher is unable
to understand and thus ignores -- such data may need to be reformatted
for Matcher to make use of it.

The user may define both the order of sorting as well as the error
ranges for each numeric metric used. These may be used in a format
similar to the following:

  matcher(sortOrder=['Age','DeathYr','otherCategory','etc'],
          errorRanges={'Age': 0.2, 'DeathYr': 2, 'etc': 0.01})
        
