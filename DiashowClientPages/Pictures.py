import random

from DiashowClientPages.Picture import Picture


class Pictures():

    def __init__(self):
        self.default = []
        self.pictures = []

    def addDefault(self,default:Picture):
        self.default.extend(default)

    def add(self,picture:Picture):
        self.pictures.extend(picture)

    def _get(self):
        if not self.pictures:
            return self.default
        else:
            return self.pictures

    def existPictures(self) -> bool:
        return len(self._get()) > 0

    def getRandomPicture(self) -> Picture:
        pictures =  self._get()
        if len(pictures) != 0:
            numberPictures = len(pictures)
            pictureIndex = random.randint(0,numberPictures-1)
            return pictures[pictureIndex]
        return None