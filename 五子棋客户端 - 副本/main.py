#encoding:gb2312
import pygame
from pygame.locals import *
import sys
import math
import storn
from socket import *
import select
import Tkinter

pygame.init()
pygame.mixer.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

#�ж��Ƿ�����
def isempty(me,targert):
    a = False
    for i in targert:
        if i.location() == me.location():
            a = True
    return a


#�ж��Ƿ�����������
def iswin(targert):
    x = []
    y = []
    for i in range(0,15):
        x.append(28+i*40)
    for i in range(0,15):
        y.append(28+i*40)
    for each in targert:
        (a,b) = each.location()
        
        #x�᷽��
        num_x = 0
        c = a - 40
        d = a + 40
        while c > 0:
            isbreak = True
            for i in targert:
                if i.location() == (c,b):
                    num_x += 1
                    isbreak = False
            if not isbreak:
                c -= 40
            else:
                break
        while d < 615:
            isbreak = True 
            for i in targert:
                if i.location() == (d,b):
                    num_x += 1
                    isbreak = False
            if not isbreak:
                d += 40
            else:
                break
        num_x += 1
        
        #y�᷽��
        num_y = 0
        e = b - 40
        f = b + 40
        while e > 0:
            isbreak = True
            for i in targert:
                if i.location() == (a,e):
                    num_y += 1
                    isbreak = False
            if not isbreak:        
                e -= 40
            else:
                break
        while f < 615:
            isbreak = True
            for i in targert:
                if i.location() == (a,f):
                    num_y += 1
                    isbreak = False
            if not isbreak:
                f += 40
            else:
                break
        num_y += 1
        
        #���������Ϸ���
        num_en = 0
        c1 = a - 40
        c2 = b - 40
        c3 = a + 40
        c4 = b + 40
        while c1>0 and c2>0:
            isbreak = True
            for i in targert:
                if i.location() == (c1,c2):
                    num_en += 1
                    isbreak = False
            if not isbreak:
                c1 -= 40
                c2 -= 40
            else:
                break
        while c3 < 615 and c4 < 615:
            isbreak = True
            for i in targert:
                isbreak = True
                if i.location() == (c3,c4):
                    num_en += 1
                    isbreak = False
            if not isbreak:
                c3 += 40
                c4 += 40
            else:
                break
        num_en += 1

        #���������Ϸ���
        num_wn = 0
        c5 = a + 40
        c6 = b - 40
        c7 = a - 40
        c8 = b + 40
        while c5 < 615 and c6 > 0:
            isbreak = True
            for i in targert:
                if i.location() == (c5,c6):
                    num_wn += 1
                    isbreak = False
            if not isbreak:
                c5 += 40
                c6 -= 40
            else:
                break
        while c7 > 0 and c8 < 615:
            isbreak = True
            for i in targert:
                isbreak = True
                if i.location() == (c3,c4):
                    num_wn += 1
                    isbreak = False
            if not isbreak:
                c7 -= 40
                c8 += 40
            else:
                break
        num_wn += 1
        if num_x >= 5 or num_y >= 5 or num_en >= 5 or num_wn >= 5:
            return True
    return False

#����IP��ַ
def gui():
    top = Tkinter.Tk()
    top.title('IP')
    top.geometry('300*200')

    L1 = Tkinter.Label(top,text='IP ��ַ',font='�����п�')
    L1.grid(row=0,column=1)
