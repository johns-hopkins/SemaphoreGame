import pygame
import pygame_gui
import random
from string import ascii_lowercase
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Semaphore Game")
CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
letter_to_figure = {letter: pygame.transform.scale_by(pygame.image.load(f"semapics/{letter.upper()}.png").convert(), 1/6) for letter in ascii_lowercase}
entry_box = pygame_gui.elements.UITextEntryLine(pygame.Rect(300, 500, 400, 50), MANAGER, object_id="#main_text_entry")
background = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

text1_font = pygame.font.SysFont("comicsans", 90, bold = True)
text2_font = pygame.font.SysFont("comicsans", 20)
text3_font = pygame.font.SysFont("comicsans", 40)
with open("words.txt") as f:
    contents = f.read()
    words = contents.split()


class button():
    def __init__(self, text, x_pos, y_pos):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.draw()

    def draw(self):
        button_text = text3_font.render(self.text, True, "black")
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (200, 60))
        if self.check_click():
            pygame.draw.rect(SCREEN, "red", button_rect)
        else:
             pygame.draw.rect(SCREEN, "yellow", button_rect)
        SCREEN.blit(button_text, (self.x_pos + (200/2 - button_text.get_width()/2), self.y_pos + (60/2 - button_text.get_height()/2)))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (200, 60))
        if left_click and button_rect.collidepoint (mouse_pos):
            return True
        else:
            return False

def draw_T (text, font, color, x, y):
    img= font.render (text, True, color)
    SCREEN.blit(img, (x, y))

def draw_BG():
    SCREEN.blit(background, (0, 0))

def draw_L(lives):
    text = "Lives: " + str(lives)
    draw_T(text , text3_font, (0, 0, 0), 750, 10)

def draw_S(score):
    text = "Score: " + str(score)
    draw_T(text , text3_font, (0, 0, 0), 50, 10)

def LOSE():
    
    lose_screen = pygame.Surface([600, 400])
    lose_screen.fill("white")
    mainscreen = button("RETURN",  400, 500)
        
    run = True

    while run:

        if pygame.mouse.get_pressed()[0]:
            if mainscreen.check_click():
                MAIN()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

        SCREEN.blit(lose_screen, (200, 200))
        draw_T("YOU LOSE!", text1_font, ("black"), 260, 260)
        mainscreen.draw() 
        pygame.display.flip()
        
    pygame.quit()

def PLAY():
    word_to_guess = random.choice(words)
    letters = list(word_to_guess)
    print(word_to_guess)
    figures = []
    fig_x = 100

    for i in letters:
        correct_figure = letter_to_figure[i]
        fig_pos = (fig_x, 200)
        figures.append((correct_figure, fig_pos))
        fig_x = fig_x + 200
        
    lives = 3
    score = 0
   
    run = True
    while run:

        draw_BG()
        draw_L(lives)
        draw_S(score)

        UI_REFRESH_RATE = CLOCK.tick(60)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":  
                entry_box.set_text("")
                ans = event.text
                if ans != word_to_guess:
                    lives = lives - 1
                else:
                    score += 1
                
                word_to_guess = random.choice(words)
                letters = list(word_to_guess)
                figures.clear()
                fig_x = 100
                for i in letters:
                    correct_figure = letter_to_figure[i]
                    fig_pos = (fig_x, 200)
                    figures.append((correct_figure, fig_pos))
                    fig_x = fig_x + 200

                print(word_to_guess, lives)
                if lives == 0:
                    LOSE()
                    run = False
                
            MANAGER.process_events(event)
       
        MANAGER.draw_ui(SCREEN)
        MANAGER.update(UI_REFRESH_RATE)

        SCREEN.fblits(figures)
        pygame.display.flip()

    pygame.quit()

def MAIN():
    run = True

    while run:
    
        main_mouse_pos = pygame.mouse.get_pos()

        draw_BG()
        draw_T("SEMAPHORE GAME", text1_font, (0, 0, 0), 70, 300)
        draw_T("WELCOME TO", text2_font, (0, 0, 0), 430, 270)

        play = button("PLAY", 400, 550)
        stop = button("QUIT",  400, 650)
        
        if pygame.mouse.get_pressed()[0]:
            if play.check_click():
                PLAY()
            if stop.check_click():
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.flip()
    pygame.quit()

MAIN()