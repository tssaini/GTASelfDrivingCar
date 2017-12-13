import win32gui, win32ui, win32con
import numpy as np
import cv2
import time

def takeScreenShot(region=None):
    w=800
    h=600

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1

    hwnd = win32gui.GetDesktopWindow()
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (left, top), win32con.SRCCOPY)

    #dataBitMap.SaveBitmapFile(cDC, "test.bmp")

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

if __name__ == "__main__":
    last_time = time.time()
    while(True):
        #sleep(1)
        screen = takeScreenShot(region=(0,30,800,620))
        #screen = cv2.resize(screen, (480, 270))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        cv2.imshow('window', screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

