# Plot the scheduling coefficient heatmap #

This Python script takes the CSV output from the SAFE Scheduling Coefficient
report and produces three images:

* A heatmap of the scheduling coefficient with the number of jobs in the 
boxes
* A heatmap of the scheduling coefficient with the number of jobs and the maen
wait time in the boxes
* A heatmap of the kAU use with the number of jobs in the boxes

## Dependencies ##

This is a Python 2 script.

You need numpy and matplotlib installed for the script to work. The easiest
way to meet this is to install the Anaconda Python distribution.

## Usage ##

    python plot_sched_heatmap.py /path/to/sched/coeff.csv

