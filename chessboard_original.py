import cv2
import numpy as np
import pygame
import sys
from screeninfo import get_monitors

# Creating Chessboard
def create_chessboard(rows=5, cols=2, square_size=50, top_left_black=True, AS_pattern=None):
    if AS_pattern is not None:
        rows, cols = len(AS_pattern), len(AS_pattern[0])
        chessboard = np.ones((rows * square_size, cols * square_size), dtype=np.uint8) * 255
        for i in range(rows):
            for j in range(cols):
                color = 0 if AS_pattern[i][j] == 0 else 255
                chessboard[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = color
    else:
        chessboard = np.ones((rows * square_size, cols * square_size), dtype=np.uint8) * 255
        for i in range(rows):
            for j in range(cols):
                if (i + j) % 2 == 0:
                    color = 0 if top_left_black else 255
                else:
                    color = 255 if top_left_black else 0
                chessboard[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = color
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

print("HI")

# Drawing Line on ChessBoard >> Working on it
def draw_transparent_line(surface, start_pos, end_pos, color, alpha):
    temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.line(temp_surface, (*color, alpha), start_pos, end_pos, 5)
    surface.blit(temp_surface, (0, 0))

def main():
    pygame.init()
    pygame.font.init()  # Init Font
    font = pygame.font.SysFont(None, 24)  # Init Font Size

    monitors = get_monitors()

    """
    # Getting Monitor Info > extended Monitor Info
    if len(monitors) > 1:
        sub_monitor = monitors[1]
        screen_width = sub_monitor.width  # Extended Monitor Height
        screen_height = sub_monitor.height  # Extended Monitor Width
    else:
        display_info = pygame.display.Info()
        screen_width = display_info.current_w
        screen_height = display_info.current_h
    """

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    
    AS_pattern = [
        [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0],
        [1, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0],
        [1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1],
        [1, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0]
    ]

    mode_names = {
        0: "HwaSung Single A",
        1: "HwaSung Single B",
        2: "HwaSung Single C",
        3: "PDI 2 Double",
        4: "PDI 3 Single",
        5: "AS Origninal",
        6: "AS x + 3",
        7: "AS x - 3",
        8: "AS y + 3",
        9: "AS y - 3"
    }

    chessboard_hwasung_A = create_chessboard(rows=5, cols=2, square_size=199, top_left_black=False) # HwaSung Single A
    chessboard_hwasung_B = create_chessboard(rows=5, cols=2, square_size=125, top_left_black=False) # HwaSung Single B
    chessboard_hwasung_C = create_chessboard(rows=5, cols=2, square_size=199, top_left_black=False) # HwaSung Single C
    chessboard_PDI_3_Single = create_chessboard(rows=5, cols=2, square_size=199, top_left_black=False) # PDI 3 Single
    chessboard_PDI_2_Double_left = create_chessboard(rows=2, cols=3, square_size=100, top_left_black=True) # PDI 2 Double Left
    chessboard_PDI_2_Double_right = create_chessboard(rows=2, cols=3, square_size=100, top_left_black=False) # PDI 2 Double Right
    chessboard_AS = create_chessboard(AS_pattern=AS_pattern, square_size=62) # AS Original
    chessboard_AS_xp3 = create_chessboard(AS_pattern=AS_pattern, square_size=62) # AS x + 3
    chessboard_AS_xm3 = create_chessboard(AS_pattern=AS_pattern, square_size=62) # AS x - 3
    chessboard_AS_yp3 = create_chessboard(AS_pattern=AS_pattern, square_size=62) # AS y + 3
    chessboard_AS_ym3 = create_chessboard(AS_pattern=AS_pattern, square_size=62) # AS y - 3

    screen = pygame.display.set_mode((screen_width, screen_height))

    # initial value
    mode = 0
    scale = 1.0
    x_offset = (screen_width - chessboard_hwasung_A.shape[1]) // 2
    y_offset = (screen_height - chessboard_hwasung_A.shape[0]) // 2 - 427
    drawing = False
    start_pos = None
    alpha = 128  # Alpha value of Line within range of ( 0 ~ 255 )
    lines = []   # List of Line

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
        
        # Factory & Line Info
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
            board_gap = -18

        if keys[pygame.K_4]: # PDI 3 Single
            mode = 4
            scale = 1.0
            x_offset = (screen_width - chessboard_PDI_3_Single.shape[1]) // 2
            y_offset = (screen_height - chessboard_PDI_3_Single.shape[0]) // 2 - 198

        if keys[pygame.K_5]: # AS Original
            mode = 5
            scale = 1.0
            x_offset = (screen_width - chessboard_AS.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS.shape[0]) // 2 - 177

        if keys[pygame.K_6]: # AS x + 3
            mode = 6
            scale = 1.0
            x_offset = (screen_width - chessboard_AS.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS.shape[0]) // 2 - 177

        if keys[pygame.K_7]: # AS x - 3
            mode = 7
            scale = 1.0
            x_offset = (screen_width - chessboard_AS.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS.shape[0]) // 2 - 177

        if keys[pygame.K_8]: # AS y + 3
            mode = 8
            scale = 1.0
            x_offset = (screen_width - chessboard_AS.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS.shape[0]) // 2 - 177

        if keys[pygame.K_9]: # AS y - 3
            mode = 9
            scale = 1.0
            x_offset = (screen_width - chessboard_AS.shape[1]) // 2
            y_offset = (screen_height - chessboard_AS.shape[0]) // 2 - 177

        if False:
            # Press d to start
            if keys[pygame.K_d]:
                mouse_pos = pygame.mouse.get_pos()

                if not drawing:
                    # initializing start_pos when mouse detect click event
                    start_pos = mouse_pos
                    drawing = True
                else:
                    end_pos = mouse_pos
                    lines.append((start_pos, end_pos))  # Saving Lines
                    start_pos = pygame.mouse.get_pos()

                    drawing = False

            # Press f to clear
            if keys[pygame.K_f]:
                lines.clear()
                drawing = False  # Turn off Drawing Mode

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

            moved_image_AS_ym3 = move_and_resize_image(chessboard_AS_ym3, x_offset, y_offset, scale, screen_width, screen_height)
            moved_image_rgb_AS_ym3 = cv2.cvtColor(moved_image_AS_ym3, cv2.COLOR_GRAY2RGB)
            moved_image_surface_AS_ym3 = pygame.surfarray.make_surface(np.rot90(moved_image_rgb_AS_ym3))
            screen.blit(moved_image_surface_AS_ym3, (0, 0))

            mode_text = mode_names.get(mode, "Unknown Mode")  # Current Mode Name
            text_surface = font.render(f"{mode_text}", True, (0,0,0))  # Text Color = Black
            screen.blit(text_surface, (10, 10))  # Text Display on Top Left Corner
            
        if False:
            for line in lines:
                draw_transparent_line(screen, line[0], line[1], (255, 255, 255), alpha)

        # 화면 업데이트
        pygame.display.update()

if __name__ == "__main__":
    main()  