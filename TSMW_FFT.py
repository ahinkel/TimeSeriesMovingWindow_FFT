# Created by Austin Hinkel, 2022
import numpy as np
import matplotlib.pyplot as plt
import sys

"""
*************************************************
*************************************************

*****************PLEASE NOTE*********************

Please see readme file in the github repository
https://github.com/ahinkel/TimeSeriesMovingWindow_FFT


*********************INPUT***********************

File input format description:
4 columns with 1 header row followed by data.
Columns: Frame, Time (s), X (cm), Y (cm)

The X and Y positions are assigned a -1 when data
is missed by the experimental setup. 

Please also see example data file.


*********************OUTPUT**********************
See print statements below.  
Filtered data begins on row 4.


*********************TO RUN**********************
python TSMW_FFT.py inputFile.csv > outputFile.csv

*************************************************
*************************************************
"""



fileInput = sys.argv[1]

def lowPassFilter(kArr, freqArr, cutOffFreq):
    for i in range(0,len(freqArr)):
        if freqArr[i] > cutOffFreq:
            kArr.real[i] = 0;
            kArr.imag[i] = 0;
    return kArr

def sliceFFT(inputX, inputT, cutOff):
    kspaceData = np.fft.rfft(inputX)
    freq = np.fft.rfftfreq(inputT.shape[-1], d=1.0/sampleRate)
    filteredData = lowPassFilter(kspaceData, freq, cutOff)
    outputX = np.fft.irfft(filteredData, len(inputX))
    return outputX

def interpolateData(array):
    #only need this if leniency is 0 and the lowpass filter fails to remove sparse -1's
    for q in range(1, len(array)-1):
        if array[q] < 0:
            #iCtr never higher than 1, so this is safe I think...
            array[q] = 0.5*(array[q-1] + array[q+1])
            #this won't remove a -1 if it is the first or last point.
    return array


#CONSTANTS/PARAMETERS:
nullIndicator = -0.5 # -1's are null. Anything less than nullIndicator is a null
sampleRate = 75 #per second
windowSize = 7 #odd number (symmetric)
margin = (windowSize - 1)/2
minPoints = 75 #try with len(xData)
fcutOff = 6
leniency = 0

#data must be in file here w/o @'s at end: 
data = np.loadtxt(fileInput, delimiter=',', skiprows=1) 

tData = data[:,1]
xData = data[:,2]
yData = data[:,3]

"""
#plot raw data:
plt.plot(tData,yData,'k-')
plt.show()

#plot raw data:
plt.plot(tData,xData,'k-')
plt.show()
"""


iCtr = np.zeros(len(xData) - margin)
conf = np.zeros(len(xData) - margin)
# See how many -1's are w/in +/- the margin of a given point 
for i in range(margin, len(xData) - margin):
    tempCtr = 0
    for j in range(-margin, margin+1):
        if xData[i + j] < nullIndicator:
            tempCtr += 1
    iCtr[i] = tempCtr


#See how many's 0's or 1's are in a row, starting at some index k
for k in range(0, len(xData) - margin):
    tmpConf = 0
    for n in range(k,len(xData)-margin):
        if iCtr[n] <= leniency:
            tmpConf += 1
        else:
            break
    conf[k] = tmpConf




#########
# MAIN()
#########

#Analyze Data if there are at least "minPoints" good points in a row:
useT = np.array([])
useX = np.array([])
useY = np.array([])
useR = np.array([])
goodCtr = 0
totXmovement = 0
totYmovement = 0
totRmovement = 0

