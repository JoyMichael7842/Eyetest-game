import cv2
import numpy as np
import imutils
import pygame
from datetime import datetime,timedelta

f = open("data.txt",'w')

def car(carImg,x, y):
  gameDisplay.blit(carImg, (x, y))

def dispbluebucket(x,y):
    gameDisplay.blit(bucketImg, (x, y))



def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        
        if click[0] == 1:
            
            return 1         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    return 0


def displayintro(point,gameDisplay,clock):
    
    gameDisplay.fill(white)
    flag = button('start',350,100,100,50,green,bright_green)
    pygame.display.update()
    clock.tick(60)
    return flag 

def displaycar(point,gameDisplay,clock,bucket,color):
    
    gameDisplay.fill(white)
    car(carImg1,point[0], point[1])
    pygame.draw.line(gameDisplay, color, bucket[0][0],bluebucket[0][1])
    pygame.draw.line(gameDisplay, color, bucket[1][0],bluebucket[1][1])
    pygame.draw.line(gameDisplay, color, bucket[2][0],bluebucket[2][1])
    flag2 = button('next',350,100,100,50,red,bright_red)
    pygame.display.update()
    clock.tick(60)
    return flag2

def displaycar2(point,gameDisplay,clock,msg):
    
    gameDisplay.fill(white)
    car(carImg1,130, 420)
    
    pygame.draw.line(gameDisplay, (0, 0, 255), (100,400), (100,500))
    pygame.draw.line(gameDisplay, (0, 0, 255), (200,400), (200,500))
    pygame.draw.line(gameDisplay, (0, 0, 255), (100,500), (200,500))

    car(carImg2,point[0], point[1])
    pygame.draw.line(gameDisplay, (255, 0, 0), (600,400), (600,500))
    pygame.draw.line(gameDisplay, (255, 0, 0), (700,400), (700,500))
    pygame.draw.line(gameDisplay, (255, 0, 0), (600,500), (700,500))

    flag4 = button(msg,350,100,100,50,red,bright_red)

    pygame.display.update()
    clock.tick(60)
    return flag4


pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0,0,255)
green = (0,200,0)
red = (200,0,0)

bright_green = (0,255,0)
bright_red = (255,0,0)

clock = pygame.time.Clock()

carImg1 = pygame.image.load('bluecircle.jpg')
carImg2  = pygame.image.load('redcircle.jpg') 

flag = 0
flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
count = 0
bluebucket = [[(100,400), (100,500)],[(200,400), (200,500)],[(100,500), (200,500)]]
redbucket = [[(600,400), (600,500)],[(700,400), (700,500)],[(600,500), (700,500)]]

cap = cv2.VideoCapture(0)



while(cap.isOpened()):
    
    # Take each frame
    ret, frame = cap.read()
    
    if ret:
    # Convert BGR to HSV
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame,width=800)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # Define range of blue color in HSV
        lower_blue = np.array([100, 60, 60])
        upper_blue = np.array([140, 255, 255])
        
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]

            cen = (center[0],center[1])
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255, 255), 2)
            cv2.circle(frame, cen, 5, (0, 0, 255), -1)
            print(center)

        
            

            count = 0
            if flag == 0:
                flag = displayintro(center,gameDisplay,clock)   
                if flag==1:
                    t1 = datetime.now().minute 
            
                    print('blue started at time {}'.format(datetime.now()))
                    f.write('blue started at time {}\n'.format(datetime.now().strftime("%c")))    
            else:
                if flag1 == 0:
                    displaycar(center,gameDisplay,clock,bluebucket,blue)
                    
                    if (center[0]>130 and center[0]<160 and center[1]>430 and center[1]<470) or datetime.now().minute-t1==2:
                        flag1 = 1
                        print('blue ended at time {}'.format(datetime.now()))
                        f.write('blue ended at time {}\n'.format(datetime.now().strftime("%c")))
            if flag1==1 and flag2==0:            
                flag2 = displaycar(((130, 420)),gameDisplay,clock,bluebucket,blue) 
                if flag2==1:
                    t2 = datetime.now().minute
                    print('red started at time {}'.format(datetime.now()))
                    f.write('red started at time {}\n'.format(datetime.now().strftime("%c")))    

            if flag2 == 1 and flag3==0:
                displaycar2(center,gameDisplay,clock,'done')
                if (center[0]>630 and center[0]<660 and center[1]>430 and center[1]<470) or datetime.now().minute-t2==2:
                    flag3=1
                    print('red ended at time {}'.format(datetime.now()))
                    f.write('red ended at time {}\n'.format(datetime.now().strftime("%c")))

            if flag3 == 1 and flag4 ==0:
                flag4 = displaycar2(((630,420)),gameDisplay,clock,'done')

            if flag4 == 1 :
                displaycar2(((630,420)),gameDisplay,clock,'complete')

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask= mask)
        # cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        cv2.imshow('res', res)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

f.close()
pygame.quit()
quit()