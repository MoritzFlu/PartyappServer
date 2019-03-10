import pygame
import threading

class Player(threading.Thread):

    DB = None
    Mixer = None
    Running = True

    def __init__(self, DB):
        self.DB = DB
        self.Mixer = pygame.mixer.init()

    def run(self):

        while running:
            path = DB.fetch_next_song()

            self.Mixer.music.load(path)
            self.Mixer.music.play()
        
            while pygame.mixer.music.get_busy() == True:
                continue





