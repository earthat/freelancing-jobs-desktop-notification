import pyautogui as pg
import win32api


def checkClickLocation():

    rect=[1224,1031] # mouse click rectangle [(1224,943),(1918,943),(1918,1031),(1224,1031)]
    _, width = pg.size()  # screen size
    minY=943/width
    # #normalize the values
    rect=normalize(points=rect)
    #a = win32api.GetAsyncKeyState(0x01)  # initial left mouse state =0(not pressed)
    #print(a)
    mouseX, mouseY = pg.position()  # grab mouse location co-ordinates
    # normalize the values
    points = normalize([mouseX, mouseY])
    mouseX = points[0]
    mouseY = points[1]

    if (mouseX > rect[0]) & (mouseY < rect[1]) & (mouseY > minY):
        return True
    else:
        return False



def normalize(points):
    height, width = pg.size()  # screen size
    points[0] = points[0] / height
    points[1] = points[1] / width
    return points

