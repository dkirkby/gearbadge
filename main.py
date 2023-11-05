import time
import array
import math

import gc9a01
from screen import Screen

def makeGear(radius, nteeth, pressureAngleDeg=20, clearanceFraction=0.25, npath=6, mult=8):

    PI = math.pi

    module = 2 * radius / nteeth
    pitchRadius = module * nteeth / 2
    baseRadius = pitchRadius * math.cos(PI / 180 * pressureAngleDeg)
    addendumRadius = pitchRadius + module
    dedendumRadius = pitchRadius - (1 + clearanceFraction) * module

    def t2xy(t):
        C, S = math.cos(t), math.sin(t)
        return baseRadius * (C + t * S), baseRadius * (S - t * C)

    r2t = lambda r : math.sqrt((r / baseRadius) ** 2 - 1)

    # Calculate points along the involute curve for one side of one tooth.
    tmin = r2t(max(baseRadius, dedendumRadius))
    tmax = r2t(addendumRadius)
    dt = (tmax - tmin) / (npath - 1)
    X, Y = [ ], [ ]
    for i in range(npath):
        t = tmin + i * dt
        x, y = t2xy(t)
        X.append(x)
        Y.append(y)
    if baseRadius > dedendumRadius:
        # Tooth is undercut. Do a simple approximation here.
        ratio = dedendumRadius / baseRadius
        X.insert(0, ratio * X[0])
        Y.insert(0, ratio * Y[0])

    # Locate the other side of the first tooth.
    tpitch = r2t(pitchRadius)
    Xpitch, Ypitch = t2xy(tpitch)
    phiPitch = math.atan2(Ypitch, Xpitch)
    phiOffset = PI / nteeth + 2 * phiPitch

    NX = len(X)
    Xgear, Ygear = [ ], [ ]
    for tooth in range(nteeth):

        phi = 2 * PI * tooth / nteeth
        C, S = math.cos(phi), math.sin(phi)
        for i in range(NX):
            x, y = X[i], Y[i]
            Xgear.append(C * x - S * y)
            Ygear.append(S * x + C * y)

        phi += phiOffset
        C, S = math.cos(phi), math.sin(phi)
        for i in range(NX):
            x, y = X[NX - 1 - i], Y[NX - 1 - i]
            Xgear.append(C * x + S * y)
            Ygear.append(S * x - C * y)

    Xgear.append(Xgear[0])
    Ygear.append(Ygear[0])

    for i in range(len(Xgear)):
        Xgear[i] = int(round(Xgear[i] * mult))
        Ygear[i] = int(round(Ygear[i] * mult))

    Xgear = array.array('h', Xgear)
    Ygear = array.array('h', Ygear)

    return Xgear, Ygear

