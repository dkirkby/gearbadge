import time
import array

import gc9a01
from screen import Screen

# The buffer below is required for offscreen rendering but does not fit in the Pico RAM
#buffer = array.array('H', [0] * size * size)

X = array.array('h', [443, 526, 532, 549, 575, 610, 650, 642, 594, 555, 527, 510, 504, 425, 384, 456, 460, 473, 491, 511, 530, 494, 443, 405, 379, 365, 361, 304, 222, 263, 265, 270, 275, 275, 268, 214, 174, 147, 130, 123, 121, 102, 0, 0, -1, -4, -15, -35, -66, -123, -142, -151, -153, -152, -151, -127, -222, -263, -266, -278, -300, -335, -382, -428, -420, -408, -396, -387, -383, -323, -384, -456, -461, -477, -505, -545, -596, -617, -585, -556, -533, -518, -512, -431, -443, -526, -532, -549, -575, -610, -650, -642, -594, -555, -527, -510, -504, -425, -384, -456, -460, -473, -491, -511, -530, -494, -443, -405, -379, -365, -361, -304, -222, -263, -265, -270, -275, -275, -268, -214, -174, -147, -130, -123, -121, -102, 0, 0, 1, 4, 15, 35, 66, 123, 142, 151, 153, 152, 151, 127, 222, 263, 266, 278, 300, 335, 382, 428, 420, 408, 396, 387, 383, 323, 384, 456, 461, 477, 505, 545, 596, 617, 585, 556, 533, 518, 512, 431, 443])
Y = array.array('h', [0, 0, 1, 4, 15, 35, 66, 123, 142, 151, 153, 152, 151, 127, 222, 263, 266, 278, 300, 335, 382, 428, 420, 408, 396, 387, 383, 323, 384, 456, 461, 477, 505, 545, 596, 617, 585, 556, 533, 518, 512, 431, 443, 526, 532, 549, 575, 610, 650, 642, 594, 555, 527, 510, 504, 425, 384, 456, 460, 473, 491, 511, 530, 494, 443, 405, 379, 365, 361, 304, 222, 263, 265, 270, 275, 275, 268, 214, 174, 147, 130, 123, 121, 102, 0, 0, -1, -4, -15, -35, -66, -123, -142, -151, -153, -152, -151, -127, -222, -263, -266, -278, -300, -335, -382, -428, -420, -408, -396, -387, -383, -323, -384, -456, -461, -477, -505, -545, -596, -617, -585, -556, -533, -518, -512, -431, -443, -526, -532, -549, -575, -610, -650, -642, -594, -555, -527, -510, -504, -425, -384, -456, -460, -473, -491, -511, -530, -494, -443, -405, -379, -365, -361, -304, -222, -263, -265, -270, -275, -275, -268, -214, -174, -147, -130, -123, -121, -102, 0])
C = array.array('h', [128, 128, 128, 128, 127, 127, 127, 126, 126, 125, 124, 123, 122, 122, 121, 119, 118, 117, 116, 114, 113, 111, 110, 108, 106, 105, 103, 101, 99, 97, 95, 93, 91, 88, 86, 84, 81, 79, 76, 74, 71, 68, 66, 63, 60, 58, 55, 52, 49, 46, 43, 40, 37, 34, 31, 28, 25, 22, 19, 16, 13, 9, 6, 3, 0, -3, -6, -9, -13, -16, -19, -22, -25, -28, -31, -34, -37, -40, -43, -46, -49, -52, -55, -58, -60, -63, -66, -68, -71, -74, -76, -79, -81, -84, -86, -88, -91, -93, -95, -97, -99, -101, -103, -105, -106, -108, -110, -111, -113, -114, -116, -117, -118, -119, -121, -122, -122, -123, -124, -125, -126, -126, -127, -127, -127, -128, -128, -128, -128, -128, -128, -128, -127, -127, -127, -126, -126, -125, -124, -123, -122, -122, -121, -119, -118, -117, -116, -114, -113, -111, -110, -108, -106, -105, -103, -101, -99, -97, -95, -93, -91, -88, -86, -84, -81, -79, -76, -74, -71, -68, -66, -63, -60, -58, -55, -52, -49, -46, -43, -40, -37, -34, -31, -28, -25, -22, -19, -16, -13, -9, -6, -3, 0, 3, 6, 9, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 60, 63, 66, 68, 71, 74, 76, 79, 81, 84, 86, 88, 91, 93, 95, 97, 99, 101, 103, 105, 106, 108, 110, 111, 113, 114, 116, 117, 118, 119, 121, 122, 122, 123, 124, 125, 126, 126, 127, 127, 127, 128, 128, 128])
S = array.array('h', [0, 3, 6, 9, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 60, 63, 66, 68, 71, 74, 76, 79, 81, 84, 86, 88, 91, 93, 95, 97, 99, 101, 103, 105, 106, 108, 110, 111, 113, 114, 116, 117, 118, 119, 121, 122, 122, 123, 124, 125, 126, 126, 127, 127, 127, 128, 128, 128, 128, 128, 128, 128, 127, 127, 127, 126, 126, 125, 124, 123, 122, 122, 121, 119, 118, 117, 116, 114, 113, 111, 110, 108, 106, 105, 103, 101, 99, 97, 95, 93, 91, 88, 86, 84, 81, 79, 76, 74, 71, 68, 66, 63, 60, 58, 55, 52, 49, 46, 43, 40, 37, 34, 31, 28, 25, 22, 19, 16, 13, 9, 6, 3, 0, -3, -6, -9, -13, -16, -19, -22, -25, -28, -31, -34, -37, -40, -43, -46, -49, -52, -55, -58, -60, -63, -66, -68, -71, -74, -76, -79, -81, -84, -86, -88, -91, -93, -95, -97, -99, -101, -103, -105, -106, -108, -110, -111, -113, -114, -116, -117, -118, -119, -121, -122, -122, -123, -124, -125, -126, -126, -127, -127, -127, -128, -128, -128, -128, -128, -128, -128, -127, -127, -127, -126, -126, -125, -124, -123, -122, -122, -121, -119, -118, -117, -116, -114, -113, -111, -110, -108, -106, -105, -103, -101, -99, -97, -95, -93, -91, -88, -86, -84, -81, -79, -76, -74, -71, -68, -66, -63, -60, -58, -55, -52, -49, -46, -43, -40, -37, -34, -31, -28, -25, -22, -19, -16, -13, -9, -6, -3])
R = 70

