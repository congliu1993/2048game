import random
import pygame
import operator
import sys
from game2048.area import Area
def all_area(setting,screen):
    allArea=[]
    for i in range(4):
        for j in range(4):
            area = Area(setting, 2,i+1,j+1, screen)
            allArea.append(area)
    return allArea
def refresh_area(areas,setting,screen):
      m=0
      while m<4:
          t = random.randint(0, 2)
          flag=True
          per=4
          k = random.randint(1, 4)
          j = random.randint(1, 4)
          area = Area(setting, per, k, j, screen)
          for code in areas:
              if code.row==area.row and code.col==area.col:
                  m-=1
                  flag=False
                  break
          if flag:
              areas.append(area)
          m+=1
def check_event(allarea,areas,setting,screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
           check_keydown_event(allarea,event,areas,setting,screen)
    if check_game_over(areas)==False:
        sys.exit()
def event_simple(allarea,areas,setting,screen,flag1,flag2):
    newArea = parse_area(areas.copy(), flag1)
    muchNewArea = count_area(setting,screen,newArea, flag1, flag2)
    if check_game_over(muchNewArea) == True and len(muchNewArea)<16 and check_refresh(areas,muchNewArea):
        muchNewArea.append(check_empty_button(allarea,muchNewArea, setting, screen))
    areas.clear()
    areas.extend(muchNewArea)
def check_refresh(areas1,areas2):
    if len(areas2)>len(areas1):
        return False
    elif len(areas2)==len(areas1):
        cmfun = operator.attrgetter('row', 'col')
        areas1.sort(key=cmfun)
        areas2.sort(key=cmfun)
        for n in range(len(areas1)):
            if areas1[n].row!=areas2[n].row or areas1[n].col!=areas2[n].col:
                return True
        return False
    else:
        return True
def check_keydown_event(allarea,event,areas,setting,screen):
    if event.key == pygame.K_RIGHT:
        event_simple(allarea,areas,setting,screen,True,False)
    elif event.key == pygame.K_LEFT:
        event_simple(allarea,areas,setting,screen,True,True)
    elif event.key == pygame.K_UP:
        event_simple(allarea,areas,setting,screen,False,True)
    elif event.key == pygame.K_DOWN:
        event_simple(allarea,areas,setting,screen,False,False)
def print_screen(screen,areas):
    screen.fill((255,255,255))
    for view in areas:
        view.draw_area()
    pygame.display.flip()
def check_game_over(areas):
    if len(areas)<16:
        return True
    else:
        for area in areas:
            for code in areas:
                if area.msg==code.msg:
                    if (area.row==code.row and area.col==code.col+1) or (area.row==code.row and area.col==code.col-1):
                        return True
                    elif (area.col==code.col and area.row==code.row+1) or (area.col==code.col and area.row==code.row-1):
                        return True
        return False
def check_empty_button(allarea,areas,setting,screen):

    for n in range(len(allarea)):
            for m in range(len(areas)):
                if areas[m].row==allarea[n].row and areas[m].col==allarea[n].col:
                    break
                elif m==len(areas)-1 and (areas[m].row!=allarea[n].row or areas[m].col!=allarea[n].col):
                   area = Area(setting, 4, allarea[n].row, allarea[n].col, screen)
                   return  area
def parse_area(areas,flag):
    newArea=[]
    #True表示横向,False表示纵向
    if flag==True:
        cmfun = operator.attrgetter('row','col')
        areas.sort(key=cmfun)
        t=0
        rowArea=[]
        for n in range(len(areas)):
            if n==0:
                t=areas[n].row
                rowArea.append(areas[n])
            else:
                if areas[n].row==t:
                    rowArea.append(areas[n])
                else:
                    newArea.append(rowArea.copy())
                    rowArea.clear()
                    t=areas[n].row
                    rowArea.append(areas[n])
            if n == len(areas) - 1:
                newArea.append(rowArea.copy())
        return newArea
    else:
        cmfun = operator.attrgetter('col','row')
        areas.sort(key=cmfun)
        t = 0
        rowArea = []
        for n in range(len(areas)):
            if n == 0:
                t = areas[n].col
                rowArea.append(areas[n])
            else:
                if areas[n].col == t:
                    rowArea.append(areas[n])
                else:
                    newArea.append(rowArea.copy())
                    rowArea.clear()
                    t = areas[n].col
                    rowArea.append(areas[n])
            if n == len(areas) - 1:
                newArea.append(rowArea.copy())
        return newArea
def count_area(setting,screen,areas,flag,txt):
    newArea = []
    # flag True表示横向,False表示纵向
    if flag==True:
        # txt True表示向左,False表示向右
        for m in range(len(areas)):
            if len(areas[m])==1:
                if txt==True:
                    area = Area(setting,areas[m][0].msg,areas[m][0].row,1, screen)
                    #areas[m][0].onlyupdatePos(areas[m][0].row, 1)
                    newArea.append(area)
                else:
                    area = Area(setting, areas[m][0].msg, areas[m][0].row,4, screen)
                    #areas[m][0].onlyupdatePos(areas[m][0].row, 4)
                    newArea.append(area)
            elif len(areas[m])==2:
                if txt==True:
                    if areas[m][0].msg==areas[m][1].msg:
                      areas[m][0].update(areas[m][0].row,1)
                      newArea.append(areas[m][0])
                    else:
                      area1 = Area(setting, areas[m][0].msg, areas[m][0].row, 1, screen)
                      area2 = Area(setting, areas[m][1].msg, areas[m][1].row, 2, screen)
                      #areas[m][0].onlyupdatePos(areas[m][0].row, 1)
                      #areas[m][1].onlyupdatePos(areas[m][1].row, 2)
                      newArea.append(area2)
                      newArea.append(area1)
                else:
                    if areas[m][0].msg==areas[m][1].msg:
                      areas[m][1].update(areas[m][1].row,4)
                      newArea.append(areas[m][1])
                    else:
                      area1 = Area(setting, areas[m][0].msg, areas[m][0].row, 3, screen)
                      area2 = Area(setting, areas[m][1].msg, areas[m][1].row, 4, screen)
                      #areas[m][0].onlyupdatePos(areas[m][0].row, 3)
                      #areas[m][1].onlyupdatePos(areas[m][1].row, 4)
                      newArea.append(area1)
                      newArea.append(area2)
            elif len(areas[m])==3:
                if txt==True:
                    if areas[m][0].msg==areas[m][1].msg:
                        areas[m][0].update(areas[m][0].row,1)
                        areas[m][2].onlyupdatePos(areas[m][2].row,2)
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][2])
                    elif areas[m][1].msg==areas[m][2].msg:
                        areas[m][1].update(areas[m][1].row,2)
                        areas[m][0].onlyupdatePos(areas[m][0].row,1)
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][0])
                    else:
                        area1 = Area(setting, areas[m][0].msg, areas[m][0].row, 1, screen)
                        area2 = Area(setting, areas[m][1].msg, areas[m][1].row, 2, screen)
                        area3 = Area(setting, areas[m][2].msg, areas[m][2].row, 3, screen)
                        #areas[m][0].onlyupdatePos(areas[m][0].row, 1)
                        #areas[m][1].onlyupdatePos(areas[m][1].row, 2)
                        #areas[m][2].onlyupdatePos(areas[m][2].row, 3)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
                else:
                    if areas[m][1].msg==areas[m][2].msg:
                        areas[m][2].update(areas[m][2].row,4)
                        areas[m][0].onlyupdatePos(areas[m][0].row,3)
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][2])
                    elif areas[m][0].msg==areas[m][1].msg:
                        areas[m][1].update(areas[m][1].row,3)
                        areas[m][2].onlyupdatePos(areas[m][2].row,4)
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][2])
                    else:
                        area1 = Area(setting, areas[m][0].msg, areas[m][0].row, 2, screen)
                        area2 = Area(setting, areas[m][1].msg, areas[m][1].row, 3, screen)
                        area3 = Area(setting, areas[m][2].msg, areas[m][2].row, 4, screen)
                        #areas[m][2].onlyupdatePos(areas[m][2].row,4)
                        #areas[m][1].onlyupdatePos(areas[m][1].row,3)
                        #areas[m][0].onlyupdatePos(areas[m][0].row,2)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
            elif len(areas[m])==4:
                if txt==True:
                    if areas[m][0].msg==areas[m][1].msg:
                        areas[m][0].update(areas[m][0].row, 1)
                        if areas[m][2].msg==areas[m][3].msg:
                            areas[m][2].update(areas[m][2].row,2)
                            newArea.append(areas[m][2])
                            newArea.append(areas[m][0])
                        else:
                            areas[m][2].onlyupdatePos(areas[m][2].row,2)
                            areas[m][3].onlyupdatePos(areas[m][3].row,3)
                            newArea.append(areas[m][2])
                            newArea.append(areas[m][0])
                            newArea.append(areas[m][3])
                    elif areas[m][1].msg==areas[m][2].msg:
                        areas[m][3].onlyupdatePos(areas[m][3].row,3)
                        areas[m][0].onlyupdatePos(areas[m][0].row,1)
                        areas[m][1].update(areas[m][1].row,2)
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][3])
                    elif areas[m][2].msg==areas[m][3].msg:
                        areas[m][2].update(areas[m][2].row,3)
                        areas[m][1].onlyupdatePos(areas[m][2].row,2)
                        areas[m][0].onlyupdatePos(areas[m][2].row,1)
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][2])
                    else:
                        area1 = Area(setting, areas[m][0].msg, areas[m][0].row, 1, screen)
                        area2 = Area(setting, areas[m][1].msg, areas[m][1].row, 2, screen)
                        area3 = Area(setting, areas[m][2].msg, areas[m][2].row, 3, screen)
                        area4 = Area(setting, areas[m][3].msg, areas[m][3].row, 4, screen)
                        #areas[m][0].onlyupdatePos(areas[m][0].row,1)
                        #areas[m][1].onlyupdatePos(areas[m][1].row,2)
                        #areas[m][2].onlyupdatePos(areas[m][2].row,3)
                        #areas[m][3].onlyupdatePos(areas[m][3].row,4)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
                        newArea.append(area4)
                else:
                    if areas[m][2].msg==areas[m][3].msg:
                        areas[m][3].update(areas[m][3].row,4)
                        if areas[m][0].msg==areas[m][1].msg:
                            areas[m][1].update(areas[m][1].row,3)
                            newArea.append(areas[m][1])
                            newArea.append(areas[m][3])
                        else:
                            areas[m][0].onlyupdatePos(areas[m][0].row,2)
                            areas[m][1].onlyupdatePos(areas[m][1].row,3)
                            newArea.append(areas[m][1])
                            newArea.append(areas[m][0])
                            newArea.append(areas[m][3])
                    elif areas[m][1].msg==areas[m][2].msg:
                        areas[m][3].onlyupdatePos(areas[m][3].row,4)
                        areas[m][0].onlyupdatePos(areas[m][0].row,2)
                        areas[m][2].update(areas[m][2].row,3)
                        newArea.append(areas[m][2])
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][3])
                    elif areas[m][0].msg==areas[m][1].msg:
                        areas[m][1].update(areas[m][1].row,2)
                        areas[m][2].onlyupdatePos(areas[m][2].row,3)
                        areas[m][3].onlyupdatePos(areas[m][3].row,4)
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][2])
                        newArea.append(areas[m][3])
                    else:
                        area1 = Area(setting, areas[m][0].msg, areas[m][0].row, 1, screen)
                        area2 = Area(setting, areas[m][1].msg, areas[m][1].row, 2, screen)
                        area3 = Area(setting, areas[m][2].msg, areas[m][2].row, 3, screen)
                        area4 = Area(setting, areas[m][3].msg, areas[m][3].row, 4, screen)
                        #areas[m][0].onlyupdatePos(areas[m][0].row,1)
                        #areas[m][1].onlyupdatePos(areas[m][1].row,2)
                        #areas[m][2].onlyupdatePos(areas[m][2].row,3)
                        #areas[m][3].onlyupdatePos(areas[m][3].row,4)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
                        newArea.append(area4)
    else:
        # txt True表示向上,False表示向下
        for m in range(len(areas)):
            if len(areas[m]) == 1:
                if txt==True:
                    area1 = Area(setting, areas[m][0].msg, 1, areas[m][0].col, screen)
                    #areas[m][0].onlyupdatePos(1,areas[m][0].col)
                    newArea.append(area1)
                else:
                    area1 = Area(setting, areas[m][0].msg,4, areas[m][0].col, screen)
                    #areas[m][0].onlyupdatePos(4,areas[m][0].col)
                    newArea.append(area1)
            elif len(areas[m]) == 2:
                if txt==True:
                    if areas[m][0].msg == areas[m][1].msg:
                        areas[m][0].update(1,areas[m][0].col)
                        newArea.append(areas[m][0])
                    else:
                        area1 = Area(setting, areas[m][0].msg, 1, areas[m][0].col, screen)
                        area2 = Area(setting, areas[m][1].msg, 2, areas[m][1].col, screen)
                        #areas[m][0].onlyupdatePos(1,areas[m][0].col)
                        #areas[m][1].onlyupdatePos(2,areas[m][1].col)
                        newArea.append(area1)
                        newArea.append(area2)
                else:
                    if areas[m][0].msg == areas[m][1].msg:
                        areas[m][1].update(4,areas[m][1].col)
                        newArea.append(areas[m][1])
                    else:
                        area1 = Area(setting, areas[m][0].msg, 3, areas[m][0].col, screen)
                        area2 = Area(setting, areas[m][1].msg, 4, areas[m][1].col, screen)
                        #areas[m][0].onlyupdatePos(3,areas[m][0].col)
                        #areas[m][1].onlyupdatePos(4,areas[m][1].col)
                        newArea.append(area1)
                        newArea.append(area2)
            elif len(areas[m]) == 3:
                if txt==True:
                    if areas[m][0].msg == areas[m][1].msg:
                        areas[m][0].update(1,areas[m][0].col)
                        areas[m][2].onlyupdatePos(2,areas[m][0].col)
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][2])
                    elif areas[m][1].msg == areas[m][2].msg:
                        areas[m][1].update(2,areas[m][1].col)
                        areas[m][0].onlyupdatePos(1,areas[m][0].col)
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][0])
                    else:
                        area1 = Area(setting, areas[m][0].msg, 1, areas[m][0].col, screen)
                        area2 = Area(setting, areas[m][1].msg, 2, areas[m][1].col, screen)
                        area3 = Area(setting, areas[m][2].msg, 3, areas[m][2].col, screen)
                        #areas[m][0].onlyupdatePos(1,areas[m][0].col)
                        #areas[m][1].onlyupdatePos(2,areas[m][1].col)
                        #areas[m][2].onlyupdatePos(3,areas[m][2].col)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
                else:
                    if areas[m][1].msg == areas[m][2].msg:
                        areas[m][2].update(4,areas[m][2].col)
                        areas[m][0].onlyupdatePos(3,areas[m][0].col)
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][2])
                    elif areas[m][0].msg == areas[m][1].msg:
                        areas[m][1].update(3,areas[m][1].col)
                        areas[m][2].onlyupdatePos(4,areas[m][2].col)
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][2])
                    else:
                        area1 = Area(setting, areas[m][0].msg, 2, areas[m][0].col, screen)
                        area2 = Area(setting, areas[m][1].msg, 3, areas[m][1].col, screen)
                        area3 = Area(setting, areas[m][2].msg, 4, areas[m][2].col, screen)
                        #areas[m][2].onlyupdatePos(4,areas[m][2].col)
                        #areas[m][1].onlyupdatePos(3,areas[m][1].col)
                        #areas[m][0].onlyupdatePos(2,areas[m][0].col)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
            elif len(areas[m]) == 4:
                if txt==True:
                    if areas[m][0].msg == areas[m][1].msg:
                        areas[m][0].update(1,areas[m][0].col)
                        if areas[m][2].msg == areas[m][3].msg:
                            areas[m][2].update(2,areas[m][2].col)
                            newArea.append(areas[m][2])
                            newArea.append(areas[m][0])
                        else:
                            areas[m][2].onlyupdatePos(2,areas[m][2].col)
                            areas[m][3].onlyupdatePos(3,areas[m][3].col)
                            newArea.append(areas[m][2])
                            newArea.append(areas[m][0])
                            newArea.append(areas[m][3])
                    elif areas[m][1].msg == areas[m][2].msg:
                        areas[m][3].onlyupdatePos(3,areas[m][3].col)
                        areas[m][0].onlyupdatePos(1,areas[m][0].col)
                        areas[m][1].update(2,areas[m][1].col)
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][3])
                    elif areas[m][2].msg == areas[m][3].msg:
                        areas[m][2].update(3,areas[m][2].col)
                        areas[m][1].onlyupdatePos(2,areas[m][2].col)
                        areas[m][0].onlyupdatePos(1,areas[m][2].col)
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][2])
                    else:
                        area1 = Area(setting, areas[m][0].msg, 1, areas[m][0].col, screen)
                        area2 = Area(setting, areas[m][1].msg, 2, areas[m][1].col, screen)
                        area3 = Area(setting, areas[m][2].msg, 3, areas[m][2].col, screen)
                        area4 = Area(setting, areas[m][3].msg, 4, areas[m][3].col, screen)
                        #areas[m][0].onlyupdatePos(1,areas[m][0].col)
                        #areas[m][1].onlyupdatePos(2,areas[m][1].col)
                        #areas[m][2].onlyupdatePos(3,areas[m][2].col)
                        #areas[m][3].onlyupdatePos(4,areas[m][3].col)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
                        newArea.append(area4)
                else:
                    if areas[m][2].msg == areas[m][3].msg:
                        areas[m][3].update(4,areas[m][3].col)
                        if areas[m][0].msg == areas[m][1].msg:
                            areas[m][1].update(3,areas[m][1].col)
                            newArea.append(areas[m][1])
                            newArea.append(areas[m][3])
                        else:
                            areas[m][0].onlyupdatePos(2,areas[m][0].col)
                            areas[m][1].onlyupdatePos(3,areas[m][1].col)
                            newArea.append(areas[m][1])
                            newArea.append(areas[m][0])
                            newArea.append(areas[m][3])
                    elif areas[m][1].msg == areas[m][2].msg:
                        areas[m][3].onlyupdatePos(4,areas[m][3].col)
                        areas[m][0].onlyupdatePos(2,areas[m][0].col)
                        areas[m][2].update(3,areas[m][2].col)
                        newArea.append(areas[m][2])
                        newArea.append(areas[m][0])
                        newArea.append(areas[m][3])
                    elif areas[m][0].msg == areas[m][1].msg:
                        areas[m][3].onlyupdatePos(4,areas[m][3].col)
                        areas[m][2].onlyupdatePos(3,areas[m][2].col)
                        areas[m][1].update(2,areas[m][1].col)
                        newArea.append(areas[m][2])
                        newArea.append(areas[m][1])
                        newArea.append(areas[m][3])
                    else:
                        area1 = Area(setting, areas[m][0].msg, 1, areas[m][0].col, screen)
                        area2 = Area(setting, areas[m][1].msg, 2, areas[m][1].col, screen)
                        area3 = Area(setting, areas[m][2].msg, 3, areas[m][2].col, screen)
                        area4 = Area(setting, areas[m][3].msg, 4, areas[m][3].col, screen)
                        #areas[m][0].onlyupdatePos(1,areas[m][0].col)
                        #areas[m][1].onlyupdatePos(2,areas[m][1].col)
                        #areas[m][2].onlyupdatePos(3,areas[m][2].col)
                        #areas[m][3].onlyupdatePos(4,areas[m][3].col)
                        newArea.append(area1)
                        newArea.append(area2)
                        newArea.append(area3)
                        newArea.append(area4)
    return newArea







