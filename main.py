import sys
import pygame
from file import mortgage

pygame.init()
pygame.display.set_caption('Mortgage')

fps = 60
fpsClock = pygame.time.Clock()
width, height = 1000,800
screen = pygame.display.set_mode((width,height))
font = pygame.font.SysFont('Arial',40)
font2 = pygame.font.SysFont('Arial',15)
colour_inactive = '#bbbbbb'
colour_active = '#333333'

buttons = []
inputboxes = []
textboxes = []
labels = []

class Button():
    def __init__(self, x, y, width, height, buttonText='Enter', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        
        self.fillColours = {
            'normal': '#bbbbbb',
            'hover': '#666666',
            'pressed': '#333333'
        }
        
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.buttonSurf = font.render(buttonText, True, (20,20,20))
        buttons.append(self)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColours['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColours['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColours['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
        
def myFunction():
    pay,total,unit = mortgage(float(t1.text),float(t2.text),float(t3.text),t4.text)
    print('£' + pay + ' per ' + unit)
    print('£' + total + ' in total')
    answer = '£' + pay + ' per ' + unit + '   £' + total + ' in total'
    
    screen.fill((255,255,255),rect=(100,500,700,200))
    ans_surface = font.render(answer,True,(0,0,0))
    screen.blit(ans_surface, (100,500))

    
class InputBox:
    def __init__(self,x, y, width, height, textbox, text='',value=''):
        self.rect = pygame.Rect(x,y,width,height)
        self.colour = colour_inactive
        self.text = text
        self.txt_surface = font.render(text,True,self.colour)
        self.active = False
        self.textbox = textbox
        inputboxes.append(self)
    
    def process(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            
            if self.active:
                self.colour = colour_active
            else:
                self.colour = colour_inactive
                
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.textbox.setText(self.text)
                    screen.fill((255,255,255),self.rect)
                    self.textbox.draw(screen)
                    self.value = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    screen.fill((255,255,255),self.rect)
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.colour)
    
    def resize(self):
        self.rect.width = max(200, self.txt_surface.get_width())
        self.rect.height = self.txt_surface.get_height()
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5,self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 2)
    
class TextBox:
    def __init__(self,x,y,w,h,text=''):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.textSurface = font.render(self.text,True,(0,0,0))
        textboxes.append(self)
        
    def draw(self,screen):
        screen.fill((255,255,255),self.rect)
        self.rect.w = max(200,self.textSurface.get_width())
        self.rect.h = self.textSurface.get_height()
        screen.blit(self.textSurface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, (0,0,0),self.rect,2)
    
    def setText(self,newtext):
        self.text = newtext
        self.textSurface = font.render(newtext,True,(0,0,0))
        
class Label:
    def __init__(self,x,y,w,h,text):
        self.text = text
        self.textSurface = font2.render(self.text,True,(0,0,0))
        self.x = x
        self.y = y
        labels.append(self)
        
    def draw(self,screen):
        screen.blit(self.textSurface, (self.x+5, self.y+5))
        
        
        
b1 = Button(800, 600, 100, 50, 'Enter', myFunction)
t1 = TextBox(500,50,140,32)
t2 = TextBox(500,150,140,32)
t3 = TextBox(500,250,140,32)
t4 = TextBox(500,350,140,32)
l1 = Label(100,30,140,32,'Enter interest rate: ')
l2 = Label(100,130,140,32,'Enter the loan: ')
l3 = Label(100,230,140,32,'Enter the time period in years: ')
l4 = Label(100,330,140,32,'Enter the compound interval (Weekly, Monthly or Daily): ')
i1 = InputBox(100,50,140,32,t1)
i2 = InputBox(100,150,140,32,t2)
i3 = InputBox(100,250,140,32,t3)
i4 = InputBox(100,350,140,32,t4)


screen.fill((255,255,255))
for label in labels:
    label.draw(screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        for inputbox in inputboxes:
            inputbox.process(event)
    for inputbox in inputboxes:
        inputbox.resize()
        inputbox.draw(screen)
    
    for button in buttons:
        button.process()
    
    pygame.display.flip()
    fpsClock.tick(fps)