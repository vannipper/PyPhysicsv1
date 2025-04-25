import pygame
import os
import math

pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Input Planet Data!")

# Define positions for the labels
label_positions = [
    (40, 35),  # Label for the page count box
    (40, 110),  # Label for Name
    (40, 160),  # Label for Mass
    (40, 210),  # Label for *10^
    (40, 260),  # Label for Diameter
    (40, 310),  # Label for Initial x position
    (40, 360),  # Label for Initial y position
    (40, 410),  # Label for Initial x velocity
    (40, 460),  # Label for Initial y velocity
    (40, 510)   # rgb label
]

labels = [
    "Number of bodies:",  # For the top text box
    "Name:",  # Box 1
    "Mass:",  # Box 2
    "*10^",  # Box 3
    "Diameter:",  # Box 4
    "Initial x position:",  # Box 5
    "Initial y position:",  # Box 6
    "Initial x velocity:",  # Box 7
    "Initial y velocity:",  # Box 8
    "Color:"
]

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Set up fonts
font = pygame.font.Font(None, 32)

# Set up the integer input box at the top (only displayed on page one)
top_input_box = pygame.Rect(300, 20, 400, 50)
top_box_active = False
top_box_color = GRAY
page_count_text = ""

# Set up the eight main text boxes for each page
input_boxes = [pygame.Rect(300, 100 + i * 50, 400, 40) for i in range(9)]
active_boxes = [False] * 9  # Track active state for each box
page_texts = [[""] * 9 for _ in range(10)]  # Stores text for each box on each page (up to 10 pages) #BUG potential
box_colors = [GRAY] * 9  # Initial colors for each box

# Pagination settings
current_page = 0  # Start on the first page
total_pages = 1  # Number of pages (from the integer input)

# Set up navigation and save buttons
prev_button = pygame.Rect(350, 580, 100, 40)
next_button = pygame.Rect(550, 580, 100, 40)
save_button = pygame.Rect(450, 640, 100, 40)
prev_text = font.render("Previous", True, WHITE)
next_text = font.render("Next", True, WHITE)
save_text = font.render("Save", True, WHITE)

