import cv2
import numpy as np
from PyQt5.QtGui import QColor


class GreenscreenColorRangeService():

    def scanImage(self,cv2Frame):
        frame = cv2.cvtColor(cv2Frame,cv2.COLOR_BGR2HSV)
        self.minCV2 = frame.min(axis=(0, 1)).astype(int)
        self.maxCV2 = frame.max(axis=(0, 1)).astype(int)
        self.averageCV2 = np.average(frame,axis=(0, 1)).astype(int)

    def getMinHSV(self):
        return self.minCV2

    def getMaxHSV(self):
        return self.maxCV2

    def getAverageHSV(self):
        return self.averageCV2

    def getMaxQColor(self):
        return self._convertCv2HsvToQColor(self.getMaxHSV())

    def getMinQColor(self):
        return self._convertCv2HsvToQColor(self.getMinHSV())

    def getAverageQColor(self):
        return self._convertCv2HsvToQColor(self.getAverageHSV())

    def _convertCv2HsvToQColor(self,cv2Hsv):
        return QColor.fromHsv(cv2Hsv[0]*2,cv2Hsv[1],cv2Hsv[2])