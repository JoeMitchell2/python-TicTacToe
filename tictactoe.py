#Python Demonstration: Unbeatable Tic Tac Toe
#Requires Pygame


import pygame, sys
from pygame.locals import *
from random import choice



# set win condition coordinates
class winCondition:
    winRow = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

# begin ai zerosum algorithm
    def nash(self, attachPoint, actionMarker):
        count = 0
        for mark in attachPoint:
            if mark == 0:
                count += 1
        actionMarker = -actionMarker    
        return self.algorithm(attachPoint, count, actionMarker, -1, 1)

    def algorithm(self, attachPoint, depth, actionMarker, maximizer, minimizer):
        if self.gameStatusCheck(attachPoint) or depth == 0:
            return self.ev(attachPoint)
        if actionMarker == -1:
            for child in self.children(attachPoint, actionMarker):
                minimizer = min(minimizer, self.algorithm(child, depth-1, -actionMarker, maximizer, minimizer))
                if maximizer >= minimizer:
                    return maximizer
            return minimizer
        else:
            for child in self.children(attachPoint, actionMarker):
                maximizer = max(maximizer, self.algorithm(child, depth-1, -actionMarker, maximizer, minimizer))
                if maximizer >= minimizer:
                    return minimizer
            return maximizer

    def gameStatusCheck(self, position):
        return self.win(position) or self.tie(position)

# define a "win"

    def win(self, position):
        for row in winCondition.winRow:
            if position[row[0]] == position[row[1]] == position[row[2]] and position[row[0]] != 0:
                return position[row[0]]
        return False

# define a "tie": nowhere left to move

    def tie(self, position):
        for mark in position:
            if mark == 0:
                return False
        return 2

# motivate the machine to notice if winning is possible, and go for it.

    def children(self, position, actionMarker):
        movelist = []
        for i in xrange(9):
            if position[i] == 0:
                temppos = position[:]
                temppos[i] = actionMarker
                movelist.append(temppos)
        return movelist

    def ev(self, attachPoint):
        for row in winCondition.winRow:
            if attachPoint[row[0]] == attachPoint[row[1]] == attachPoint[row[2]] and attachPoint[row[0]] != 0:
                return attachPoint[row[0]]
        return 0

    def machineMove(self, attachPoint, actionMarker):
        evaluations = []
        for child in self.children(attachPoint, actionMarker):
            evaluations.append(self.nash(child, actionMarker))
        if actionMarker == 1:
            maxv = max(evaluations)
        else:
            maxv = min(evaluations)
        possmov = []
        for i in range(len(evaluations)):
            if evaluations[i] == maxv:
                possmov.append(i)
        ind = choice(possmov)
        for i in range(len(self.children(attachPoint, actionMarker)[ind])):
            if self.children(attachPoint, actionMarker)[ind][i] != attachPoint[i]:
                return i

# define column/row boundaries, add them together, store

    def map_position(self, position):
        if position[0] < 100:
            col = 0
        elif position[0] < 200:
            col = 1
        else:
            col = 2
        if position[1] < 100:
            row = 0
        elif position[1] < 200:
            row = 3
        else:
            row = 6
        return row+col  

    def inp(self, events): 
       for event in events: 
          if event.type == QUIT: 
             sys.exit()

    def map_win(self, position):
        for row in winCondition.winRow:
            if position[row[0]] == position[row[1]] == position[row[2]] and position[row[0]] != 0:
                pygame.draw.line(self.screen, 0, self.centers[row[0]], self.centers[row[2]], 5)
            pygame.display.flip()
            pygame.display.set_caption('You have lost.')

