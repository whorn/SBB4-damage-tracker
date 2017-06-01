__author__ = 'William'
import cv2
import imutils
import os
import glob

def createTrainingData(filename,time_start,time_stop):
    vidcap = cv2.VideoCapture(filename)
    try:
        os.makedirs("trainingdata_"+filename)
    except OSError:
        pass
    os.chdir("trainingdata_"+filename)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    for time in range(time_start,time_stop):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,time*1000)
        success,image = vidcap.read()
        image = cv2.medianBlur(image,7)
        resized = imutils.resize(image, width=800)
        p1 = resized[370:430,220:300]
        p2 = resized[370:430,520:600]
        p1 = cv2.Canny(p1, 400, 100, 255)
        p2 = cv2.Canny(p2, 400, 100, 255)
        cv2.imwrite('p1_'+str(time)+".png",p1)
        cv2.imwrite('p2_'+str(time)+".png",p2)
    os.chdir("..")
def labelData(foldername):
    os.chdir(foldername)
    for filename in glob.iglob('*.png'):
        print(filename)
        img = cv2.imread(filename,-1)
        three_cell1 = img[4:39,2:29]
        three_cell2 = img[4:39,23:50]
        three_cell3 = img[4:39,48:75]
        two_cell1 = img[4:39,13:40]
        two_cell2 =  img[4:39,37:64]
        ims = [three_cell1,three_cell2,three_cell3,two_cell1,two_cell2]
        numbs = []
        for pic in ims:
            cv2.imshow("preview", pic)
            k = cv2.waitKey(0)
            if k == 45:
                numbs.append("-")
            else:
                numbs.append(k-48)
        if numbs[0] == "-" and numbs[1]!="-":
            os.rename(filename, filename[:-4]+"_"+str(numbs[1])+".png")
        elif numbs[0] != "-":
            os.rename(filename, filename[:-4]+"_"+str(numbs[0])+str(numbs[1])+str(numbs[2])+".png")
        elif numbs[4] != "-":
            os.rename(filename, filename[:-4]+"_"+str(numbs[3])+str(numbs[4])+".png")
        else:
            os.rename(filename, filename[:-4]+"_-.png")
def labelData2(foldername):
    os.chdir(foldername)
    for filename in glob.iglob('*.png'):
        img = cv2.imread(filename,-1)
        number = ""
        cv2.imshow("preview",img)
        while(1):
            k = cv2.waitKey(0)
            if k not in range(48,58):
                break
            else:
                number += str(k-48)
        if number == "":
            os.rename(filename, filename[:-4]+"_-.png")
        else:
            os.rename(filename, filename[:-4]+"_"+number+".png")
def cutOutNumbers(foldername):
    os.chdir(foldername)
    i = X
    for filename in glob.iglob('*.png'):
        if filename[-6] == "_":
            img = cv2.imread(filename,-1)
            cv2.imwrite('-_'+str(i)+".png",img[4:39,2:29])
            i +=1
            cv2.imwrite(str(filename[-5])+"_"+str(i)+".png",img[4:39,23:50])
            i += 1
            cv2.imwrite('-_'+str(i)+".png",img[4:39,48:75])
            i += 1
        elif filename[-7] == "_":
            img = cv2.imread(filename,-1)
            cv2.imwrite(str(filename[-6])+"_"+str(i)+".png",img[4:39,13:40])
            i += 1
            cv2.imwrite(str(filename[-5])+"_"+str(i)+".png",img[4:39,37:64])
            i += 1
    os.chdir("..")

#createTrainingData("sayyes4.mp4",70,90)
#createTrainingData("match3.mp4",10,240)
#createTrainingData("videotest.mp4",0,60)
#labelData("trainingdata_match1.mp4")
#labelData2("trainingdata_match3.mp4")
X = 2500
cutOutNumbers("trainingdata_match3.mp4")