def draw_planet_representation():
    planet_name = page_texts[current_page][0]
    diameter = int(page_texts[current_page][3]) if validate_input(3, page_texts[current_page][3]) else 100
    x_position = float(page_texts[current_page][4]) if validate_input(4, page_texts[current_page][4]) else 0
    y_position = float(page_texts[current_page][5]) if validate_input(5, page_texts[current_page][5]) else 0
    x_velocity = float(page_texts[current_page][6]) if validate_input(6, page_texts[current_page][6]) else 0
    y_velocity = float(page_texts[current_page][7]) if validate_input(7, page_texts[current_page][7]) else 0
    color_input = page_texts[current_page][8]
    
    try:
        rgb = list(map(int, color_input.split()))
        if len(rgb) == 3 and all(0 <= val <= 255 for val in rgb):
            circle_color = tuple(rgb)
        else:
            raise ValueError
    except ValueError:
        circle_color = GRAY

    circle_x, circle_y = 900, 350
    display_radius = 100
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), display_radius)

    velocity_angle = math.atan2(y_velocity, x_velocity) # velocity arrow
    arrow_start_x = circle_x + display_radius * math.cos(velocity_angle)
    arrow_start_y = circle_y + display_radius * math.sin(velocity_angle)
    arrow_end_x = circle_x + 150 * math.cos(velocity_angle)
    arrow_end_y = circle_y + 150 * math.sin(velocity_angle)
    pygame.draw.line(screen, BLACK, (arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y), 2)
    pygame.draw.polygon(screen, BLACK, [
        (arrow_end_x, arrow_end_y),
        (arrow_end_x - 10 * math.cos(velocity_angle - math.pi / 6), arrow_end_y - 10 * math.sin(velocity_angle - math.pi / 6)),
        (arrow_end_x - 10 * math.cos(velocity_angle + math.pi / 6), arrow_end_y - 10 * math.sin(velocity_angle + math.pi / 6)),
    ])

    screen.blit(font.render(f'Initial Position: ({x_position}, {y_position})', True, BLACK), (750, 150)) # text
    screen.blit(font.render(f'Initial Velocity: ({x_velocity}, {y_velocity})', True, BLACK), (750, 180))
    name_text = font.render(planet_name, True, BLACK)
    screen.blit(name_text, (circle_x - name_text.get_width() // 2, circle_y - name_text.get_height() // 2))
    line_length = display_radius * 2
    line_start_x, line_start_y = circle_x - display_radius, circle_y + display_radius + 30
    line_end_x, line_end_y = line_start_x + line_length, line_start_y
    pygame.draw.line(screen, BLACK, (line_start_x, line_start_y), (line_end_x, line_end_y), 2)
    diameter_text = font.render(f"Diameter: {diameter}", True, BLACK)
    screen.blit(diameter_text, (line_start_x, line_start_y + 10))

def validate_input(box_index, text):
    try:
        if box_index == 0:
            return text.isalnum()  # Box 1: Any alphanumeric string
        elif box_index == 1:
            value = float(text)
            return 1.0 <= value <= 9.999  # Box 2: Float between 1.0 and 9.999
        elif box_index == 2:
            value = int(text)
            return -100 <= value <= 100  # Box 3: Integer between -100 and 100
        elif box_index == 3:
            value = int(text)
            return value > 0  # Box 4: Integer greater than 0
        elif box_index in {4, 5}:
            int(text)  # Boxes 5 and 6: Any integer
            return True
        elif box_index == 6:
            float(text)  # Box 7: Any float
            return True
        elif box_index == 7:
            float(text)  # Box 8: Any float
            return True
        if box_index == 8:  # RGB color validation
            rgb = list(map(int, text.split()))
            if len(rgb) == 3 and all(0 <= val <= 255 for val in rgb):
                return True
    except ValueError:
        return False
    return False

def validate_page_count(text):
    try:
        return int(text) > 0
    except ValueError:
        return False

def save_to_file():
    with open("planetdata.dat", "w") as file:
        for page in page_texts:
            if all(validate_input(i, page[i]) for i in range(len(page))): 
                line = ",".join(page)
                file.write(line + "\n")

def load_defaults():
    global page_count_text, total_pages
    try:
        with open("default.dat", "r") as file:
            lines = file.readlines()
            total_pages = len(lines)  # Set total pages based on number of lines in default.dat
            page_count_text = str(total_pages)  # Set initial value of top text box
            
            for i, line in enumerate(lines):
                if i >= len(page_texts):
                    break  # Stop if there are more lines than page_texts can hold
                page_texts[i] = line.strip().split(",")
                page_texts[i] += [""] * (8 - len(page_texts[i])) # Ensure exactly 8 boxes per page, fill missing entries with empty strings
    except FileNotFoundError:
        pass

def all_inputs_valid():
    for i, text in enumerate(page_texts[current_page]):
        if not validate_input(i, text):
            return False
    return True

def draw_labels():
    for i, label in enumerate(labels): # Draw each label next to the corresponding text box
        if current_page == 0 or i > 0: # Only show "Number of bodies" label on page 1
            label_text = font.render(label, True, (0, 0, 0))  # Black text
            screen.blit(label_text, label_positions[i])

    page_indicator = font.render(f"Page {current_page + 1} of {total_pages}", True, BLACK) # Draw page indicator
    screen.blit(page_indicator, (500, 20))

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

load_defaults()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clear_terminal()
            pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_page == 0 and top_input_box.collidepoint(event.pos): # Check if the top input box was clicked (only on page one)
                top_box_active = not top_box_active
            else:
                top_box_active = False
            top_box_color = LIGHT_BLUE if top_box_active else GRAY
            
            for i, box in enumerate(input_boxes): # Check if any of the main boxes were clicked
                if box.collidepoint(event.pos):
                    if box_colors[i] != RED:  # Only activate the box if it isn’t currently invalid (red)
                        active_boxes[i] = not active_boxes[i]
                else:
                    active_boxes[i] = False
                box_colors[i] = LIGHT_BLUE if active_boxes[i] else GRAY

            if prev_button.collidepoint(event.pos) and current_page > 0: # Check if "Next", "Previous", or "Save" buttons were clicked
                current_page -= 1
            elif next_button.collidepoint(event.pos) and current_page < total_pages - 1:
                current_page += 1
            elif save_button.collidepoint(event.pos) and all_inputs_valid():
                save_to_file()
                clear_terminal()
                pygame.quit()
                os.system('python3 runengine.py')
                exit()

        if event.type == pygame.KEYDOWN:
            if top_box_active and current_page == 0: # Handle input for the top box
                if event.key == pygame.K_BACKSPACE:
                    page_count_text = page_count_text[:-1]
                elif event.unicode.isdigit():  # Allow only digits
                    page_count_text += event.unicode
                if validate_page_count(page_count_text):
                    total_pages = int(page_count_text)

            for i, box in enumerate(input_boxes): # Handle input for main boxes
                if active_boxes[i]:
                    if event.key == pygame.K_BACKSPACE:
                        page_texts[current_page][i] = page_texts[current_page][i][:-1]
                    elif event.unicode.isprintable():
                        page_texts[current_page][i] += event.unicode

                    if validate_input(i, page_texts[current_page][i]): # Validate input after every change and adjust color accordingly
                        box_colors[i] = GREEN
                    else:
                        box_colors[i] = RED

    screen.fill(WHITE) # Draw the screen elements
    draw_labels()
    draw_planet_representation()

    if current_page == 0: # Draw the top input box (number of bodies) for page 1 only
        pygame.draw.rect(screen, top_box_color, top_input_box)
        text = font.render(page_count_text, True, BLACK)
        screen.blit(text, (top_input_box.x + 10, top_input_box.y + 10))

    for i, box in enumerate(input_boxes): # Draw input boxes and their text
        pygame.draw.rect(screen, box_colors[i], box)
        text = font.render(page_texts[current_page][i], True, BLACK)
        screen.blit(text, (box.x + 10, box.y + 10))

    pygame.draw.rect(screen, BLUE, prev_button)  # Draw the buttons
    screen.blit(prev_text, (prev_button.x + 5, prev_button.y + 5))
    pygame.draw.rect(screen, BLUE, next_button)
    screen.blit(next_text, (next_button.x + 20, next_button.y + 5))
    pygame.draw.rect(screen, GREEN, save_button)
    screen.blit(save_text, (save_button.x + 25, save_button.y + 5))

    pygame.display.update()