# define menu options

    def createButton(self, text, width):
        but = pygame.surface.Surface((width, 50))
        but.fill(pygame.Color("black"))
        
        button_font = pygame.font.Font(None, 50)
        message = button_font.render(text, True, pygame.Color("red"))
        
        message_rect = message.get_rect()
        message_rect.center = (width/2, 25)
        
        but.blit(message, message_rect)
        return but

    def welcomeText(self, text, y):
        font = pygame.font.Font(None, 25)
        
        rendered = font.render(text, True, (0, 0, 0, 0))
        rendered_rect = rendered.get_rect()
        rendered_rect.y = y
        rendered_rect.centerx = 150
        
        return rendered, rendered_rect

    def playerText(self, text, y):
        font = pygame.font.Font(None, 25)
        
        rendered = font.render(text, True, (0, 0, 0, 0))
        rendered_rect = rendered.get_rect()
        rendered_rect.y = y
        rendered_rect.centerx = 50
        
        return rendered, rendered_rect

    def menu(self):
        firstPlayerButton = self.createButton("X", 100)
        secondPlayerButton = self.createButton("O", 100)        
        tx = pygame.font.SysFont("Helvetica, FreeSans", 14, True, False)

        introduction1, introduction1_rect = self.welcomeText("Tic-Tac-Toe", 25)
        introduction2, introduction2_rect = self.welcomeText("Choose play symbol:", 75)
        introduction3, introduction3_rect = self.playerText("Player 1", 100)
        introduction4, introduction4_rect = self.playerText("Player 2", 200)



        self.screen.blit(introduction1, introduction1_rect)
        self.screen.blit(introduction2, introduction2_rect)
        self.screen.blit(introduction3, introduction3_rect)
        self.screen.blit(introduction4, introduction4_rect)



        firstPlayerButton_rect = firstPlayerButton.get_rect()
        (firstPlayerButton_rect.x, firstPlayerButton_rect.y) = (180, 100)

        secondPlayerButton_rect = secondPlayerButton.get_rect()
        (secondPlayerButton_rect.x, secondPlayerButton_rect.y) = (180, 200)

        self.screen.blit(firstPlayerButton, firstPlayerButton_rect)
        self.screen.blit(secondPlayerButton, secondPlayerButton_rect)

        button_rects = [(firstPlayerButton_rect, 1), (secondPlayerButton_rect, -1)]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    for button_rect in button_rects:
                        if button_rect[0].collidepoint(*event.pos):
                            pygame.time.wait(250)
                            return button_rect[1]

# draw marker symbols

    def draw(self, mark, actionMarker):
        if actionMarker == 1:
                center = self.centers[mark]
                topLeft = (center[0] - 50, center[1] - 50)
                bottomRight = (center[0] + 50, center[1] + 50)
                bottomLeft = (center[0] - 50, center[1] + 50)
                topRight = (center[0] + 50, center[1] - 50)
                pygame.draw.line(self.screen, 0xFF0000, topLeft, bottomRight, 3)
                pygame.draw.line(self.screen, 0xFF0000, topRight, bottomLeft, 3)
        else:
            pygame.draw.circle(self.screen, 0xFF0000, self.centers[mark], 45, 2)
        pygame.display.flip()

# turn protocol

    def getMove(self, player):
        if player == "machine":
            piece = -self.actionMarker
            AImove = self.machineMove(self.gameSurface, piece)
            return AImove, piece
        else:
            piece = self.actionMarker
            while True:
                self.inp(pygame.event.get())
                if 1 in pygame.mouse.get_pressed():
                    position = pygame.mouse.get_pos()
                    mark = self.map_position(position)
                    if self.gameSurface[mark] == 0:
                        return mark, piece


    def makeMove(self, mark, piece):
        self.gameSurface[mark] = piece
        self.draw(mark, piece)

    def move(self, player):
        self.makeMove( *self.getMove(player) )

    def gameEnd(self):
        if self.win(self.gameSurface):
            self.map_win(self.gameSurface)
            while 1:
                self.inp(pygame.event.get())
        elif self.tie(self.gameSurface):
            pygame.display.set_caption('The match ends in a tie.')
            pygame.display.flip()
            while 1:
                self.inp(pygame.event.get())

# define UI window
                
    def main(self):
        pygame.init()
        pygame.display.set_caption('Man Versus Machine') 
        self.screen = pygame.display.set_mode((300, 300))
        self.screen.fill(0xDDDDDD)

# initialize program variables
        self.gameSurface = [0] * 9
        self.centers = {0:(50, 50), 1:(150, 50), 2:(250, 50), 3:(50, 150), 4:(150, 150), 5:(250, 150), 6:(50, 250), 7:(150, 250), 8:(250, 250)}

        self.choice = self.menu()
        if self.choice in (-1, 1):
            self.actionMarker = self.choice
            self.protocol()

# draw the gamespace
    def renderGamespace(self):
        self.screen.fill(0xDDDDDD)
        pygame.draw.line(self.screen, 0, (100, 0), (100, 300), 3)
        pygame.draw.line(self.screen, 0, (200, 0), (200, 300), 3)
        pygame.draw.line(self.screen, 0, (0, 100), (300, 100), 3)
        pygame.draw.line(self.screen, 0, (0, 200), (300, 200), 3)
        pygame.display.flip()

# put it all together

    def protocol(self):
        self.renderGamespace()
        if self.actionMarker == -1:
            self.move("machine")
        while True:
            self.move("human")
            self.gameEnd()
            self.move("machine")
            self.gameEnd()

if __name__ == "__main__":
    winCondition().main()

