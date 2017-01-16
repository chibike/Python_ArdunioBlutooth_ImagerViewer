import urllib, pygame, sys, time


def restart():
    urllib.urlopen("http://10.14.121.75/game/restart")

def new():
    urllib.urlopen("http://10.14.121.75/game/new")

def up():
    urllib.urlopen("http://10.14.121.75/mdxBot/move/y-")

def down():
    urllib.urlopen("http://10.14.121.75/mdxBot/move/y+")

def left():
    urllib.urlopen("http://10.14.121.75/mdxBot/move/x-")

def right():
    urllib.urlopen("http://10.14.121.75/mdxBot/move/x+")

def bar():
    urllib.urlopen("http://10.14.121.75/username/blink")

pygame.init()
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Joystick Testing / XBOX360 Controller")

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255,0,255))
    
    joysticks = []
    clock = pygame.time.Clock()
    keep_playing = True
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print "Detected Joystick"
        print "Name =",joysticks[-1].get_name()
    while keep_playing:
        clock.tick(60)
        for  event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_playing = False
                #BT.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                keep_playing = False
                #BT.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:#A
                    print "KEY A PRESSED"
                elif event.button == 1:#B
                    print "KEY B PRESSED"
                elif event.button == 2:#X
                    print "KEY X PRESSED"
                elif event.button == 3:#Y
                    print "KEY Y PRESSED"
                elif event.button == 4:#L1
                    print "KEY L1 PRESSED"
                elif event.button == 5:#R1
                    print "KEY R1 PRESSED"
                elif event.button == 6:#BACK
                    print "KEY BACK PRESSED"
                elif event.button == 7:#START
                    print "KEY START PRESSED"
                #print "Button Pressed =", event.button
            elif event.type == pygame.JOYAXISMOTION:
                #print "JOYSTICK MOTION AXIS =",event.dict['axis']
                #print "JOYSTICK MOTION VALUE =",event.dict['value']
                axis = event.dict['axis']
                value = event.dict['value']
                if axis == 0:
                    print "LEFT JOYSTICK Y =",value
                elif axis == 1:
                    print "LEFT JOYSTICK X =",value
                elif axis == 2:
                    print "ANALOG TRIGGER =",value
                elif axis == 3:
                    print "RIGHT JOYSTICK X =",value
                elif axis == 4:
                    print "RIGHT JOYSTICK Y =",value
                
            elif event.type == pygame.JOYHATMOTION:
                #print "JOYSTICK HAT MOTION AXIS =",event.dict['axis']
                #print "JOYSTICK HAT MOTION VALUE =",event.dict['value']
                k = event.dict['value']
                if k[0] < 0:
                    print "HAT LEFT PRESSED"
                elif k[0] > 0:
                    print "HAT RIGHT PRESSED"

                if k[1] < 0:
                    print "HAT DOWN PRESSED"
                elif k[1] > 0:
                    print "HAT UP PRESSED"
                    
            else:
                if event.type == 2:
                    if event.key == 273:
                        print "UP PRESSED"
                        #BT.write("SA;0;F;")
                        up()
                    elif event.key == 274:
                        print "DOWN PRESSED"
                        #BT.write("SA;0;B;")
                        down()
                    elif event.key == 276:
                        print "LEFT PRESSED"
                        #BT.write("SA;-30;F;")
                        left()
                    elif event.key == 275:
                        print "RIGHT PRESSED"
                        #BT.write("SA;30;F;")
                        right()
                    elif event.key == 32:
                        print "SPACE PRESSED"
                        #BT.write("SA;0;")
                        new()
                    elif event.key == 97:
                        print "A PRESSED"
                        #BT.write("SA;0;")
                        bar()
                    else:
                        print "PRESSED = KEY",event.key
                elif event.type == 3:
                    if event.key == 273:
                        print "UP RELEASED"
                        #BT.write("S;")
                    elif event.key == 274:
                        print "DOWN PRESSED"
                        #BT.write("S;")
                    elif event.key == 276:
                        print "LEFT RELEASED"
                    elif event.key == 275:
                        print "RIGHT RELEASED"
                    elif event.key == 32:
                        print "SPACE RELEASED"
                    else:
                        print "RELEASED = KEY",event.key
                else:
                    try:
                        print "Event Type =",event.type
                        print "Event Key =",event.key
                    except:
                        continue
        #screen.blit(background, (0,0))
        #pygame.display.flip()

main()
pygame.quit()
sys.exit()
