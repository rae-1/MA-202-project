import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

circles_data = []

maxNumberOfParticles = 0
minNumberOfParticles = 1000000
sum = 0
imageIdContainingMaxNumberOfParticles = 0
imageIdContainingMinNumberOfParticles = 0

for i in range(490):

    imgNumber    = str(i)
    imgNumber    = imgNumber.zfill(5)

    fileLocation = f"C:\\Users\\sahil\\Documents\\MA202-project\\mathsProject(MA202)\\images\\Img_{imgNumber}.tif"

    imgCLR       = cv.imread(fileLocation)

    img          = cv.cvtColor(imgCLR, cv.COLOR_BGR2GRAY)

    blur         = cv.GaussianBlur(img, (19, 19), 0)

    threshold    = cv.threshold(blur, 125, 255, cv.THRESH_BINARY)[1]
    
    circles      = cv.HoughCircles(threshold, cv.HOUGH_GRADIENT,
                                    dp=2.8, minDist=13,
                                    param1 = 20, param2 = 10,
                                    minRadius = 1, maxRadius = 7)

    circles_data.append(circles)

    if circles is not None:

        numberOfParticles = circles.shape[1]
        sum += numberOfParticles

        print("\nNo. of particles in ", imgNumber, "th", "image : ",numberOfParticles)

        if(maxNumberOfParticles < numberOfParticles):

            maxNumberOfParticles = numberOfParticles
            imageIdContainingMaxNumberOfParticles = i

        if(minNumberOfParticles > numberOfParticles):
            
            minNumberOfParticles = numberOfParticles
            imageIdContainingMinNumberOfParticles = i


print("\nImage Id Containing Max Number Of Particles: ", imageIdContainingMaxNumberOfParticles)
print("Max Number Of Particles: ", maxNumberOfParticles)
print("\nImage Id Containing Max Number Of Particles: ", imageIdContainingMinNumberOfParticles)
print("Max Number Of Particles: ", minNumberOfParticles)



# Average value of number of circles(particles) in all images
# print(avg/490)
# sum = 0
# for i in range(0, 490):
#     sum += len(circles_data[i][0])

average = sum/490

print("\nAverage no. of particles: ", average)


combinedData = []
meanData = []
varData = []

totalNumberOfParticles = 0
totalNumberOfImages = len(circles_data)

for i in range(totalNumberOfImages):
    
    dataOfSingleImage = []
    numberOfParticlesInEachImage = len(circles_data[i][0])
    totalNumberOfParticles += numberOfParticlesInEachImage
    
    for j in range(numberOfParticlesInEachImage):

        Xc = circles_data[i][0][j][0]
        Yc = circles_data[i][0][j][1]
        r  = circles_data[i][0][j][2]
        
        dataOfSingleParticle = [i,Xc,Yc,r]
        combinedData.append( dataOfSingleParticle )
        dataOfSingleImage.append( dataOfSingleParticle )
        
    dfPerImage = pd.DataFrame(dataOfSingleImage, columns = ['Image Number', 'Xc', 'Yc', 'R'])
    meanData.append(list(dfPerImage.mean()))
    varData.append(list(dfPerImage.var()))


dfPopulation      = pd.DataFrame(combinedData , columns = ['Image Number', 'Xc', 'Yc', 'R'])
dfMean            = pd.DataFrame(meanData     , columns = ['Image Number', 'Mean of Xc', 'Mean of Yc', 'Mean of R'])
dfVar             = pd.DataFrame(varData      , columns = ['Image Number', 'Variance of Xc', 'Variance of Yc', 'Variance of R'])


# Expectation value of mean of x-coordinates = Mean of x-coord. values from dfMean dataframe.
expectationOfSampleMean = list(dfMean.mean())[1]
print("\nExpectation value of sample mean(Xc): ", expectationOfSampleMean)


# Standarad Deviation of sample mean
standardDeviationOfSampleMean = (list(dfMean.var())[1])**0.5
print("Standarad Deviation of sample mean: ", standardDeviationOfSampleMean)


# Mean of Population
populationMean = list(dfPopulation.mean())[1]
print("\nMean of Population: ", populationMean)


# Value of (Standard Deviation / n) for the population
var = list(dfPopulation.var())[1]
sigma = var**0.5
print("Standard Deviation of the population divided by sqrt n: ", sigma/(2036**0.5))
print("\n")



plt.hist(dfPopulation['Xc'], bins='auto')
plt.show()


plt.hist(dfMean['Mean of Xc'], bins='auto')
plt.show()


plt.hist(dfVar['Variance of Xc'], bins='auto')
plt.show()