"""Code to drive the Hackaday Supercon 2023 badge.
"""
import time
import array
import math

import gc9a01
from screen import Screen

# Design an involute gear. Based on https://observablehq.com/@dkirkby/gears.
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

    return Xgear, Ygear, 180 / PI * phiPitch

# Precomputed sine and cosine values for 256 steps around a circle. Values are multiplied by 128 and rounded to integers.
# I really only need a quarter cycle of one of these but the full tables save some index calculations.
C = array.array('h', [128, 128, 128, 128, 127, 127, 127, 126, 126, 125, 124, 123, 122, 122, 121, 119, 118, 117, 116, 114, 113, 111, 110, 108, 106, 105, 103, 101, 99, 97, 95, 93, 91, 88, 86, 84, 81, 79, 76, 74, 71, 68, 66, 63, 60, 58, 55, 52, 49, 46, 43, 40, 37, 34, 31, 28, 25, 22, 19, 16, 13, 9, 6, 3, 0, -3, -6, -9, -13, -16, -19, -22, -25, -28, -31, -34, -37, -40, -43, -46, -49, -52, -55, -58, -60, -63, -66, -68, -71, -74, -76, -79, -81, -84, -86, -88, -91, -93, -95, -97, -99, -101, -103, -105, -106, -108, -110, -111, -113, -114, -116, -117, -118, -119, -121, -122, -122, -123, -124, -125, -126, -126, -127, -127, -127, -128, -128, -128, -128, -128, -128, -128, -127, -127, -127, -126, -126, -125, -124, -123, -122, -122, -121, -119, -118, -117, -116, -114, -113, -111, -110, -108, -106, -105, -103, -101, -99, -97, -95, -93, -91, -88, -86, -84, -81, -79, -76, -74, -71, -68, -66, -63, -60, -58, -55, -52, -49, -46, -43, -40, -37, -34, -31, -28, -25, -22, -19, -16, -13, -9, -6, -3, 0, 3, 6, 9, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 60, 63, 66, 68, 71, 74, 76, 79, 81, 84, 86, 88, 91, 93, 95, 97, 99, 101, 103, 105, 106, 108, 110, 111, 113, 114, 116, 117, 118, 119, 121, 122, 122, 123, 124, 125, 126, 126, 127, 127, 127, 128, 128, 128])
S = array.array('h', [0, 3, 6, 9, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 60, 63, 66, 68, 71, 74, 76, 79, 81, 84, 86, 88, 91, 93, 95, 97, 99, 101, 103, 105, 106, 108, 110, 111, 113, 114, 116, 117, 118, 119, 121, 122, 122, 123, 124, 125, 126, 126, 127, 127, 127, 128, 128, 128, 128, 128, 128, 128, 127, 127, 127, 126, 126, 125, 124, 123, 122, 122, 121, 119, 118, 117, 116, 114, 113, 111, 110, 108, 106, 105, 103, 101, 99, 97, 95, 93, 91, 88, 86, 84, 81, 79, 76, 74, 71, 68, 66, 63, 60, 58, 55, 52, 49, 46, 43, 40, 37, 34, 31, 28, 25, 22, 19, 16, 13, 9, 6, 3, 0, -3, -6, -9, -13, -16, -19, -22, -25, -28, -31, -34, -37, -40, -43, -46, -49, -52, -55, -58, -60, -63, -66, -68, -71, -74, -76, -79, -81, -84, -86, -88, -91, -93, -95, -97, -99, -101, -103, -105, -106, -108, -110, -111, -113, -114, -116, -117, -118, -119, -121, -122, -122, -123, -124, -125, -126, -126, -127, -127, -127, -128, -128, -128, -128, -128, -128, -128, -127, -127, -127, -126, -126, -125, -124, -123, -122, -122, -121, -119, -118, -117, -116, -114, -113, -111, -110, -108, -106, -105, -103, -101, -99, -97, -95, -93, -91, -88, -86, -84, -81, -79, -76, -74, -71, -68, -66, -63, -60, -58, -55, -52, -49, -46, -43, -40, -37, -34, -31, -28, -25, -22, -19, -16, -13, -9, -6, -3])

# Constants for 90 phase shift in the loookup tables.
N = len(C)
M = N // 4

