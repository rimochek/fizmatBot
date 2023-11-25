import logging

class SongEditor(object):
    def __init__(self, path):
        self.path = path
    
    def addSong(self, song):
        file = open(self.path, "a+")
        file.write(f"{song}\n")
        file.close()
        logging.info(f"Добавил трек: {song}")
    
    def getSongs(self):
        file = open(self.path, "r")
        songs = file.read().split("\n")
        return songs

    def deleteAllData(self):
        with open(self.path, "w") as file:
            pass
        logging.info("Удалил все треки")