nextRun = 0
for m in range(margin, len(xData) - margin):
    #print nextRun, conf[m]
    if conf[m] > minPoints and m>=nextRun:
        goodCtr += conf[m]
        nextRun = m+int(conf[m])
        xSlice = np.array([])
        ySlice = np.array([])
        tSlice = np.array([])
        xSlice = xData[m - margin:m - margin + int(conf[m])]
        ySlice = yData[m - margin:m - margin + int(conf[m])]
        tSlice = tData[m - margin:m - margin + int(conf[m])]
        #FFT of a good run of data
        newX = sliceFFT(xSlice, tSlice, fcutOff)
        newY = sliceFFT(ySlice, tSlice, fcutOff)
        newR = np.sqrt(newX*newX + newY*newY)
        #add to final array:
        useT = np.append(useT, tSlice)
        useX = np.append(useX, newX)
        useY = np.append(useY, newY)
        useR = np.append(useR, newR)
        for n in range(0,len(newX)-1): 
            totXmovement += np.abs(newX[n+1] - newX[n])
            totYmovement += np.abs(newY[n+1] - newY[n])
            totRmovement += np.sqrt((newX[n+1] - newX[n])**2 + (newY[n+1] - newY[n])**2)
    elif nextRun <= m:
        nextRun += 1


#Now Linearly interpolate the missing data between good runs of data.
finalT = np.array([])
finalX = np.array([])
finalY = np.array([])
finalR = np.array([])
for w in range(0,len(useT)-1): #-1 for discrete difference
    if useT[w+1]-useT[w] < (1.5/sampleRate): 
        #IMPORTANT NOTE: 1.5/sampleRate means 1.5 frames -- accounts for rounding
        #this means consecutive points:
        finalT = np.append(finalT, useT[w])
        finalX = np.append(finalX, useX[w])
        finalY = np.append(finalY, useY[w])
        finalR = np.append(finalR, useR[w])
    else:
        #this means a "jump" that we need to interpolate.
        framesMissed = int(round((useT[w+1]-useT[w])/(1.0/sampleRate)))
        timeMissed = framesMissed*(1.0/sampleRate)
        xJump = useX[w+1]-useX[w]
        yJump = useY[w+1]-useY[w]
        xSlope = xJump/timeMissed
        ySlope = yJump/timeMissed
        #append start point of Interpolation
        finalT = np.append(finalT, useT[w])
        finalX = np.append(finalX, useX[w])
        finalY = np.append(finalY, useY[w])
        finalR = np.append(finalR, useR[w])
        lastT = useT[w]
        lastX = useX[w]
        lastY = useY[w]
        lastR = useR[w]
        for z in range(0,framesMissed-1):
            #z+1 is the number of frames and * timeStep = timeElapsed
            missingT = (z+1) * (1.0/sampleRate) + useT[w]
            missingX = xSlope * (z+1) * (1.0/sampleRate) + useX[w]
            missingY = ySlope * (z+1) * (1.0/sampleRate) + useY[w]
            missingR = np.sqrt(missingX**2 + missingY**2)
            #append missing data:
            finalT = np.append(finalT, missingT)
            finalX = np.append(finalX, missingX)
            finalY = np.append(finalY, missingY)
            finalR = np.append(finalR, missingR)
            goodCtr += 1
            #need to add to sum from earlier for these missing points.
            totXmovement += np.abs(missingX - lastX)
            totYmovement += np.abs(missingY - lastY)
            totRmovement += np.sqrt((missingX - lastX)**2 + (missingY - lastY)**2)
            #update "last" point:
            lastT = missingT
            lastX = missingX
            lastY = missingY
            lastR = missingR
            if z == framesMissed-2:
                totXmovement += np.abs(useX[w+1] - lastX)
                totYmovement += np.abs(useY[w+1] - lastY)
                totRmovement += np.sqrt((useX[w+1] - lastX)**2 + (useY[w+1] - lastY)**2)



print "Points Used,", "Total X Movement (cm),", "Total Y Movement (cm),", "Total R Movement (cm),", "Original Number of Points"
printStr = str(int(goodCtr)) + "," + str(totXmovement) + "," + str(totYmovement) + "," + str(totRmovement) + "," + str(len(tData))
print printStr


print "Time (s),", "X (cm),", "Y (cm),", "R (cm)"
for p in range(0,len(finalX)):
    myStr = str(finalT[p]) + "," + str(finalX[p]) + "," + str(finalY[p]) + "," + str(finalR[p])
    print myStr

