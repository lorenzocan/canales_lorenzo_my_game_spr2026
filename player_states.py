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
        self.player.animate()
        print('enter player fly state')

    def exit(self):
        print('exit player fly state')

    def update(self):
        self.player.animate()

class PlayerDashState(State):
    def __init__(self, player):
        self.player = player
        self.name = "dash"

        # using cooldown object to describe a time length for the dash rather than a length of waiting
        self.dash_slash_length = Cooldown(300) # this long to account for the 200 spent nothing-ing
        self.dash_slash_freeze_length = Cooldown(200)
        self.dash_slash_end_freeze_length = Cooldown(500) # this long to account for the 300 ticks spent dashing

    def get_state_name(self):
        return "dash"

    def enter(self):
        self.player.animate()
        # start dash timer
        self.player.dash_slash_cd.start()
        self.dash_slash_length.start()
        self.dash_slash_freeze_length.start()
        self.dash_slash_end_freeze_length.start()

        self.player.is_key_locked = True

        print('enter player dash state')

    def exit(self):
        print('exit player dash state')
        self.player.is_key_locked = False
        self.player.vel.x = 0


    def update(self):
        self.player.animate()
        # print('updating player dash state...')
        if self.dash_slash_freeze_length.ready(): # after freeze time is done, do the moving

            # if the dash time is in between the end of end dash freeze and the end of dash length (the end freeze)...
            if not self.dash_slash_end_freeze_length.ready() and self.dash_slash_length.ready():
                # ensures hitbox won't take up space to affect enemy health only when dashing
                self.player.dash_rect = pg.Rect(0,0,0,0)
            
            # without this, movement happens as soon as everything ends - i.e. do the dash only within the time frame of the dash itself
            elif not self.dash_slash_length.ready():
                # check most recent direction to fix the direction of dash
                if self.player.direction == "left" and not self.dash_slash_length.ready():
                    self.player.pos.x -= PLAYER_SPEED * self.player.game.dt * 12
                else:
                    self.player.pos.x += PLAYER_SPEED * self.player.game.dt * 12
                        
                # dash hitbox moves along with player during the duration of the dash (appears only when doing the moving)
                self.player.dash_rect = pg.Rect(self.player.pos.x - TILESIZE, self.player.pos.y - TILESIZE, TILESIZE * 2, TILESIZE * 2)
        
        self.player.effects_trail()

        # exit dash state when dash ends
        if self.dash_slash_end_freeze_length.ready():
            self.exit()
            print("dash done")
            self.player.state_machine.transition("fly")
