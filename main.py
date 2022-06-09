import pygame
from pygame import mixer

pygame.init()  # initializes all the imported pygame modules

# screen size
width = 1400
height = 800
screen = pygame.display.set_mode([width, height])  # declaring screen size
pygame.display.set_caption("Beat Creator")
fps = 60
timer = pygame.time.Clock()  # control the speed of game

# colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (180, 180, 180)
dark_gray = (28, 28, 28)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

boxes = []
default_beats = 8
instruments = 6
clicked = [[-1 for _ in range(default_beats)] for _ in range(instruments)]
active_instruments = [1 for _ in range(instruments)]

index = 100
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)
bpm = 240  # bpm -> beats per minute. Here it's 4 beats per sec
is_playing = True
active_length = 0  # the beat that we are currently on is active
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for val in file:
    saved_beats.append(val)
beat_name = ''
is_typing = False

# loading sounds
hi_hat = mixer.Sound("sounds/hi hat.WAV")
clap = mixer.Sound("sounds/clap.wav")
crash = mixer.Sound("sounds/crash.wav")
bass_drum = mixer.Sound("sounds/kick.WAV")
snare = mixer.Sound("sounds/snare.WAV")
floor_tom = mixer.Sound("sounds/tom.WAV")
# sounds_list = [hi_hat, snare, bass_drum, crash, clap, floor_tom]
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_instruments[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                bass_drum.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                floor_tom.play()


def play_pause_buttons():
    button = pygame.draw.rect(screen, gray, [50, height - 150, 200, 100], 0, 5)
    button_text = label_font.render('Play/Pause', True, white)
    screen.blit(button_text, (70, height - 130))
    if is_playing:
        button_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        button_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(button_text2, (100, height - 100))
    return button


def beats_per_minute_button():
    # creating button
    button = pygame.draw.rect(screen, gray, [300, height - 150, 200, 100], 5, 5)
    button_text = medium_font.render("Beats per Minute", True, white)
    screen.blit(button_text, (308, height - 130))

    # printing the existing bpm value on screen
    bpm_value = label_font.render(f"{bpm}", True, white)
    screen.blit(bpm_value, (370, height - 100))

    # creating increment/decrement buttons
    add = pygame.draw.rect(screen, gray, [505, height - 150, 48, 48], 0, 5)
    add_button_text = medium_font.render('+5', True, white)
    screen.blit(add_button_text, (520, height - 140))

    sub = pygame.draw.rect(screen, gray, [505, height - 100, 48, 48], 0, 5)
    sub_button_text = medium_font.render('-5', True, white)
    screen.blit(sub_button_text, (520, height - 90))

    return add, sub


def beats_button():
    # creating button
    button = pygame.draw.rect(screen, gray, [600, height - 150, 200, 100], 5, 5)
    button_text = medium_font.render('Beats in Loop', True, white)
    screen.blit(button_text, (625, height - 130))

    # printing the existing beats value on screen
    beats_value = label_font.render(f'{default_beats}', True, white)
    screen.blit(beats_value, (680, height - 100))

    # creating increment/decrement buttons
    add = pygame.draw.rect(screen, gray, [805, height - 150, 48, 48], 0, 5)
    add_button_text = medium_font.render('+1', True, white)
    screen.blit(add_button_text, (820, height - 140))

    sub = pygame.draw.rect(screen, gray, [805, height - 100, 48, 48], 0, 5)
    sub_button_text = medium_font.render('-1', True, white)
    screen.blit(sub_button_text, (820, height - 90))

    return add, sub


def load_save_button():
    l_button = pygame.draw.rect(screen, gray, [900, height - 150, 180, 48], 0, 5)
    load_button_text = label_font.render('Load Beat', True, white)
    screen.blit(load_button_text, (920, height - 140))

    s_button = pygame.draw.rect(screen, gray, [900, height - 100, 180, 48], 0, 5)
    save_button_text = label_font.render('Save Beat', True, white)
    screen.blit(save_button_text, (920, height - 90))

    return l_button, s_button


def clear_button():
    c_button = pygame.draw.rect(screen, gray, [1100, height - 150, 200, 100], 0, 5)
    clear_button_text = label_font.render('Clear Board', True, white)
    screen.blit(clear_button_text, (1115, height - 120))
    return c_button


def draw_grid(clicks, beat, active_instru):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, height - 200], 3)
    bottom_box = pygame.draw.rect(screen, gray, [0, height - 200, width, 200], 3)
    box = []
    colors = [gray, white, gray]

    # displaying the instruments on the screen whose color will
    # change depending on whether that channel is turned on/off
    hi_hat_text = label_font.render("Hi-Hat", True, colors[active_instru[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render("Snare", True, colors[active_instru[1]])
    screen.blit(snare_text, (30, 130))
    bass_drum_text = label_font.render("Bass Drum", True, colors[active_instru[2]])
    screen.blit(bass_drum_text, (30, 230))
    crash_text = label_font.render("Crash", True, colors[active_instru[3]])
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render("Clap", True, colors[active_instru[4]])
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render("Floor-Tom", True, colors[active_instru[5]])
    screen.blit(floor_tom_text, (30, 530))

    # drawing line for separating the instruments
    for line in range(0, instruments + 1):
        pygame.draw.line(screen, gray, (0, line * 100), (200, line * 100), 3)

    # creating grid
    for i in range(default_beats):  # we are looping column-wise
        for j in range(instruments):
            if clicks[j][i] == -1:  # 'j' is row here and 'i' is column
                color = gray
            else:
                if active_instruments[j] == 1:
                    color = green
                else:
                    color = dark_gray
            # this one is the actual rectangle which will change
            rect = pygame.draw.rect(screen, color, [i * ((width - 200) // default_beats) + 200, (j * 100) + 5,
                                                    ((width - 200) // default_beats) - 10,
                                                    ((height - 200) // instruments) - 10], 0, 3)
            #  this is used to add a padding of gold inside the outer rectangle
            pygame.draw.rect(screen, gold, [i * ((width - 200) // default_beats) + 200, (j * 100),
                                            ((width - 200) // default_beats), ((height - 200) // instruments)], 5, 5)
            #  the actual outer rectangle which act as a boundary
            pygame.draw.rect(screen, black, [i * ((width - 200) // default_beats) + 200, (j * 100),
                                             ((width - 200) // default_beats), ((height - 200) // instruments)], 2, 5)
            box.append((rect, (j, i)))  # similarly here 'j' is row and 'i' is column
        # creating the beat tracker marker
        active = pygame.draw.rect(screen, blue,
                                  [beat * ((width - 200) // default_beats) + 200, 0, ((width - 200) // default_beats),
                                   instruments * 100], 6, 3)

    return box


def draw_save_menu(name_of_beats, typing):
    # creating new window for save menu
    pygame.draw.rect(screen, black, [0, 0, width, height])
    # creating text message
    text_msg = label_font.render('SAVE MENU: Enter a name for Current Beat', True, white)
    screen.blit(text_msg, (400, 40))
    # creating a current beat saver button
    saving_btn = pygame.draw.rect(screen, gray, [width // 2 - 200, height * 0.75, 400, 100], 0, 5)
    saving_txt = label_font.render('Save Beat', True, white)
    screen.blit(saving_txt, (width // 2 - 70, height * 0.75 + 30))
    # creating close button
    exit_btn = pygame.draw.rect(screen, gray, [width - 200, height - 100, 180, 90], 0, 5)
    exit_btn_text = label_font.render('Close', True, white)
    screen.blit(exit_btn_text, (width - 160, height - 70))
    # creating entry box for input names
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_rect_txt = label_font.render(f'{name_of_beats}', True, white)
    screen.blit(entry_rect_txt, (430, 250))
    return entry_rect, saving_btn, exit_btn, name_of_beats


def draw_load_menu(index):
    loaded_beats = 0
    loaded_bpm = 0
    loaded_clicked = []
    # creating new window for load menu
    pygame.draw.rect(screen, black, [0, 0, width, height])
    # creating load text message
    text_msg = label_font.render('LOAD MENU: Select a Beat File to Load', True, white)
    screen.blit(text_msg, (400, 40))
    # creating the menu box containing previous saved beats
    menu_box_rect = pygame.draw.rect(screen, gray, [200, 90, 1000, 600], 5, 5)
    # creating a mark on the selected beat
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, light_gray, [210, 100 + index * 50, 980, 40])
    for beat in range(len(saved_beats)):
        # for displaying indexes and beat names of the saved beats
        if beat < 10:
            beat_clicked = []
            # displaying indexes
            beat_idx = medium_font.render(f'{beat + 1}.', True, white)
            screen.blit(beat_idx, (210, 100 + beat * 50))
            # displaying beat name
            name_index_start = saved_beats[beat].index("name: ") + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        # loading the beat on the console which we clicked
        if 0 <= index < len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 8:beat_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat][beat_index_end + 6: bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split('], ['))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]

    # creating a loading button
    loading_btn = pygame.draw.rect(screen, gray, [width // 2 - 200, height * 0.87, 400, 100], 0, 5)
    loading_txt = label_font.render('Load Beat', True, white)
    screen.blit(loading_txt, (width // 2 - 70, height * 0.87 + 30))
    # creating the  delete button
    delete_btn = pygame.draw.rect(screen, gray, [width // 2 - 500, height * 0.87, 200, 100], 0, 5)
    delete_btn_txt = label_font.render('Delete Beat', True, white)
    screen.blit(delete_btn_txt, (width // 2 - 485, height * 0.87 + 30))
    # creating the close button
    exit_btn = pygame.draw.rect(screen, gray, [width - 200, height - 100, 180, 90], 0, 5)
    exit_btn_text = label_font.render('Close', True, white)
    screen.blit(exit_btn_text, (width - 160, height - 70))
    return exit_btn, loading_btn, delete_btn, menu_box_rect, loaded_info


is_running = True

while is_running:
    timer.tick(fps)  # will execute the code on a rate of 60 fps
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_instruments)

    # CREATING LOWER MENU BUTTONS:

    # creating instruments buttons
    instruments_button = []
    for i in range(instruments):
        button_rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instruments_button.append(button_rect)

    # creating play/pause button
    play_pause = play_pause_buttons()  # play/pause button

    # creating BPM add/subtract buttons (bpm -> beats per minute)
    add_bpm_button, sub_bpm_button = beats_per_minute_button()

    # creating beats add/subtract button
    add_beats_button, sub_beats_button = beats_button()

    # creating load/save button
    load_button, save_button = load_save_button()

    # creating clear button
    clear = clear_button()

    # creating save/load menu window
    if save_menu:
        entry_rectangle, saving_button, exit_button, beat_name = draw_save_menu(beat_name, is_typing)
    if load_menu:
        exit_button, loading_button, delete_button, entry_rectangle, loaded_information = draw_load_menu(index)

    # playing notes
    if beat_changed:
        play_notes()
        beat_changed = False

    # Configuring mouse inputs
    for event in pygame.event.get():
        # event handling -> manages all the even or inputs from the keyboard
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:

            # mark the clicked boxes
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coordinates = boxes[i][1]
                    clicked[coordinates[0]][coordinates[1]] *= -1

        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:

            # checking if play/pause button got pressed
            if play_pause.collidepoint(event.pos):
                if is_playing:
                    is_playing = False
                elif not is_playing:
                    is_playing = True
                    active_beat = 0
                    active_length = 0

            # checking if add/subtract button of bpm got pressed
            if add_bpm_button.collidepoint(event.pos):
                bpm += 5
            elif sub_bpm_button.collidepoint(event.pos):
                bpm -= 5

            # checking if the add/subtract button of beats got pressed
            if add_beats_button.collidepoint(event.pos):
                default_beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif sub_beats_button.collidepoint(event.pos):
                default_beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)

            # checking whether clear button got pressed
            if clear.collidepoint(event.pos):
                clicked = [[-1 for _ in range(default_beats)] for _ in range(instruments)]

            # checking whether save_button/load_button got pressed
            if save_button.collidepoint(event.pos):
                save_menu = True
            if load_button.collidepoint(event.pos):
                load_menu = True
                is_playing = False

            # checking whether instrument button is pressed to turn off that channel
            for i in range(len(instruments_button)):
                if instruments_button[i].collidepoint(event.pos):
                    active_instruments[i] *= -1

        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                is_playing = True
                beat_name = ''
                is_typing = False

            if entry_rectangle.collidepoint(event.pos):  # it tells us where we clicked on the y axis in menu rectangle
                if save_menu:
                    if is_typing:
                        is_typing = False
                    else:
                        is_typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50
            if save_menu:
                if saving_button.collidepoint(event.pos):
                    file = open('saved_beats.txt', 'w')
                    saved_beats.append(f'\nname: {beat_name}, beats: {default_beats}, bpm: {bpm}, selected: {clicked}')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    is_playing = True
                    beat_name = ''
                    is_typing = False
            if load_menu:
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        default_beats = loaded_information[0]
                        bpm = loaded_information[1]
                        clicked = loaded_information[2]
                        index = 100
                        save_menu = False
                        load_menu = False
                        is_playing = True
                        is_typing = False
        if event.type == pygame.TEXTINPUT and is_typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0:
                beat_name = beat_name[:-1]

    # to add a moving beat tracker
    beat_length = fps * 60 // bpm

    if is_playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < default_beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()  # prints all the thing on screen

file = open('saved_beats.txt', 'w')
for i in range(len(saved_beats)):
    file.write(str(saved_beats[i]))
file.close()
pygame.quit()