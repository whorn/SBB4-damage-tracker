import cv2
from sklearn.externals import joblib
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
import imutils
import os
import glob
import matplotlib.pyplot as plt


CLF = joblib.load("digits2.pkl") #CLASSIFIER

def trainClassifier(foldername,classifierName):
    model = cv2.ml.KNearest_create()
    features = []
    labels = []
    os.chdir(foldername)
    for filename in glob.iglob('*.png'):
        features.append(cv2.imread((filename),-1))
        labels.append(filename[0])
    list_hog_fd = []
    for feature in features:
        fd = hog(feature.reshape((27, 35)), orientations=9, pixels_per_cell=(9, 7), cells_per_block=(1, 1), visualise=False)
        list_hog_fd.append(fd)
    hog_features = np.array(list_hog_fd, 'float64')
    os.chdir("..")
    clf = LinearSVC()
    clf.fit(hog_features, labels)
    joblib.dump(clf,classifierName, compress=3)
    os.chdir("..")

def testClassifier(foldername,classifier):
    clf = joblib.load(classifier)
    os.chdir(foldername)
    correct = 0
    total = 0
    for filename in glob.iglob('*.png'):
        img = cv2.imread(filename,-1)
        roi = hog(img.reshape((27, 35)), orientations=9, pixels_per_cell=(9, 7), cells_per_block=(1, 1), visualise=False)
        preditcion = clf.predict(roi)
        if preditcion == filename[0]:
            correct += 1
        total += 1
    print(total)
    print(correct)
def videoToImageArray(filename,time_start,time_stop):
    vidcap = cv2.VideoCapture(filename)
    pictures = [[],[]]
    for time in range(time_start,time_stop):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,time*1000)      # just cue to 20 sec. position
        success,image = vidcap.read()
        image = cv2.medianBlur(image,7)
        resized = imutils.resize(image, width=800)
        p1 = resized[370:430,220:300]
        p2 = resized[370:430,520:600]
        p1 = cv2.Canny(p1, 400, 100, 255)
        p2 = cv2.Canny(p2, 400, 100, 255)
        pictures[0].append(p1)
        pictures[1].append(p2)
    return pictures
def imageToDamageArray(image_array):
    dmg = [[],[]]
    lastdamage = [0,0]
    for player in range(2):
        for time in range(len(image_array[1])):
            three_cell1 = CLF.predict([hog(image_array[player][time][4:39,2:29].reshape((27, 35)),orientations=9, pixels_per_cell=(9, 7), cells_per_block=(1, 1), visualise=False)])[0]
            three_cell2 = CLF.predict([hog(image_array[player][time][4:39,23:50].reshape((27, 35)),orientations=9, pixels_per_cell=(9, 7), cells_per_block=(1, 1), visualise=False)])[0]
            three_cell3 = CLF.predict([hog(image_array[player][time][4:39,48:75].reshape((27, 35)),orientations=9, pixels_per_cell=(9, 7), cells_per_block=(1, 1), visualise=False)])[0]
            two_cell1 = CLF.predict([hog(image_array[player][time][4:39,13:40].reshape((27, 35)),orientations=9, pixels_per_cell=(9, 7), cells_per_block=(1, 1), visualise=False)])[0]
            two_cell2 =  CLF.predict([hog(image_array[player][time][4:39,37:64].reshape((27, 35)),orientations=9, pixels_per_cell=(9, 7), cells_per_block=(1, 1), visualise=False)])[0]
            if three_cell1 != "-" and three_cell2 != "-" and three_cell3 != "-":
                if int(three_cell1)*100+int(three_cell2)*10-lastdamage[player]>50:
                    #print(three_cell1,three_cell2,three_cell3)
                    #print(two_cell1,two_cell2)
                    if two_cell1 != "-" and two_cell2 != "-" and two_cell1 != 0:
                        dmg[player].append(10*int(two_cell1)+int(two_cell2))
                        lastdamage[player]=dmg[player][-1]
                    else:
                        dmg[player].append("-")
                else:
                    dmg[player].append(100*int(three_cell1)+10*int(three_cell2)+int(three_cell3))
                    lastdamage[player]=dmg[player][-1]
            elif two_cell1 != "-" and two_cell2 != "-" and two_cell1!= 0:
                dmg[player].append(10*int(two_cell1)+int(two_cell2))
                lastdamage[player]=dmg[player][-1]
            elif three_cell1 == "-" and three_cell2 != "-" and three_cell3 == "-":
                dmg[player].append(int(three_cell2))
            else:
                dmg[player].append("-")
    return dmg

def plotDMG(dmg_array):
    points = [[[0,0]],[[0,0]]]
    for i in range(len(dmg_array[0])):
        for player in range(2):
            if dmg_array[player][i]!="-":
                if dmg_array[player][i] != points[player][-1][1] and (dmg_array[player][i] -points[player][-1][1] > -5 or dmg_array[player][i] == 0):
                    points[player].append([i-1,points[player][-1][1]])
                    points[player].append([i,dmg_array[player][i]])
    plt.plot([points[0][i][0] for i in range(len(points[0]))],[points[0][i][1] for i in range (len(points[0]))],"o-",label = "p1 damage over time")
    plt.plot([points[1][i][0] for i in range(len(points[1]))],[points[1][i][1] for i in range (len(points[1]))],"o-",label = "p2 damage over time")
    plt.xlabel("time passed (s)")
    plt.ylabel("damage taken")
    plt.legend()
    plt.savefig("damgegraph.png")
    plt.show()
#testClassifier("testdata.mp4","digits_cls.pkl")
#trainClassifier("justNumbers","digits2.pkl")
#
dmg = imageToDamageArray(videoToImageArray("testvid.mp4",5,220))
plotDMG(dmg)
