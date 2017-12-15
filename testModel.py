import numpy as np
from screenShot import takeScreenShot
import cv2
from time import time, sleep
from key import PressKey, ReleaseKey, W, A, S, D, getKeys
from alexnet import alexnet2

# Press 1 to pause

width = 160
height = 120
epochs = 10
model_name = 'GTA5-NoVehicle-70k-data.model'
#model_name = 'GTA5-NoVehicles-0.001-alexnet-8-epochs-80K-data.model'
w = [1,0,0,0,0,0]
a = [0,1,0,0,0,0]
d = [0,0,1,0,0,0]
wa = [0,0,0,1,0,0]
wd = [0,0,0,0,1,0]
nk = [0,0,0,0,0,1]

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)


def forward_left():
    PressKey(W)
    PressKey(A)
    ReleaseKey(D)


def forward_right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)


def no_keys():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)


model = alexnet2(width, height, 6)
model.load(model_name)


def main():
    last_time = time()
    for i in range(1,4):
        print(4-i)
        sleep(1)

    paused = False
    while (True):

        if not paused:
            screen = takeScreenShot(region=(0, 30, 800, 630))
            print('loop took {} seconds'.format(time() - last_time))
            last_time = time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160, 120))

            prediction = model.predict([screen.reshape(160, 120, 1)])[0]
            print(prediction)

            if np.argmax(prediction) == np.argmax(w):
                straight()
            if np.argmax(prediction) == np.argmax(a):
                left()
            if np.argmax(prediction) == np.argmax(d):
                right()
            if np.argmax(prediction) == np.argmax(wa):
                forward_left()
            if np.argmax(prediction) == np.argmax(wd):
                forward_right()
            if np.argmax(prediction) == np.argmax(nk):
                no_keys()

        keys = getKeys()
        if '1' in keys:
            if paused:
                paused = False
                sleep(1)
            else:
                paused = True
                print("Paused")
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                sleep(1)


main()