def main():
    
    bg_size = 615,615

    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption('������')
    bg_image = pygame.image.load('image/bg.png').convert_alpha()  #����ͼƬ

    #��������
    bg_sound = pygame.mixer.music.load('sound/bg_music.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    running = True
    
    clock = pygame.time.Clock()

    #TCP����
    HOST = 'localhost'
    POST = 21578
    BUFSIZ = 2048
    ADDR = (HOST,POST)
    
    tcpclisock = socket(AF_INET,SOCK_STREAM)
    tcpclisock.connect(ADDR)

    inputs = [tcpclisock]
    
    #����
    white_chesses = []
    black_chesses = []
    chesses = []

    #��־�ֵ��ķ�����
    isplay = True

    #��־�Ƿ�����
    islink = True

    #��־�Ƿ������Ϸ
    result = False

    #��־������
    is_people = False

    #��־�������
    is_ai = False

    #��־�Ƿ�����ѡ��
    is_choise = False

    #��Ӯ
    font1 = pygame.font.Font('font/12345.TTF',30)
    win_text = font1.render("You Lose!!!",True,WHITE)
    win_text_rect = win_text.get_rect()
    win_text_rect.left,win_text_rect.top = (bg_size[0]-win_text_rect.width)//2,\
                                           (bg_size[1]-win_text_rect.height)//2
    lose_text = font1.render("You Win...",True,WHITE)
    lose_text_rect = lose_text.get_rect()
    lose_text_rect.left,lose_text_rect.top = (bg_size[0]-lose_text_rect.width)//2,\
                                           (bg_size[1]-lose_text_rect.height)//2
    play_text = font1.render("Play Again",True,WHITE)
    play_text_rect = play_text.get_rect()

    #����ѡ��
    text1 = font1.render('��������', True, WHITE)
    text1_rect = text1.get_rect()
    text1_rect.left,text1_rect.top = (bg_size[0]-text1_rect.width)//2,\
                                           (bg_size[1]-text1_rect.height)//2 - 60
    text2 = font1.render('��������',True, WHITE)
    text2_rect = text2.get_rect()
    text2_rect.left, text2_rect.top = (bg_size[0] - text1_rect.width) // 2, \
                                      (bg_size[1] - text1_rect.height) // 2
    text3 = font1.render('������  ��',True, WHITE)
    text3_rect = text3.get_rect()
    text3_rect.left, text3_rect.top = (bg_size[0] - text3_rect.width) // 2, \
                                      (bg_size[1] - text3_rect.height) // 2 + 60
    text4 = font1.render('������  ��',True, BLACK)
    text4_rect = text4.get_rect()
    text4_rect.left, text4_rect.top = (bg_size[0] - text4_rect.width) // 2, \
                                      (bg_size[1] - text4_rect.height) // 2 + 60
    
    while running:

        screen.blit(bg_image,(0,0))

        #����ѡ��
        if not choise:
            screen.blit(text1,text1_rect)
            screen.blit(text2,text2_rect)
            screen.blit(text3,text3_rect)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if text1_rect.left <= pos[0] <= text1_rect.left + 100 and \
                                        text1_rect.top <= pos[1] <= text1_rect.top + 60:
                    is_choise = True
                    is_people = True
                if text1_rect.left <= pos[0] <= text1_rect.left + 100 and \
                                                text1_rect.top +60 <= pos[1] <= text1_rect.top + 120:
                    is_choise = True
                    is_people = True



        #��������
        if choise:
            if chesses:
                for i in chesses:
                    screen.blit(i.image,i.location())

        for event in pygame.event.get():
            if event.type == QUIT:
                tcpclisock.close()
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN and not result:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    #�ж��Ƿ������Ƿ����Լ�����ʱ��
                    if islink and isplay:
                        me = storn.Storn_White(pos)
                        if not isempty(me,chesses):
                            white_chesses.append(me)
                            chesses.append(me)
                            tcpclisock.send(str(pos))
                            isplay = False
                        else:
                            del(me)
                            

        #����cli����Ϣ
        rs,ws,es = select.select(inputs,[],[],0)
        for r in rs:
            if r is tcpclisock: 
                try:
                    data = r.recv(BUFSIZ)
                    disconnected = not data
                    if not isplay:
                        me = storn.Storn_Black(eval(data))
                        black_chesses.append(me)
                        chesses.append(me)
                        isplay = True
                except socket.error:
                    disconnected = True
                    islink = False

        #�ж���Ӯ
        if iswin(black_chesses):
            screen.blit(lose_text,win_text_rect)
            screen.blit(play_text,(win_text_rect.left,win_text_rect.top + 80))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if win_text_rect.left < pos[0] < win_text_rect.right and\
                   win_text_rect.top + 80< pos[1] < win_text_rect.top + 120:
                    main()
                    
        if iswin(white_chesses):
            screen.blit(win_text,lose_text_rect)
            screen.blit(play_text,(win_text_rect.left,win_text_rect.top + 80))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if win_text_rect.left < pos[0] < win_text_rect.right and\
                   win_text_rect.top +80< pos[1] < win_text_rect.top + 120:
                    main()
            
        pygame.display.flip()

        clock.tick(60)


        
if __name__ == '__main__':
    main()