DR = 4 * R

screen = Screen()

xc1, yc1 = 120 * 1024, 120 * 1024
xc2, yc2 = (120 + 2 * R) * 1024, 120 * 1024
xc3, yc3 = 120 * 1024, (120 + 2 * R) * 1024

XPLOT1 = array.array('h', [0] * len(X))
YPLOT1 = array.array('h', [0] * len(Y))
XPLOT1b = array.array('h', [0] * len(X))
YPLOT1b = array.array('h', [0] * len(Y))
XPLOT2 = array.array('h', [0] * len(X))
YPLOT2 = array.array('h', [0] * len(Y))
XPLOT2b = array.array('h', [0] * len(X))
YPLOT2b = array.array('h', [0] * len(Y))
XPLOT3 = array.array('h', [0] * len(X))
YPLOT3 = array.array('h', [0] * len(Y))
XPLOT3b = array.array('h', [0] * len(X))
YPLOT3b = array.array('h', [0] * len(Y))

N = len(C)
M = N // 4

def visible(x, y):
    return (x >= 0 and x < 240 and y >= 0 and y < 240)

'''
size = 240
bitarray = bytearray(size * size // 8)

def clearBuffer():
    for i in range(len(bitarray)):
        bitarray[i] = 0

def setPixel(x, y):
    idx = y * size + x
    bitarray[idx >> 3] |= 1 << (idx % 8)

# https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
def drawLine(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy
    while True:
        setPixel(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error += dy
            x0 += sx
        if e2 <= dx:
            if y0 == y1:
                break
            error += dx
            y0 += sy
'''

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

        # Clear the screen
        #screen.tft.fill(gc9a01.WHITE)
        #clearBuffer()
        # Draw the new coordinates into an off-screen buffer
        for i in range(len(XPLOT1)-1):
            ##drawLine(XPLOT1[i], YPLOT1[i], XPLOT1[i+1], YPLOT1[i+1])
            if undraw:
                screen.tft.line(XPLOT1b[i], YPLOT1b[i], XPLOT1b[i+1], YPLOT1b[i+1], BG)
            screen.tft.line(XPLOT1[i], YPLOT1[i], XPLOT1[i+1], YPLOT1[i+1], FG)
        for i in range(len(XPLOT2)-1):
            if undraw:
                screen.tft.line(XPLOT2b[i], YPLOT2b[i], XPLOT2b[i+1], YPLOT2b[i+1], BG)
            if visible(XPLOT1[i], YPLOT1[i]) or visible(XPLOT1[i+1], YPLOT1[i+1]):
               screen.tft.line(XPLOT2[i], YPLOT2[i], XPLOT2[i+1], YPLOT2[i+1], FG)
               ##drawLine(XPLOT2[i], YPLOT2[i], XPLOT2[i+1], YPLOT2[i+1])
        for i in range(len(XPLOT2)-1):
            if undraw:
                screen.tft.line(XPLOT2b[i] - DR, YPLOT2b[i], XPLOT2b[i+1] - DR, YPLOT2b[i+1], BG)
            if visible(XPLOT2[i] - DR, YPLOT2[i]) or visible(XPLOT2[i+1] - DR, YPLOT2[i+1]):
                screen.tft.line(XPLOT2[i] - DR, YPLOT2[i], XPLOT2[i+1] - DR, YPLOT2[i+1], FG)
                ##drawLine(XPLOT2[i] - DR, YPLOT2[i], XPLOT2[i+1] - DR, YPLOT2[i+1])
        for i in range(len(XPLOT3)-1):
            if undraw:
                screen.tft.line(XPLOT3b[i], YPLOT3b[i], XPLOT3b[i+1], YPLOT3b[i+1], BG)
            if visible(XPLOT3[i], YPLOT3[i]) or visible(XPLOT3[i+1], YPLOT3[i+1]):
                screen.tft.line(XPLOT3[i], YPLOT3[i], XPLOT3[i+1], YPLOT3[i+1], FG)
                ##drawLine(XPLOT3[i], YPLOT3[i], XPLOT3[i+1], YPLOT3[i+1])
        for i in range(len(XPLOT3)-1):
            if undraw:
                screen.tft.line(XPLOT3b[i], YPLOT3b[i] - DR, XPLOT3b[i+1], YPLOT3b[i+1] - DR, BG)
            if visible(XPLOT3[i], YPLOT3[i] - DR) or visible(XPLOT3[i+1], YPLOT3[i+1] - DR):
                screen.tft.line(XPLOT3[i], YPLOT3[i] - DR, XPLOT3[i+1], YPLOT3[i+1] - DR, FG)
        # Blit the off-screen buffer to the screen
        ##screen.tft.map_bitarray_to_rgb565(bitarray, buffer, gc9a01.WHITE, gc9a01.BLACK)
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
