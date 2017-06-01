SBB4-damage-tracker
made by Koji
STILL A WIP

My plan was:
1. Make python read a video file 
2. Save a screenshot of every second in the video
3. Read and save the damages for p1 and p2 in arrays
4. Plot the data

————————
What the program does:

videotopictures.py 
Purpose: create a training data set.

createTrainingData - Gathers screenshot of every second in between time_start and time_stop. It also resizes the initial screenshot to 800 pixels of width, blurs it and crops out the area around P1 and P2’s damage counters. Then it finds the contours and saves the image. As seen in examplePicture1.png

labeldata2 - Create a Loads the images saved createTrainingData and so you can label the data. An image pops up, you input the numbers you see, then press anything other than a number to exit. If the picture doesn’t show a number, you just press any key other than a number to label it as "no number". It then updates the filenames to p[playernumber]_[second]_[damage in picture]. For example p2_34_57.png

cutOutNumbers - Divide the previous pictures into a set of three boxes (for 1 and 3 digit numbers) and another one of 2 boxes (for 2 digit numbers). For example: If the picture is 57% showing, the set of three boxes would save ["-","-","-"], while the set of two would save [5,7]. It then saves the five boxes as new images with the filename [dataclass]_[placeholderNumber].pdf, dataclass = 0..9 or "-" the placeholdernumber is to keep the program from making two equal filenames.

I did this with about 5 minutes of footage to generate my training data set.



trainingandtesting.py
Purpose: train a classifier and test it vs another video.

For this I modified this code, so I don't know too much about how the whole works thing works.  
http://hanzratech.in/2015/02/24/handwritten-digit-recognition-using-opencv-sklearn-and-python.html

trainClassifier: Train a classifier with the training data we've made. Also saves the classifier as a pkl file so we can use it later on.  
digits2.pkl is the classifier I’ve made from my training data.


videoToImageArray: Takes a video and returns a screenshot of P1 and P2's damage every second in an array [[P1 damage pictures],[P2 damage pictures]]

imageToDamageArray: Uses the classifier we've trained to translate the screenshots from the previous array into numbers. Uses some extra conditions, to keep the data clean. For example if the interpreted is more than 50% bigger than the previous one, it's just registered as - instead.

plotDMG: plots the data. points labeled "-" are and counts as <<same % as previous second>>



