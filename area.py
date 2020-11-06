import pygame.font
class Area():
    def __init__(self,setting,msg,row,col,screen):
        self.msg=msg
        self.screen=screen
        self.row=row
        self.col=col
        self.font = pygame.font.SysFont(None, 48)
        self.text_color=(0,0,0)
        self.setting=setting
        self.rect = pygame.Rect(0, 0, self.setting.areawidth, self.setting.areawidth)
        self.init_rect_position()
        self.initColor()
        self.init_image()
    def init_rect_position(self):
        self.rect.x=(self.col-1)*self.setting.areawidth
        self.rect.y=(self.row-1)*self.setting.areawidth
    def update(self,row,col):
        self.msg=self.msg+self.msg
        self.row=row
        self.col=col
        self.initColor()
        self.init_rect_position()
        self.init_image()
    def onlyupdatePos(self,row,col):
        self.row=row
        self.col=col
        self.initColor()
        self.init_rect_position()
        self.init_image()
    def initColor(self):
        if self.msg==2:
            self.txt='2'
            self.bg_color=(255,179,167)
        elif self.msg==4:
            self.txt='4'
            self.bg_color=(244,121,131)
        elif self.msg==8:
            self.txt='8'
            self.bg_color = (219,90,107)
        elif self.msg==16:
            self.txt='16'
            self.bg_color = (250,255,114)
        elif self.msg==32:
            self.txt='32'
            self.bg_color = (255,241,67)
        elif self.msg==64:
            self.txt='64'
            self.bg_color = (255,164,0)
        elif self.msg==128:
            self.txt='128'
            self.bg_color = (250,140,53)
        elif self.msg==256:
            self.txt='256'
            self.bg_color = (141,75,187)
        elif self.msg==512:
            self.txt='512'
            self.bg_color = (128,29,174)
        elif self.msg==1024:
            self.txt='1024'
            self.bg_color = (75,92,196)
        elif self.msg==2048:
            self.txt='2048'
            self.bg_color = (112,243,255)
    def init_image(self):
        self.msg_image = self.font.render(self.txt, True, self.text_color,
                                          self.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_area(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