# Precomputed sine and cosine values for 256 steps around a circle. Values are multiplied by 128 and rounded to integers.
# I really only need a quarter cycle of one of these but the full tables save some index calculations.
C = array.array('h', [128, 128, 128, 128, 127, 127, 127, 126, 126, 125, 124, 123, 122, 122, 121, 119, 118, 117, 116, 114, 113, 111, 110, 108, 106, 105, 103, 101, 99, 97, 95, 93, 91, 88, 86, 84, 81, 79, 76, 74, 71, 68, 66, 63, 60, 58, 55, 52, 49, 46, 43, 40, 37, 34, 31, 28, 25, 22, 19, 16, 13, 9, 6, 3, 0, -3, -6, -9, -13, -16, -19, -22, -25, -28, -31, -34, -37, -40, -43, -46, -49, -52, -55, -58, -60, -63, -66, -68, -71, -74, -76, -79, -81, -84, -86, -88, -91, -93, -95, -97, -99, -101, -103, -105, -106, -108, -110, -111, -113, -114, -116, -117, -118, -119, -121, -122, -122, -123, -124, -125, -126, -126, -127, -127, -127, -128, -128, -128, -128, -128, -128, -128, -127, -127, -127, -126, -126, -125, -124, -123, -122, -122, -121, -119, -118, -117, -116, -114, -113, -111, -110, -108, -106, -105, -103, -101, -99, -97, -95, -93, -91, -88, -86, -84, -81, -79, -76, -74, -71, -68, -66, -63, -60, -58, -55, -52, -49, -46, -43, -40, -37, -34, -31, -28, -25, -22, -19, -16, -13, -9, -6, -3, 0, 3, 6, 9, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 60, 63, 66, 68, 71, 74, 76, 79, 81, 84, 86, 88, 91, 93, 95, 97, 99, 101, 103, 105, 106, 108, 110, 111, 113, 114, 116, 117, 118, 119, 121, 122, 122, 123, 124, 125, 126, 126, 127, 127, 127, 128, 128, 128])
S = array.array('h', [0, 3, 6, 9, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 60, 63, 66, 68, 71, 74, 76, 79, 81, 84, 86, 88, 91, 93, 95, 97, 99, 101, 103, 105, 106, 108, 110, 111, 113, 114, 116, 117, 118, 119, 121, 122, 122, 123, 124, 125, 126, 126, 127, 127, 127, 128, 128, 128, 128, 128, 128, 128, 127, 127, 127, 126, 126, 125, 124, 123, 122, 122, 121, 119, 118, 117, 116, 114, 113, 111, 110, 108, 106, 105, 103, 101, 99, 97, 95, 93, 91, 88, 86, 84, 81, 79, 76, 74, 71, 68, 66, 63, 60, 58, 55, 52, 49, 46, 43, 40, 37, 34, 31, 28, 25, 22, 19, 16, 13, 9, 6, 3, 0, -3, -6, -9, -13, -16, -19, -22, -25, -28, -31, -34, -37, -40, -43, -46, -49, -52, -55, -58, -60, -63, -66, -68, -71, -74, -76, -79, -81, -84, -86, -88, -91, -93, -95, -97, -99, -101, -103, -105, -106, -108, -110, -111, -113, -114, -116, -117, -118, -119, -121, -122, -122, -123, -124, -125, -126, -126, -127, -127, -127, -128, -128, -128, -128, -128, -128, -128, -127, -127, -127, -126, -126, -125, -124, -123, -122, -122, -121, -119, -118, -117, -116, -114, -113, -111, -110, -108, -106, -105, -103, -101, -99, -97, -95, -93, -91, -88, -86, -84, -81, -79, -76, -74, -71, -68, -66, -63, -60, -58, -55, -52, -49, -46, -43, -40, -37, -34, -31, -28, -25, -22, -19, -16, -13, -9, -6, -3])

# Precompute a polygon approximation to the central sun gear. Values are pixel coordinates multiplied by 8 and rounded to integers.
Rsun = 70
Nsun = 12
X, Y = makeGear(Rsun, Nsun)

screen = Screen()

DR = 4 * Rsun
xc1, yc1 = 120 * 1024, 120 * 1024
xc2, yc2 = (120 + 2 * Rsun) * 1024, 120 * 1024
xc3, yc3 = 120 * 1024, (120 + 2 * Rsun) * 1024

XPLOT1 = bytearray(len(X))
YPLOT1 = bytearray(len(Y))
XPLOT1b = bytearray(len(X))
YPLOT1b = bytearray(len(Y))

XPLOT2 = array.array('h', [0] * len(X))
YPLOT2 = array.array('h', [0] * len(Y))
XPLOT3 = array.array('h', [0] * len(X))
YPLOT3 = array.array('h', [0] * len(Y))
XPLOT2b = array.array('h', [0] * len(X))
YPLOT2b = array.array('h', [0] * len(Y))
XPLOT3b = array.array('h', [0] * len(X))
YPLOT3b = array.array('h', [0] * len(Y))

N = len(C)
M = N // 4

def visible(x, y):
    return (x >= 0 and x < 240 and y >= 0 and y < 240)

