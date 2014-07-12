=======
Matcher
=======

Matcher is a tool that matches an individual to others based on a defined range of similarity. To achieve this, matcher begins with an individual and a pool of potential candidates. Then, the pool is trimmed by removing mismatches using several metrics of both numeric and categorical data that define similarity.

Installation
=============
This version of Matcher requires Python 2.7.6, which may be downloaded here:

    https://www.python.org/download/releases/2.7.6/ 

The core package requires no installation and can be run directly from the Matcher directory.

Running
=======
Select matcher-qt.py to run the graphical interface. This will fill with default values. The example data provided with matcher is selected by default. If using your own data, follow the data format .

Documentation
=============
Matcher uses two raw data inputs: individual data and record data, both in csv format. The defaults for this are patient-list.csv and skeleton-list.csv, respectively. The filenames may be specified by the user. Data should be in columnar format for each variable with the first line containing the data labels. These labels should contain only alphanumeric characters, dashes, and underscores. The variables to be used must match between the two files. Extra data that will not be used is allowed and matcher will ignore it.

The three outputs of Matcher are Counts_Table.csv, Remaining_Table.csv, and anomaly_log.csv. Counts_Table provides a summary of the results by showing both the value of each metric and the corresponding pool size after applying that metric. Remaining_Table.csv shows the pool after matching for every individual. Anomaly_log.csv will fill with data that Matcher is unable to understand and thus ignores -- such data may need to be reformatted for Matcher to make use of it. The output directory of these files may be specified.

The user may define both the order of sorting as well as the error ranges for each numeric metric used. These may be used in a format similar to the following:

matcher(sortOrder=['Age','DeathYr','Sex','etc'],
        errorFunctions={'Age': "2", 'DeathYr': "2 * x",
                        'etc': "(0.01 * x)**0.5"})

Variables that are specified in sort order but are not given error functions will be treated as categorical data, e.g. sex, favorite food, etc.
