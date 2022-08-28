# TSMW_FFT
Time-Series Moving-Window outlier detection and Fourier Transform for data with
pattern-wise outliers surrounded by dubious transition data.  In Python.



This program scans through time series data and detects pattern-wise outliers 
which tend to occur in batches.  Around these batches are time series points 
which are partially compromised, so a window size and leniency approach allows
for occasional outliers to be filtered out in a Fast Fourier Transform with a 
Low Pass Filter while the batches of outliers *and* compromised adjacent points
are caught by the outlier detection routine.  For sufficiently large batches, 
the program linearly interpolates to connect the time series data, but the 
particular functionality can be chosen for the user's specific purpose.




to add: windowSize based on suspected transition region around pattern-wise outliers. 

to add: leniency depends on windowSize and user preference.

to add: tolerance explanation.

to add: how to run, cmd line args, etc.

