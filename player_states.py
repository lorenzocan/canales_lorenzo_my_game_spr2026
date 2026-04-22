from state_machine import *
from settings import *
from utils import *

class PlayerFlyState(State):
    def __init__(self, player):
        self.player = player
        self.name = "fly"

    def get_state_name(self):
        return "fly"

    def enter(self):
        # start dash timer
        # increase speed
        self.player.image.fill(MAGENTA)
        self.player.dash_rect = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)
        print('enter player fly state')

    def exit(self):
        print('exit player fly state')
        self.player.dash_rect = pg.Rect(0,0,0,0)

    def update(self):
        # print('updating player move state...')
        # when start timer done, exit state
        self.player.image.fill(GREEN)
        keys = pg.key.get_pressed()

class PlayerDashState(State):
    def __init__(self, player):
        self.player = player
        self.name = "dash"

        self.dash_slash_cd = Cooldown(2000)
        self.dash_slash_length = Cooldown(300) 
        self.dash_slash_freeze_length = Cooldown(200)
        self.dash_slash_end_freeze_length = Cooldown(500)

    def get_state_name(self):
        return "dash"

    def enter(self):
        # start dash timer
        # increase speed

        self.dash_slash_cd.start()
        self.dash_slash_length.start()
        self.dash_slash_freeze_length.start()
        self.dash_slash_end_freeze_length.start()
        self.player.image.fill(YELLOW)
        self.player.dash_rect = self.dash_rect = pg.Rect(self.player.pos.x - TILESIZE, self.player.pos.y - TILESIZE, TILESIZE * 2, TILESIZE * 2)

        print('enter player dash state')

    def exit(self):
        print('exit player dash state')
        print("cd:",self.dash_slash_cd.ready(),
              "lgnth:",self.dash_slash_length.ready(),
              "f:",self.dash_slash_freeze_length.ready(),
              "ef:",self.dash_slash_end_freeze_length.ready())
        self.player.vel.x = 0
        self.player.dash_rect = pg.Rect(0,0,0,0)

    def update(self):
        # print('updating player dash state...')
        # when start timer done, exit state
        self.player.image.fill(YELLOW)
        
        print("cd:",self.dash_slash_cd.ready(),
              "lgnth:",self.dash_slash_length.ready(),
              "f:",self.dash_slash_freeze_length.ready(),
              "ef:",self.dash_slash_end_freeze_length.ready())

        if self.dash_slash_freeze_length.ready(): # after freeze time is done, do the moving
            # if the dash time is in between the end of end dash freeze and the end of dash length, do not do anything
            if not self.dash_slash_end_freeze_length.ready() and self.dash_slash_length.ready():
                pass

            elif not self.dash_slash_length.ready(): # without this, movement happens as soon as everything ends
                # check most recent direction to fix the direction of dash
                if self.player.direction == "left" and not self.dash_slash_length.ready():
                    self.player.pos.x -= PLAYER_SPEED * self.player.game.dt * 12
                else:
                    self.player.pos.x += PLAYER_SPEED * self.player.game.dt * 12
                        
                # dash hitbox moves along with player during the duration of the dash
                self.dash_rect = pg.Rect(self.player.pos.x - TILESIZE, self.player.pos.y - TILESIZE, TILESIZE * 2, TILESIZE * 2)
        
        # exit dash state when dash ends
        if self.dash_slash_end_freeze_length.ready():
            self.exit()
            print("dash done")
            self.player.state_machine.transition("fly")
