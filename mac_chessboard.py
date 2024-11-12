import cv2
import numpy as np
import pygame
import sys
from screeninfo import get_monitors
from PIL import ImageGrab, Image
import os
import datetime
import Quartz
import Quartz.CoreGraphics as CG

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                             User Guide                            #
#  Version : Check Git History                                      #
#  Made By : Jongho                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                   #
#  Number = Pattern                                                 #
#                                                                   #
#  0 : "HwaSung Single A",                                          #
#  1 : "HwaSung Single B",                                          #
#  2 : "HwaSung Single C",                                          #
#  3 : "PDI 2 Double",                                              #
#  4 : "PDI 3 Single",                                              #
#  5 : "AS Origninal",                                              #
#  6 : "AS x + 3",                                                  #
#  7 : "AS x - 3",                                                  #
#  8 : "AS y + 3",                                                  #
#  9 : "AS y - 3"                                                   #
#                                                                   #
#  + : Zoom In                                                      #
#  - : Zoom Out                                                     #
#                                                                   #
#  Moving Pattern : Key_Left, Key_Right, Key_Up, Key_Down           #
#                                                                   #
#  ScreenShot : Key_SpaceBar                                        #
#                                                                   #
#  Border Gap : Space Between Left ChessBoard & Right ChessBoard    #
#                                                                   #
#  ChessBoard Width, ChessBoard Height : Due to Display resolution, #
#  Square != exact Square. Need to adjust Width and Height manualy. #
#                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Creating ChessBoard, Height = Width = square_size
#
# def create_chessboard(rows=5, cols=2, square_size=50, top_left_black=True, AS_pattern=None):
#     if AS_pattern is not None:
#         rows, cols = len(AS_pattern), len(AS_pattern[0])
#         chessboard = np.ones((rows * square_size, cols * square_size), dtype=np.uint8) * 255
#         for i in range(rows):
#             for j in range(cols):
#                 color = 0 if AS_pattern[i][j] == 0 else 255
#                 chessboard[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = color
#     else:
#         chessboard = np.ones((rows * square_size, cols * square_size), dtype=np.uint8) * 255
#         for i in range(rows):
#             for j in range(cols):
#                 if (i + j) % 2 == 0:
#                     color = 0 if top_left_black else 255
#                 else:
#                     color = 255 if top_left_black else 0
#                 chessboard[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = color
#     return chessboard

# Global Variable
mode_names = {
    0: "HwaSung Single A", # Size Done, Height needs to be adjust 160
    1: "HwaSung Single B", # Size Done, Height needs to be adjust 160
    2: "HwaSung Single C", # Size Done, Height needs to be adjust 160
    3: "PDI 2 Double", # Size Done, Height needs to be adjust 75
    4: "PDI 3 Single", # Need to start Size and Height
    5: "AS Origninal", # Done 50
    6: "AS x + 3", # Done 50
    7: "AS x - 3", # Done 50
    8: "AS y + 3", # Done 50
    9: "AS y - 3" # Done 50
}

Folder_flag = [False]

# Creating ChessBoard, Custom Height & Width 
def create_chessboard(rows=5, cols=2, square_width=50, square_height=50, top_left_black=True, AS_pattern=None):
    if AS_pattern is not None:
        rows, cols = len(AS_pattern), len(AS_pattern[0])
        chessboard = np.ones((rows * square_height, cols * square_width), dtype=np.uint8) * 255
        for i in range(rows):
            for j in range(cols):
                color = 0 if AS_pattern[i][j] == 0 else 255
                chessboard[i * square_height:(i + 1) * square_height, j * square_width:(j + 1) * square_width] = color
    else:
        chessboard = np.ones((rows * square_height, cols * square_width), dtype=np.uint8) * 255
        for i in range(rows):
            for j in range(cols):
                if (i + j) % 2 == 0:
                    color = 0 if top_left_black else 255
                else:
                    color = 255 if top_left_black else 0
                chessboard[i * square_height:(i + 1) * square_height, j * square_width:(j + 1) * square_width] = color
    return chessboard

