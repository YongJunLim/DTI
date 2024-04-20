import pygame
from sys import exit
from random import randint, choice
import game_constants
import os
from PIL import Image
import Encoder

PLAYER_MOVEMENT = (
    game_constants.HEIGHT // (game_constants.REP_INTERVAL * game_constants.FRAMERATE // 1.5)
)
PLAYER_UPDATE_INCREMENT = 0.5
# approx move across screen width in one rep interval
OBSTACLE_MOVEMENT = (
    game_constants.WIDTH // (game_constants.REP_INTERVAL * game_constants.FRAMERATE // 1.5)
)

# will re-declare again
ENC_INITIAL = game_constants.INITIAL
SORTED_WALK_RANGE = sorted((game_constants.WALK + ENC_INITIAL,ENC_INITIAL + 20))
ENC_WALK_VALUES = tuple(range(*SORTED_WALK_RANGE))
ENC_FLY_MIN = game_constants.LIFT + ENC_INITIAL # must be more negative than this value ton fly up

class Player(pygame.sprite.Sprite):
    def __init__(self, enc):
        super().__init__()
        pilImage = Image.open(game_constants.PLAYER_WALKING_IMAGES[0])
        player_walk_1 = pygame.image.frombytes(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()
        player_walk_1 = pygame.transform.rotozoom(player_walk_1, 0, 2)
        pilImage = Image.open(game_constants.PLAYER_WALKING_IMAGES[1])
        player_walk_2 = pygame.image.frombytes(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()
        player_walk_2 = pygame.transform.rotozoom(player_walk_2, 0, 2)
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        pilImage = Image.open(game_constants.PLAYER_FLYING_IMAGE)
        self.player_fly = pygame.image.frombytes(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()
        self.player_fly = pygame.transform.rotozoom(self.player_fly, 0, 2)
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=
            (game_constants.PLAYER_MIDBOTTOM_X, game_constants.PLAYER_MIDBOTTOM_Y)
        ) # point at the center of the bottom of the rectangle.

        self.enc = enc

    def player_input(self):
        # towards red/key: negative/upwards
        # towards ground/black: positive/downwards
        new_enc_pos = self.enc.read()
        if new_enc_pos in ENC_WALK_VALUES and self.rect.bottom <= game_constants.PLAYER_MIDBOTTOM_Y: # fly down
            self.rect.y += PLAYER_MOVEMENT
        elif new_enc_pos <= ENC_FLY_MIN and self.rect.top >= game_constants.SKY_UPPER_Y: # fly up
            self.rect.y -= PLAYER_MOVEMENT

    def player_reset(self):
        print("resetted")
        self.player_index = 0
        self.rect.bottom = game_constants.PLAYER_MIDBOTTOM_Y
        self.ducking = False
        self.image = self.player_walk[self.player_index]
    
    def animation_state(self):
        if self.rect.bottom < game_constants.PLAYER_MIDBOTTOM_Y:
            self.image = self.player_fly
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): 
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'horizontal':
            obstacle = game_constants.HORIZONTAL_OBSTACLE_IMG_PATH
            y_pos = game_constants.HEIGHT - 130
        elif type == 'vertical':
            obstacle = game_constants.VERTICAL_OBSTACLE_IMG_PATH
            y_pos = game_constants.HEIGHT
        pilImage = Image.open(obstacle)
        obstacle_img = pygame.image.frombytes(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()
        # obstacle_img = pygame.transform.rotozoom(obstacle_img, 0, 1.5)
        self.animation_index = 0
        self.image = obstacle_img
        self.rect = self.image.get_rect(midbottom=(game_constants.WIDTH, y_pos))

    def update(self):
        self.rect.x -= OBSTACLE_MOVEMENT

    def destroy(self):
        # if self.rect.x < -30:
        print("despawning obstacle")
        self.kill()

def obstacle_status(player, obstacle_group):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        print("collided")
        player.sprite.player_reset()
        obstacle_group.empty()
        return "collided"
    else:
        for obstacle in obstacle_group:
            if obstacle.rect.left < player.sprite.rect.left - 100:
                obstacle.destroy()
                obstacle_group.empty()
                return "passed"
    return False

def intermission_screen(screen, purpose, seconds_left, score, completed_sets=0):
    pilImage = Image.open('graphics/player/idle/idle1.png')
    player_stand = pygame.image.frombytes(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 3)
    player_stand_rect = player_stand.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 + 20))

    screen.fill(game_constants.INTERMISSION_BG_COLOR)
    screen.blit(player_stand, player_stand_rect)

    title_font = pygame.font.Font(game_constants.HONK_FONT, game_constants.TITLE_FONT_SIZE)
    text_font = pygame.font.Font(game_constants.HONK_FONT, game_constants.TEXT_FONT_SIZE)
    game_name = title_font.render(game_constants.GAME_NAME, False, game_constants.TEXT_FONT_COLOUR)
    game_name_rect = game_name.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 - 150))

    if purpose == "introduction":
        if seconds_left == game_constants.START_GAME_INTERVAL:
            game_message = text_font.render(f'Gently lift log for {seconds_left} seconds to start', False, game_constants.TEXT_FONT_COLOUR)
        else:
            game_message = text_font.render(f'Gently lift log for {seconds_left} more seconds to start', False, game_constants.TEXT_FONT_COLOUR)
        game_message_rect = game_message.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 + 150))
    elif purpose == "rest":
        status_exercise_set = text_font.render(f'Sets completed: {completed_sets}', False, game_constants.TEXT_FONT_COLOUR)
        status_exercise_set_rect = status_exercise_set.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 - 100))
        game_message = text_font.render(f'Resting for {seconds_left} more seconds ...', False, game_constants.TEXT_FONT_COLOUR)
        game_message_rect = game_message.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 + 150))
        screen.blit(status_exercise_set, status_exercise_set_rect)
    if score is not None:
        if score == (game_constants.NUM_SETS * game_constants.NUM_REPS):
            game_completion_status =  text_font.render(f'GAME COMPLETED', False, game_constants.TEXT_FONT_COLOUR)
        else:
            game_completion_status =  text_font.render(f'GAME OVER', False, game_constants.TEXT_FONT_COLOUR)
        game_score = text_font.render(f'Score: {score}', False, game_constants.TEXT_FONT_COLOUR)
        game_score_rect = game_score.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 - 100))
        game_completion_status_rect =  game_completion_status.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 - 50))
        screen.blit(game_score, game_score_rect)
        screen.blit(game_completion_status, game_completion_status_rect)
    # if score is not None:
    #     game_score = text_font.render(f'Score: {score}', False, game_constants.TEXT_FONT_COLOUR)
    #     game_score_rect = game_score.get_rect(center=(game_constants.WIDTH // 2, game_constants.HEIGHT // 2 - 100))
    #     screen.blit(game_score, game_score_rect)

    screen.blit(game_name, game_name_rect)
    screen.blit(game_message, game_message_rect)