undraw = False

FG = gc9a01.BLUE
BG = gc9a01.WHITE

# Clear the screen
screen.tft.fill(BG)

while True:
    for t in range(N):
        # Calculate the rotated gear coordinates
        c = C[t]
        s = S[t]
        c3 = C[(t + M) % N]
        s3 = S[(t + M) % N]
        for i in range(len(X)):
            XPLOT1[i] = (xc1 + c * X[i] - s * Y[i]) >> 10
            YPLOT1[i] = (yc1 + c * Y[i] + s * X[i]) >> 10
            XPLOT2[i] = (xc2 + c * X[i] + s * Y[i]) >> 10
            YPLOT2[i] = (yc2 + c * Y[i] - s * X[i]) >> 10
            XPLOT3[i] = (xc3 + c3 * X[i] + s3 * Y[i]) >> 10
            YPLOT3[i] = (yc3 + c3 * Y[i] - s3 * X[i]) >> 10

        # Draw the new coordinates into an off-screen buffer
        for i in range(len(XPLOT1)-1):
            if undraw:
                screen.tft.line(XPLOT1b[i], YPLOT1b[i], XPLOT1b[i+1], YPLOT1b[i+1], BG)
            screen.tft.line(XPLOT1[i], YPLOT1[i], XPLOT1[i+1], YPLOT1[i+1], FG)
        for i in range(len(XPLOT2)-1):
            if undraw:
                screen.tft.line(XPLOT2b[i], YPLOT2b[i], XPLOT2b[i+1], YPLOT2b[i+1], BG)
            if visible(XPLOT1[i], YPLOT1[i]) or visible(XPLOT1[i+1], YPLOT1[i+1]):
               screen.tft.line(XPLOT2[i], YPLOT2[i], XPLOT2[i+1], YPLOT2[i+1], FG)
        for i in range(len(XPLOT2)-1):
            if undraw:
                screen.tft.line(XPLOT2b[i] - DR, YPLOT2b[i], XPLOT2b[i+1] - DR, YPLOT2b[i+1], BG)
            if visible(XPLOT2[i] - DR, YPLOT2[i]) or visible(XPLOT2[i+1] - DR, YPLOT2[i+1]):
                screen.tft.line(XPLOT2[i] - DR, YPLOT2[i], XPLOT2[i+1] - DR, YPLOT2[i+1], FG)
        for i in range(len(XPLOT3)-1):
            if undraw:
                screen.tft.line(XPLOT3b[i], YPLOT3b[i], XPLOT3b[i+1], YPLOT3b[i+1], BG)
            if visible(XPLOT3[i], YPLOT3[i]) or visible(XPLOT3[i+1], YPLOT3[i+1]):
                screen.tft.line(XPLOT3[i], YPLOT3[i], XPLOT3[i+1], YPLOT3[i+1], FG)
        for i in range(len(XPLOT3)-1):
            if undraw:
                screen.tft.line(XPLOT3b[i], YPLOT3b[i] - DR, XPLOT3b[i+1], YPLOT3b[i+1] - DR, BG)
            if visible(XPLOT3[i], YPLOT3[i] - DR) or visible(XPLOT3[i+1], YPLOT3[i+1] - DR):
                screen.tft.line(XPLOT3[i], YPLOT3[i] - DR, XPLOT3[i+1], YPLOT3[i+1] - DR, FG)
        # Save coordinates of the lines just drawn so we can undraw them for the next frame
        for i in range(len(XPLOT1)):
            XPLOT1b[i] = XPLOT1[i]
            YPLOT1b[i] = YPLOT1[i]
            XPLOT2b[i] = XPLOT2[i]
            YPLOT2b[i] = YPLOT2[i]
            XPLOT3b[i] = XPLOT3[i]
            YPLOT3b[i] = YPLOT3[i]
        undraw = True
        # Pause until the next frame
        time.sleep_ms(5)
