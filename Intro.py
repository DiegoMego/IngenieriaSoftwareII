import pygame as pg
from os import path
from settings import *
from spritesheet import *
from Tutorial import *

class Intro:
    def __init__(self):
        self.image_folder, self.image_file = "Background", "Background.jpg"
        self.spritesheet = SpriteSheet(self.image_folder, self.image_file)
        self.image = pg.transform.scale(self.spritesheet.image, (WIDTH, HEIGHT))
        self.image_rect = self.image.get_rect()
        self.done = {"Game": False,
                     "Tutorial": False,
                     "Salir": False}

    def load_buttons(self):
        self.buttons = {"Game": Button("Nueva Partida"),
                        "Tutorial": Button("Tutorial"),
                        "Salir": Button("Salir")}
        x = WIDTH / 2
        y = 0.2
        for button in self.buttons:
            button.set_pos(x, HEIGHT * y)
            y += 0.25

    def events(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        for key, button in self.buttons.items():
            if button.clicked:
                self.done[key] = True

    def update(self):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        for key, button in self.buttons.items():
            button.update(mouse, click)

    def draw(self, screen):
        screen.fill(WHITE)
        for key, button in self.button.items():
            screen.blit(button.surface, button.rect)

class Button:
    def __init__(self, text):
        self.font = pg.font.SysFont("Arial", 25)
        self.text = self.font.render(text, True, WHITE)
        self.textrect = self.text.get_rect()
        self.width = WIDTH * 0.2
        self.height = HEIGHT * 0.1
        self.surface = pg.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()

    def load_text(self):
        self.textrect.center = self.rect.center

    def color(self, color):
        self.rect.fill(color)
        self.rect.blit(self.text, self.textrect)

    def set_pos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.load_text()

    def update(self, mouse, click):
        self.clicked = False
        if self.rect.left <= mouse[0] <= self.rect.right and self.rect.top <= mouse[1] <= self.rect.bottom:
            self.color(DOWN_RED)
            if click[0] == 1:
                self.clicked = True
        else:
            self.color(LIGHT_BLACK)

def Intro(self):

    img_dir = path.join(game_folder, "img")

    clock = pg.time.Clock()

    #font = pg.font.SysFont("Arial", 35)
    GameDisplay = pg.display.set_mode((WIDTH, HEIGHT))
    background = pg.image.load(path.join(img_dir, "background.jpg")).convert()
    background = pg.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    #img_dir = path.join(game_folder, "img")

    titu = pg.image.load(path.join(img_dir, "logo1.png")).convert()
    titu.set_colorkey(BLACK)
    #titu = pg.transform.scale(titu, (WIDTH, HEIGHT))
    titu_rect = titu.get_rect()
    #titu.rect.top

    def text_button(text, font, color):
        textbutton = font.render(text, True, color)
        return textbutton, textbutton.get_rect()

    def button_iniciar(x, y, width, height, text, events, hover_color, color):
        #Getting mouse position
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        #Creating the button
        r = pg.Rect(x, y, width, height)
        r.center = (x/2, y/2)
        #If mouse is hovering the button, light it up
        if r.x <= mouse[0] <= r.x + width and r.y <= mouse[1] <= r.y + height:
            pg.draw.rect(GameDisplay, hover_color, r)
            if click[0] == 1:
                self.run()
        else:
            pg.draw.rect(GameDisplay, color, r)

        #Creating text for the button
        font = pg.font.SysFont("Arial", 25)
        textbutton, textrect = text_button(text, font, WHITE)
        #Centering text
        textrect.center = (r.x + (width/2), r.y + (height/2))

        GameDisplay.blit(textbutton, textrect)


    def button_tutorial(x, y, width, height, text, events, hover_color, color):
        #Getting mouse position
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        #Creating the button
        r = pg.Rect(x, y, width, height)
        r.center = (x/2, y/1.5)
        #If mouse is hovering the button, light it up
        if r.x <= mouse[0] <= r.x + width and r.y <= mouse[1] <= r.y + height:
            pg.draw.rect(GameDisplay, hover_color, r)
            if click[0] == 1:
                tutorial()
        else:
            pg.draw.rect(GameDisplay, color, r)

        #Creating text for the button
        font = pg.font.SysFont("Arial", 25)
        textbutton, textrect = text_button(text, font, WHITE)
        #Centering text
        textrect.center = (r.x + (width/2), r.y + (height/2))

        GameDisplay.blit(textbutton, textrect)

    def button_salir(x, y, width, height, text, events, hover_color, color):
        #Getting mouse position
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        #Creating the button
        r = pg.Rect(x, y, width, height)
        r.center = (x/2, y/1.2)
        #If mouse is hovering the button, light it up
        if r.x <= mouse[0] <= r.x + width and r.y <= mouse[1] <= r.y + height:
            pg.draw.rect(GameDisplay, hover_color, r)
            if click[0] == 1:
                pg.quit()
                quit()
        else:
            pg.draw.rect(GameDisplay, color, r)

        #Creating text for the button
        font = pg.font.SysFont("Arial", 25)
        textbutton, textrect = text_button(text, font, WHITE)
        #Centering text
        textrect.center = (r.x + (width/2), r.y + (height/2))

        GameDisplay.blit(textbutton, textrect)


    done = False

    while not done:

        events = pg.event.get()
        mouse = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                quit()


        GameDisplay.fill(WHITE)
        GameDisplay.blit(background, background_rect)
        GameDisplay.blit(titu, titu_rect)
        #button(x, y, width, height, text, event, hover_color, color)
        button_iniciar(WIDTH, HEIGHT, 150, 50, "Nueva Partida", events, DOWN_RED, LIGHT_BLACK)
        button_tutorial(WIDTH, HEIGHT, 150, 50, "Tutorial", events, DOWN_RED, LIGHT_BLACK)
        button_salir(WIDTH, HEIGHT, 150, 50, "Salir", events, DOWN_RED, LIGHT_BLACK)
        #game_title, game_title_rect = text_button(INTRO_TITLE, font, RED)
        #game_title_rect.center = (WIDTH/2, HEIGHT/4 + 30)
        #GameDisplay.blit(game_title, game_title_rect)

        pg.display.update()