# Move Chessboard & Scaling
def move_and_resize_image(image, x_offset, y_offset, scale, canvas_width, canvas_height):
    resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
    canvas = np.ones((canvas_height, canvas_width), dtype=np.uint8) * 255
    h, w = resized_image.shape
    x_start = max(0, min(canvas.shape[1] - w, x_offset))
    y_start = max(0, min(canvas.shape[0] - h, y_offset))
    canvas[y_start:y_start + h, x_start:x_start + w] = resized_image
    return canvas

# ScreenShot Added # 11_12_24 - jongho
def screenshot(current_mode, flag):
    i = 1
    if flag[0] == False:
        flag[0] = True
        global making_folder_dir 
        making_folder_dir = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
        os.makedirs(making_folder_dir)
        
        current_dir = os.getcwd()
        os.chdir(f"{current_dir}/{making_folder_dir}")

    while os.path.exists(f"{mode_names[current_mode]}_{i}.png"):
        i += 1
    img = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
    img.save(f"{mode_names[current_mode]}_{i}.png")
    print(f"Saved {mode_names[current_mode]}_{i}.png")

# Main Start
def main():
    pygame.init()
    pygame.font.init()  # Init Font
    font = pygame.font.SysFont(None, 40)  # Init Font Size

    monitors = get_monitors()
    # Getting Monitor Info > extended Monitor Info
    if len(monitors) > 1:
        sub_monitor = monitors[1]
        screen_width = sub_monitor.width  # Extended Monitor Height
        screen_height = sub_monitor.height  # Extended Monitor Width
    else:
        display_info = pygame.display.Info()
        screen_width = display_info.current_w
        screen_height = display_info.current_h

    AS_pattern = [
        [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0],
        [1, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0],
        [1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1],
        [1, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0]
    ]

    chessboard_hwasung_A = create_chessboard(rows=5, cols=2, square_width=199, square_height=201, top_left_black=False) # HwaSung Single A
    chessboard_hwasung_B = create_chessboard(rows=5, cols=2, square_width=199, square_height=201, top_left_black=False) # HwaSung Single B
    chessboard_hwasung_C = create_chessboard(rows=5, cols=2, square_width=199, square_height=201, top_left_black=False) # HwaSung Single C
    chessboard_PDI_3_Single = create_chessboard(rows=5, cols=2, square_width=199, square_height=199, top_left_black=False) # PDI 3 Single
    chessboard_PDI_2_Double_left = create_chessboard(rows=2, cols=3, square_width=94, square_height=93, top_left_black=True) # PDI 2 Double Left
    chessboard_PDI_2_Double_right = create_chessboard(rows=2, cols=3, square_width=94, square_height=93, top_left_black=False) # PDI 2 Double Right
    chessboard_AS = create_chessboard(AS_pattern=AS_pattern, square_width=62, square_height=63) # AS Original
    chessboard_AS_xp3 = create_chessboard(AS_pattern=AS_pattern, square_width=62, square_height=63) # AS x + 3
    chessboard_AS_xm3 = create_chessboard(AS_pattern=AS_pattern, square_width=62, square_height=63) # AS x - 3
    chessboard_AS_yp3 = create_chessboard(AS_pattern=AS_pattern, square_width=62, square_height=63) # AS y + 3
    chessboard_AS_ym3 = create_chessboard(AS_pattern=AS_pattern, square_width=62, square_height=63) # AS y - 3

    screen = pygame.display.set_mode((screen_width, screen_height))

    # Initial value
    mode = 0
    scale = 1.0
    x_offset = (screen_width - chessboard_hwasung_A.shape[1]) // 2
    y_offset = (screen_height - chessboard_hwasung_A.shape[0]) // 2 - 427

    while True:
        screen.fill((255, 255, 255))  # White Background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESCAPE Button = Escape
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()
        
        # Factory & Line Info with key event
        if keys[pygame.K_0]: # HwaSung Single A
            mode = 0
            scale = 1.0
            x_offset = (screen_width - chessboard_hwasung_A.shape[1]) // 2
            y_offset = (screen_height - chessboard_hwasung_A.shape[0]) // 2 - 427 

        if keys[pygame.K_1]: # HwaSung Single B
            mode = 1
            scale = 1.0
            x_offset = (screen_width - chessboard_hwasung_B.shape[1]) // 2
            y_offset = (screen_height - chessboard_hwasung_A.shape[0]) // 2 - 409

        if keys[pygame.K_2]: # HwaSung Single C
            mode = 2
            scale = 1.0
            x_offset = (screen_width - chessboard_hwasung_C.shape[1]) // 2
            y_offset = (screen_height - chessboard_hwasung_C.shape[0]) // 2 - 427 

        if keys[pygame.K_3]: # PDI 2 Double
            mode = 3
            scale = 1.0
            x_offset = (screen_width // 2 - chessboard_PDI_2_Double_left.shape[1]) // 2
            y_offset = (screen_height - chessboard_PDI_2_Double_right.shape[0]) // 8 
            board_gap = -208

        if keys[pygame.K_4]: # PDI 3 Single
            mode = 4
            scale = 1.0
            x_offset = (screen_width - chessboard_PDI_3_Single.shape[1]) // 2
            y_offset = (screen_height - chessboard_PDI_3_Single.shape[0]) // 2 - 198

        if keys[pygame.K_5]: # AS Original
            mode = 5
            scale = 1.0
            x_offset = (screen_width - chessboard_AS.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS.shape[0]) // 2 - 165

        if keys[pygame.K_6]: # AS x + 3
            mode = 6
            scale = 1.0
            x_offset = (screen_width - chessboard_AS_xp3.shape[1]) // 2 + 37
            y_offset = (screen_height - chessboard_AS_xp3.shape[0]) // 2 - 165

        if keys[pygame.K_7]: # AS x - 3
            mode = 7
            scale = 1.0
            x_offset = (screen_width - chessboard_AS_xm3.shape[1]) // 2 - 37
            y_offset = (screen_height - chessboard_AS_xm3.shape[0]) // 2 - 165

        if keys[pygame.K_8]: # AS y + 3
            mode = 8
            scale = 1.0
            x_offset = (screen_width - chessboard_AS_yp3.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS_yp3.shape[0]) // 2 - 165 - 38

        if keys[pygame.K_9]: # AS y - 3
            mode = 9
            scale = 1.0
            x_offset = (screen_width - chessboard_AS_ym3.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS_ym3.shape[0]) // 2 - 165 + 38

        # Mode Event
        if mode == 0: # HwaSung Single A
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1 
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_hwasung_A = move_and_resize_image(chessboard_hwasung_A, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_hwasung_A = cv2.cvtColor(moved_image_hwasung_A, cv2.COLOR_GRAY2RGB)
            moved_image_surface_hwasung_A = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_hwasung_A))
            screen.blit(moved_image_surface_hwasung_A, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 1: # HwaSung Single B
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1 
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_hwasung_B = move_and_resize_image(chessboard_hwasung_B, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_hwasung_B = cv2.cvtColor(moved_image_hwasung_B, cv2.COLOR_GRAY2RGB)
            moved_image_surface_hwasung_B = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_hwasung_B))
            screen.blit(moved_image_surface_hwasung_B, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 2: # HwaSung Single C
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_hwasung_C = move_and_resize_image(chessboard_hwasung_C, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_hwasung_C = cv2.cvtColor(moved_image_hwasung_C, cv2.COLOR_GRAY2RGB)
            moved_image_surface_hwasung_C = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_hwasung_C))
            screen.blit(moved_image_surface_hwasung_C, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 3: # PDI 2 Double
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_o]:  # Increase DIstance between Inner Chess Board
                board_gap += 1
            if keys[pygame.K_p]:  # Decrease DIstance between Inner Chess Board
                board_gap -= 1
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)    

            # Left Chessboard
            moved_image_PDI_2_Double_left = move_and_resize_image(chessboard_PDI_2_Double_left, x_offset - board_gap, y_offset, scale, screen_width // 2, screen_height)
            moved_image_rgb_PDI_2_Double_left = cv2.cvtColor(moved_image_PDI_2_Double_left, cv2.COLOR_GRAY2RGB)
            moved_image_surface_PDI_2_Double_left = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_PDI_2_Double_left))
            screen.blit(moved_image_surface_PDI_2_Double_left, (0, screen_height // 4))  # Align to Center H Line

            # Right Chessboard
            moved_image_PDI_2_Double_right = move_and_resize_image(chessboard_PDI_2_Double_right, x_offset + board_gap, y_offset, scale, screen_width // 2, screen_height)
            moved_image_rgb_PDI_2_Double_right = cv2.cvtColor(moved_image_PDI_2_Double_right, cv2.COLOR_GRAY2RGB)
            moved_image_surface_PDI_2_Double_right = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_PDI_2_Double_right))
            screen.blit(moved_image_surface_PDI_2_Double_right, (screen_width // 2, screen_height // 4))  # Align to Center H Line

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 4: # PDI 3 Single
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1 
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_PDI_3_Single = move_and_resize_image(chessboard_PDI_3_Single, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_PDI_3_Single = cv2.cvtColor(moved_image_PDI_3_Single, cv2.COLOR_GRAY2RGB)
            moved_image_surface_PDI_3_Single = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_PDI_3_Single))
            screen.blit(moved_image_surface_PDI_3_Single, (0, 0))    

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 5: # AS Original
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_AS = move_and_resize_image(chessboard_AS, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_AS = cv2.cvtColor(moved_image_AS, cv2.COLOR_GRAY2RGB)
            moved_image_surface_AS = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_AS))
            screen.blit(moved_image_surface_AS, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 6: # AS x + 3
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_AS_xp3 = move_and_resize_image(chessboard_AS_xp3, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_AS_xp3 = cv2.cvtColor(moved_image_AS_xp3, cv2.COLOR_GRAY2RGB)
            moved_image_surface_AS_xp3 = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_AS_xp3))
            screen.blit(moved_image_surface_AS_xp3, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 7: # AS x - 3
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_AS_xm3 = move_and_resize_image(chessboard_AS_xm3, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_AS_xm3 = cv2.cvtColor(moved_image_AS_xm3, cv2.COLOR_GRAY2RGB)
            moved_image_surface_AS_xm3 = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_AS_xm3))
            screen.blit(moved_image_surface_AS_xm3, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 8: # AS y + 3
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)
                
            moved_image_AS_yp3 = move_and_resize_image(chessboard_AS_yp3, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_AS_yp3 = cv2.cvtColor(moved_image_AS_yp3, cv2.COLOR_GRAY2RGB)
            moved_image_surface_AS_yp3 = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_AS_yp3))
            screen.blit(moved_image_surface_AS_yp3, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        elif mode == 9: # AS y - 3
            if keys[pygame.K_LEFT]:
                x_offset += 1
            if keys[pygame.K_RIGHT]:
                x_offset -= 1
            if keys[pygame.K_UP]:
                y_offset -= 1
            if keys[pygame.K_DOWN]:
                y_offset += 1
            if keys[pygame.K_EQUALS]:  # '+' = Bigger Size
                scale += 0.001
            if keys[pygame.K_MINUS]:  # '-' = Smaller Size
                scale -= 0.001
            if keys[pygame.K_SPACE]:
                screenshot(mode,Folder_flag)

            moved_image_AS_ym3 = move_and_resize_image(chessboard_AS_ym3, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_AS_ym3 = cv2.cvtColor(moved_image_AS_ym3, cv2.COLOR_GRAY2RGB)
            moved_image_surface_AS_ym3 = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_AS_ym3))
            screen.blit(moved_image_surface_AS_ym3, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner

        # Updating Screen
        pygame.display.update()

if __name__ == "__main__":
    main()