def display_score(completed_sets, completed_reps):
    score_font = pygame.font.Font(game_constants.HONK_FONT, game_constants.TITLE_FONT_SIZE)
    score_surf = score_font.render(f'Set {completed_sets + 1} of {game_constants.NUM_SETS}: Rep {completed_reps} of {game_constants.NUM_REPS}', 
        False, game_constants.SCORE_FONT_COLOUR)
    score_rect = score_surf.get_rect(center=(400, 50))
    return score_surf, score_rect

def show_text_transition():
    pygame.display.update()
    pygame.time.wait(int(game_constants.TIME_DELAY * 1000))
    
def main():
    pygame.init()
    screen = pygame.display.set_mode([game_constants.WIDTH, game_constants.HEIGHT])
    surface = pygame.Surface((game_constants.WIDTH, game_constants.HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption(game_constants.GAME_NAME)

    pilImage = Image.open(f'{game_constants.PARENT_FOLDER}/graphics/Game Background.png')
    background = pygame.image.frombytes(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()
    background = pygame.transform.rotozoom(background, 0, 3)
    bg_color = (128, 128, 128)

    clock = pygame.time.Clock()
    countdown_event = pygame.USEREVENT
    obstacle_event = pygame.USEREVENT + 1
    rest_event = pygame.USEREVENT + 2
    pygame.time.set_timer(countdown_event, 1000)
    start_game_countdown = game_constants.START_GAME_INTERVAL

    game_active = False
    game_over = False
    game_rest = False

    score = None
    completed_sets = 0
    completed_reps = 0

    enc = Encoder.Encoder(game_constants.S1, game_constants.S2)

    player = pygame.sprite.GroupSingle()
    playerSprite = Player(enc)
    player.add(playerSprite)
    obstacle_group = pygame.sprite.Group()
    obstacle_iterator = 1 #randint(0,1)

    ENC_INITIAL = game_constants.INITIAL
    SORTED_WALK_RANGE = sorted((game_constants.WALK + ENC_INITIAL,ENC_INITIAL + 20))
    ENC_WALK_VALUES = tuple(range(*SORTED_WALK_RANGE))
    ENC_FLY_MIN = game_constants.LIFT + ENC_INITIAL # must be more negative than this value ton fly up

    while True:
        print(enc.read(), ENC_INITIAL, SORTED_WALK_RANGE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if game_active:
                if event.type == obstacle_event:
                    print("Spawning obstacle")
                    if obstacle_iterator == 0:
                        obstacle_group.add(Obstacle('horizontal'))
                        obstacle_iterator = 1
                    elif obstacle_iterator == 1:
                        obstacle_group.add(Obstacle('vertical'))
                        obstacle_iterator = 0
            elif game_rest: # but not game_active
                if event.type == countdown_event:
                    rest_countdown -= 1
            else:
                # towards red/key: negative
                # towards ground/black: positive
                # bring up to your neutral height
                ACTIVATE_RANGE = tuple(range(ENC_INITIAL - 5, ENC_INITIAL + 5))
                curr_enc_pos = enc.read()
                if enc.read() in ACTIVATE_RANGE and curr_enc_pos != ENC_INITIAL and event.type == countdown_event:
                    start_game_countdown -= 1

        if game_active:
            screen.blit(background, (0, 0))
            status = obstacle_status(player, obstacle_group)
            if status == "collided":
                game_active = False
                show_text_transition()
                score = completed_sets * game_constants.NUM_REPS + completed_reps
                completed_sets = 0
                completed_reps = 0
                start_game_countdown = game_constants.START_GAME_INTERVAL
                pygame.time.set_timer(obstacle_event, 0)
                pygame.time.set_timer(countdown_event, 1000)
            elif status == "passed":
                completed_reps += 1

            if completed_reps == game_constants.NUM_REPS:
                score_surf, score_rect = display_score(completed_sets, completed_reps)
                screen.blit(score_surf, score_rect)
                show_text_transition()
                completed_sets += 1
                if completed_sets == game_constants.NUM_SETS:
                    game_active = False
                    game_rest = False
                    score = completed_sets * game_constants.NUM_REPS
                    completed_sets = 0
                    completed_reps = 0
                    start_game_countdown = game_constants.START_GAME_INTERVAL
                else:
                    rest_countdown = game_constants.REST_INTERVAL
                    game_rest = True
                    game_active = False
                    completed_reps = 0
                pygame.time.set_timer(obstacle_event, 0)
                pygame.time.set_timer(countdown_event, 1000)

            score_surf, score_rect = display_score(completed_sets, completed_reps)
            screen.blit(score_surf, score_rect)

            player.draw(screen)
            player.update()
            
            obstacle_group.draw(screen)
            obstacle_group.update()

        elif game_rest:
            if rest_countdown == 0:
                ENC_INITIAL = enc.read()
                SORTED_WALK_RANGE = sorted((game_constants.WALK + ENC_INITIAL,ENC_INITIAL + 20))
                ENC_WALK_VALUES = tuple(range(*SORTED_WALK_RANGE))
                ENC_FLY_MIN = game_constants.LIFT + ENC_INITIAL # must be more negative than this value ton fly up
                intermission_screen(screen, "rest", rest_countdown, None, completed_sets)
                show_text_transition()
                game_active = True
                game_rest = False
                player.sprite.player_reset()
                pygame.time.set_timer(countdown_event, 0) # disabled
                pygame.time.set_timer(obstacle_event, int(game_constants.REP_INTERVAL * 1000))
            intermission_screen(screen, "rest", rest_countdown, None, completed_sets)
        else:
            if start_game_countdown == 0:
                ENC_INITIAL = enc.read()
                SORTED_WALK_RANGE = sorted((game_constants.WALK + ENC_INITIAL,ENC_INITIAL + 20))
                ENC_WALK_VALUES = tuple(range(*SORTED_WALK_RANGE))
                ENC_FLY_MIN = game_constants.LIFT + ENC_INITIAL # must be more negative than this value ton fly up
                intermission_screen(screen, "introduction", start_game_countdown, score)
                show_text_transition()
                game_active = True
                pygame.time.set_timer(countdown_event, 0) # disabled
                pygame.time.set_timer(obstacle_event, int(game_constants.REP_INTERVAL * 1000))
            intermission_screen(screen, "introduction", start_game_countdown, score)

        pygame.display.update()
        clock.tick(game_constants.FRAMERATE)
        print(clock.get_fps())

if __name__ == "__main__":
    main()
