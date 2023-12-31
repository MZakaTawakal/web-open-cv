import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

pygame.init()


class Balloon:
    def __init__(self, img, position, size, speed):
        self.img = pygame.image.load(img).convert_alpha()
        self.position = position
        self.size = size
        self.rect = self.img.get_rect()
        self.speed = speed


width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Popper")

fps = 30
clock = pygame.time.Clock()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

balloons = [
    Balloon(
        img='Balon.png',
        position=(500, 300),
        size=1,
        speed=15,
    ),
    Balloon(
        img='balon1.png',
        position=(500, 300),
        size=1,
        speed=10,
    )
]

score = 0
startTime = time.time()
totalTime = 30
detector = HandDetector(detectionCon=0.8, maxHands=2)


def resetBalloon(balloon):
    balloon.rect.x = random.randint(width // 10, width // 2)
    balloon.rect.y = random.randint(height // 10, height // 2)


start = True
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    timeRemain = int(totalTime - (time.time() - startTime))

    if timeRemain < 0:
        window.fill((255, 255, 255))
        font = pygame.font.Font('Marcellus-Regular.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Finish', True, (50, 50, 255))
        textTitle = font.render(f'Balloon Popper', True, (50, 50, 255))
        window.blit(textTitle, (490, 35))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (530, 275))
    else:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))

        for balloon in balloons:

            balloon.rect.y -= balloon.speed

            if balloon.rect.y < 0:
                resetBalloon(balloon)
                balloon.speed += 1

            if hands:
                hand = hands[0]
                x, y = hand['lmList'][8][0:2]
                if balloon.rect.collidepoint(x, y):
                    resetBalloon(balloon)
                    score += 10
                    balloon.speed += 1

            window.blit(balloon.img, balloon.rect)

        font = pygame.font.Font('Marcellus-Regular.ttf', 50)
        textScore = font.render(f'Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
        textTitle = font.render(f'Balloon Popper', True, (50, 50, 255))
        window.blit(textTitle, (490, 35))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1000, 35))

    pygame.display.update()
    clock.tick(fps)