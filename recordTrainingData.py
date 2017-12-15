import cv2
import screenShot
from key import getKeys
import numpy as np
import os
from time import time, sleep


w = [1,0,0,0,0,0]
a = [0,1,0,0,0,0]
d = [0,0,1,0,0,0]
wa = [0,0,0,1,0,0]
wd = [0,0,0,0,1,0]
nk = [0,0,0,0,0,1]


def keysOutput(keys):
    output = [0,0,0,0,0,0]

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'W' in keys:
        output = w
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output

if __name__ == "__main__":

    fileName = "trainingData.npy"
    # Load data from file
    if os.path.isfile(fileName):
        print("File exists")
        trainingData = list(np.load(fileName))
    else:
        print("Creating new File")
        trainingData = []

    record = False
    print("Press 'P' to start and stop recording!")

    while True:
        keyPressed = getKeys();
        if 'P' in keyPressed:
            if record:
                record = False
                print("Paused");
                sleep(1)
            else:
                record = True
                for i in range(1,4):
                    print(4-i)
                    sleep(1)
                print("Recording!")

        if record:
            last_time = time()
            screen = screenShot.takeScreenShot(region=(0,30,800,630))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160, 120))
            #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            keys = getKeys()
            output = keysOutput(keys)
            #print(output)
            trainingData.append([screen, output])
            # save after every 5,000 frames
            if len(trainingData) % 5000 == 0:
                print(len(trainingData))
                np.save(fileName, trainingData)
                print('SAVED')

            #cv2.imshow('window', screen)
            #if cv2.waitKey(25) & 0xFF == ord('q'):
            #    cv2.destroyAllWindows()
            #    break

            #print('loop took {} seconds'.format(time.time() - last_time))
            last_time = time()
