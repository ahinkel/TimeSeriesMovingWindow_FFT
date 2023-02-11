# TSMW_FFT
Time-Series Moving-Window outlier detection and Fourier Transform for data with
pattern-wise outliers surrounded by dubious transition data.  In Python.


## Summary:
This program scans through time series data and detects pattern-wise outliers 
which tend to occur in batches.  Around these batches are time series points 
which are partially compromised, so a window size and leniency approach allows
for occasional outliers to be filtered out in a Fast Fourier Transform with a 
Low Pass Filter while the batches of outliers *and* compromised adjacent points
are caught by the outlier detection routine.  For sufficiently large batches, 
the program linearly interpolates to connect the time series data, but the 
particular functionality can be chosen for the user's specific purpose.

The current outliers the program is designed to catch are -1's in the time 
series data.  This can be changed as needed.  I hope to update the code
to be more general.


## Note:
I really need to clean this code and readme up.


## Dependencies:
numpy

matplotlib

sys

written in python 2.7 (update print statement if using python3)


## Parameters:

### sampleRate 
number of samples per second in the input time-series data

### cutOff
cutoff frequency for the low pass filter used during the FFT process.

### windowSize
A moving window size that is based on suspected transition region around pattern-wise outliers.  (Currently needs to be an odd number.  Will maybe update later.)  For example, if the pattern-wise outliers are surrounded by up to 3 dubious transition points, a window size of 2 x 3 + 1 = 7 will provide the correct 'buffer zone' during the outlier detection algorithm.

### margin
(windowSize-1)/2 -- the size of the buffer zone.  See above.

### leniency 
How lenient the outlier detection program is when counting outliers.  That is, the algorithm counts all outliers within +/- margin from the time-series data point in question, and if the number of outliers are less than or equal to the leniency value, the program does not identify the outlier as a pattern-wise outlier, and allows it to be filtered out in the Discrete Fast Fourier Transfrom (FFT) low pass filter process.  If the number of identified outliers are greater than the leniency value, the algorithm identifies the block of data as a pattern-wise outlier, and performs the FFT only on the data up to and not including the pattern-wise outlier.  The outlier region is skipped momentarily, and the process repeats in order to find other stretches of reliable data.  Each stretch of reliable data, after passing through a low pass filter FFT process is then connected across any pattern-wise outliers by a simple linear interpolation.  The interpolation routine can be modified to fit other use cases.  The leniency value should be chosen based on the expected outlier signature in the data. That is, a leniency should be high enough to allow any expected "one-off" outliers through to the low-pass filter and FFT stage, while low enough to catch pattern-wise outliers. Must be less than windowSize.

## To run:
python TSMW_FFT.py inputFile.csv > outputFile.csv 

## Tags: 
FFT, Fast Fourier Transform, Outlier Detection, Pattern-wise Outlier Detection, Moving Window Scan, Python
