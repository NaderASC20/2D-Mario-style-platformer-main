import math, copy, os
from cmu_112_graphics import *
from threading import Thread
import threading
import cv2
import mediapipe as mp
import time
import random


####################################################################
# Map Pieces #
####################################################################

baseMap=[]
maps=[map1, map2, map3, map4, map5, map6, map7, map8, map9, map10, map11, map12,
map13, map14, map15, map16, map17, map18, map19, map20, map21, map22, map23, map24
map25, map26, map27, map28, map29, map30 ]

#Dictionary which maps a current map to a list of possbile maps
possibleMaps=dict()

####################################################################
# Model Functions #
####################################################################

def appStarted(app):
    thread = threading.Thread(target=handDetection, args=(app,))
    thread.start()
    app.rows=100
    app.cols=100
    app.cellWidth = app.width // 100
    app.cellHeight = app.height // 100
    app.board=[ ([True]*100) for row in range(app.rows)]
    for c in range(app.cols):
        app.board[95][c]=False

    app.scrollX = app.cellWidth
    app.scrollY = 0
    # Player holds the x and y coordinates of the players
    app.player = [app.width//2,0]
    app.playerJumpHeight = 20
    app.velocity=0
    app.timerDelay = 1
    app.handDetection = None
    app.platformerBackground = app.loadImage('image.png')
    app.switchMap=False
    app.mapLengthCounter=0
    app.nextMap=[]

####################################################################
# Controller Functions #
####################################################################
def playerJump(app):
    app.player[1] += app.playerJumpHeight

def checkForHandInputs(app, handDetection):
    print(handDetection)
    # if handDetection == 1:
    #     #move map to left by x pixels
    #     pass
    # elif handDetection == 2:
    #     playerJump(app)
    # elif handDetection == 3:
    #     playerDown()
    

def doGravity(app):
    app.velocity-= 2.0

def keyPressed(app):
    pass

def timerFired(app):
    doGravity(app)
    # moveMap(app)
    movePlayer(app)
    
    # if(app.switchMap=True)

def movePlayer(app):
    app.player[1]-=app.velocity
    if(app.handDetection==1):
        dash(app)
        app.handDetection=0
    elif (app.handDetection==2):
        playerJump(app)
        app.handDetection=0
    elif (app.handDetection==3):
        playerDown(app)
        app.handDetection=0

def dash(app):
    pass
def playerDown(app):
    #while player is still in the air:
    app.velocity -= 4.0

# def moveMap(app):
#     for r in range(app.rows):
#         app.board.pop(0)
#     if(len(app.nextMap)<1):
#         mapsAfter=possibleMaps[app.nextMap]
#         #Picks first element(Random element) from maps that are possible for the player
#         for nextMap in mapsAfter:
#             app.nextMap=nextMap
#             break
#     for r in range(app.rows):
#         app.board[r].append(app.nextMap[r].pop(0))

    

####################################################################
# Drawing Functions #
####################################################################

def redrawAll(app,canvas):
    drawBackground(app, canvas)
    drawMap(app, canvas)
    drawPlayer(app, canvas)


def drawBackground(app,canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.platformerBackground))
    
def drawCell(app, canvas,row,col):
    if (app.board[row][col] == True):
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill='green', width=0)

def getCellBounds(app, row, col):
    x0 = (app.cellWidth * col)
    y0 = (app.cellHeight * row)
    x1 = (app.cellWidth * (col + 1))
    y1 = (app.cellHeight * (row + 1))
    return (x0, y0, x1, y1)

def drawPlayer(app, canvas):
    canvas.create_rectangle(app.player[0]-30, app.player[1]-30, 
                           app.player[0]+30, app.player[1]+30, fill='red')

def drawMap(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col)

def checkDeltaLM(previousLMs, LM, id, delta=40):
    prevCX, prevCY = previousLMs[id]
    cx, cy = LM
    deltaX = prevCX - cx
    deltaY = prevCY- cy
    if deltaX > delta:
        print("DASH RIGHT")
        return 1
    if deltaY > delta:
        print("JUMP")
        return 2
    if deltaY < -1 * delta:
        print("STOMP")
        return 3
    return 0

#portion from: https://github.com/BakingBrains/Hand_Tracking-_Using_OpenCV/blob/main/Hand_tracking.py
def handDetection(app):
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    previousLMs = []
    start = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                newPreviousLM = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    if time.time() - start >= 1:
                        if len(previousLMs) == len(handLms.landmark):
                            dash = checkDeltaLM(previousLMs, (cx, cy), id)
                            app.handDetection = dash
                            if dash != 0:
                                start = time.time()                             
                                break
                        newPreviousLM.append((cx, cy))
                        
                    previousLMs = copy.deepcopy(newPreviousLM)

        # cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

runApp(width=1280, height=720)