# Precompute a polygon approximation to the central sun gear. Values are pixel coordinates multiplied by 8 and rounded to integers.
Nsun = 12
Rsun = 65
Xsun, Ysun, phiPitchSun = makeGear(Rsun, Nsun)

# Precompute the planet gear design.
# The number of planet gear teeth must exactly divide the number of sun gear teeth
# to simplify the calculation of the offset into the C,S tables. A better solution
# would be to replace the sin,cos tables with direct calls to the math library.
Nplanet = 6
Rplanet = Rsun * Nplanet / Nsun
Xplanet, Yplanet, phiPitchPlanet = makeGear(Rplanet, Nplanet)
Rplanet = int(round(Rplanet))

# Calculate the rotations of each planet gear.
ratio = Nsun / Nplanet
def getSpin(rollDeg):
    spinDeg = rollDeg * (1 + ratio) - phiPitchSun * ratio
    spinDeg += 180 - phiPitchPlanet
    spinDeg += 2 # this is a cosmetic fudge factor
    # convert to index offset in C,S
    return int(round((spinDeg % 360) / 360 * len(C)))

spinR = getSpin(0)
spinT = getSpin(90)
spinL = getSpin(180)
spinB = getSpin(270)

screen = Screen()

# Offset from right to left or bottom to top in screen pixels.
DR = 2 * (Rsun + Rplanet)

# Center of central gear in screen pixels x 1024
xc, yc = 120 * 1024, 120 * 1024
# Center of right-side planet gear in screen pixels x 1024
xcR, ycR = (120 + Rsun + Rplanet) * 1024, 120 * 1024
# Center of lower-side planet gear in screen pixels x 1024
xcB, ycB = 120 * 1024, (120 + Rsun + Rplanet) * 1024
# Center of left-side planet gear in screen pixels x 1024
xcL, ycL = xcR - DR * 1024, ycR
# Center of top-side planet gear in screen pixels x 1024
xcT, ycT = xcB, ycB - DR * 1024

# Central sun gear is fully contained within [0,240] so only needs 1 byte per coordinate.
XPLOT = bytearray(len(Xsun))
YPLOT = bytearray(len(Ysun))
XPLOTb = bytearray(len(Xsun))
YPLOTb = bytearray(len(Ysun))

# Offset planet gears might extend beyond [0,240] so need 2 bytes per coordinate.
XPLOTR = array.array('h', [0] * len(Xplanet))
YPLOTR = array.array('h', [0] * len(Yplanet))
XPLOTB = array.array('h', [0] * len(Xplanet))
YPLOTB = array.array('h', [0] * len(Yplanet))
XPLOTL = array.array('h', [0] * len(Xplanet))
YPLOTL = array.array('h', [0] * len(Yplanet))
XPLOTT = array.array('h', [0] * len(Xplanet))
YPLOTT = array.array('h', [0] * len(Yplanet))
XPLOTRb = array.array('h', [0] * len(Xplanet))
YPLOTRb = array.array('h', [0] * len(Yplanet))
XPLOTBb = array.array('h', [0] * len(Xplanet))
YPLOTBb = array.array('h', [0] * len(Yplanet))
XPLOTLb = array.array('h', [0] * len(Xplanet))
YPLOTLb = array.array('h', [0] * len(Yplanet))
XPLOTTb = array.array('h', [0] * len(Xplanet))
YPLOTTb = array.array('h', [0] * len(Yplanet))

def visible(x, y):
    return (x >= 0 and x < 240 and y >= 0 and y < 240)

undraw = False

FG = gc9a01.GREEN
BG = gc9a01.BLACK

# Clear the screen
screen.tft.fill(BG)

iratio = int(round(ratio))

while True:
    for t in range(N):
        # Calculate the rotated gear coordinates
        c = C[t]
        s = S[t]
        for i in range(len(Xsun)):
            XPLOT[i] = (xc + c * Xsun[i] - s * Ysun[i]) >> 10
            YPLOT[i] = (yc + c * Ysun[i] + s * Xsun[i]) >> 10
        cR = C[(iratio * t + spinR) % N]
        sR = S[(iratio * t + spinR) % N]
        cT = C[(iratio * t + spinT) % N]
        sT = S[(iratio * t + spinT) % N]
        cL = C[(iratio * t + spinL) % N]
        sL = S[(iratio * t + spinL) % N]
        cB = C[(iratio * t + spinB) % N]
        sB = S[(iratio * t + spinB) % N]
        for i in range(len(Xplanet)):
            XPLOTR[i] = (xcR + cR * Xplanet[i] + sR * Yplanet[i]) >> 10
            YPLOTR[i] = (ycR + cR * Yplanet[i] - sR * Xplanet[i]) >> 10
            XPLOTB[i] = (xcB + cB * Xplanet[i] + sB * Yplanet[i]) >> 10
            YPLOTB[i] = (ycB + cB * Yplanet[i] - sB * Xplanet[i]) >> 10
            XPLOTL[i] = (xcL + cL * Xplanet[i] + sL * Yplanet[i]) >> 10
            YPLOTL[i] = (ycL + cL * Yplanet[i] - sL * Xplanet[i]) >> 10
            XPLOTT[i] = (xcT + cT * Xplanet[i] + sT * Yplanet[i]) >> 10
            YPLOTT[i] = (ycT + cT * Yplanet[i] - sT * Xplanet[i]) >> 10

        # Draw the new coordinates into an off-screen buffer
        for i in range(len(XPLOT)-1):
            if undraw:
                screen.tft.line(XPLOTb[i], YPLOTb[i], XPLOTb[i+1], YPLOTb[i+1], BG)
            screen.tft.line(XPLOT[i], YPLOT[i], XPLOT[i+1], YPLOT[i+1], FG)
        for i in range(len(XPLOTR)-1):
            if undraw:
                screen.tft.line(XPLOTRb[i], YPLOTRb[i], XPLOTRb[i+1], YPLOTRb[i+1], BG)
            if visible(XPLOTR[i], YPLOTR[i]) or visible(XPLOTR[i+1], YPLOTR[i+1]):
               screen.tft.line(XPLOTR[i], YPLOTR[i], XPLOTR[i+1], YPLOTR[i+1], FG)
        for i in range(len(XPLOTB)-1):
            if undraw:
                screen.tft.line(XPLOTBb[i], YPLOTBb[i], XPLOTBb[i+1], YPLOTBb[i+1], BG)
            if visible(XPLOTB[i], YPLOTB[i]) or visible(XPLOTB[i+1], YPLOTB[i+1]):
                screen.tft.line(XPLOTB[i], YPLOTB[i], XPLOTB[i+1], YPLOTB[i+1], FG)
        for i in range(len(XPLOTL)-1):
            if undraw:
                screen.tft.line(XPLOTLb[i], YPLOTLb[i], XPLOTLb[i+1], YPLOTLb[i+1], BG)
            if visible(XPLOTL[i], YPLOTL[i]) or visible(XPLOTL[i+1], YPLOTL[i+1]):
                screen.tft.line(XPLOTL[i], YPLOTL[i], XPLOTL[i+1], YPLOTL[i+1], FG)
        for i in range(len(XPLOTT)-1):
            if undraw:
                screen.tft.line(XPLOTTb[i], YPLOTTb[i], XPLOTTb[i+1], YPLOTTb[i+1], BG)
            if visible(XPLOTT[i], YPLOTT[i]) or visible(XPLOTT[i+1], YPLOTT[i+1]):
                screen.tft.line(XPLOTT[i], YPLOTT[i], XPLOTT[i+1], YPLOTT[i+1], FG)
        # Save coordinates of the lines just drawn so we can undraw them for the next frame
        for i in range(len(XPLOT)):
            XPLOTb[i] = XPLOT[i]
            YPLOTb[i] = YPLOT[i]
        for i in range(len(XPLOTR)):
            XPLOTRb[i] = XPLOTR[i]
            YPLOTRb[i] = YPLOTR[i]
            XPLOTBb[i] = XPLOTB[i]
            YPLOTBb[i] = YPLOTB[i]
            XPLOTLb[i] = XPLOTL[i]
            YPLOTLb[i] = YPLOTL[i]
            XPLOTTb[i] = XPLOTT[i]
            YPLOTTb[i] = YPLOTT[i]
        undraw = True
        # Pause until the next frame
        time.sleep_ms(5)
