from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

def CheckCurrentColor():
    # Find the element by XPath
    xpath = "//*[@id='canvselect']/img"
    element = driver.find_element(By.XPATH, xpath)

     # Take a screenshot of the element
    screenshot_path = "screenshot.png"
    element.screenshot(screenshot_path)

    # Open the screenshot image
    image = Image.open(screenshot_path)

    # Get the color at the top left corner, but 5 pixels lower and 5 pixels to the right
    color = image.getpixel((5, 5))

    return color

def get_character(pixel, color_mapping=None):

    
    if color_mapping is None:
        color_mapping = {     
            (109, 0 ,26): "1",
            (190, 0, 57): "2",
            (255, 69, 0): "3",
            (255, 168, 0): "4",
            (255, 214, 53): "5",
            (255, 248, 184): "6",
            (0, 163, 104): "7",
            (0, 204, 120): "8",
            (126, 237, 86): "9",
            (0, 117, 111): "a",
            (0, 158, 170): "b",
            (0, 204, 192): "c",
            (36, 80, 164): "d",
            (54, 144, 234): "e",
            (81, 233, 244): "f",
            (73, 58, 193): "g",
            (106, 92, 255): "h",
            (148, 179, 255): "i",
            (129, 30, 159): "j",
            (180, 74, 192): "k",
            (228, 171, 255): "l",
            (222, 16, 127): "m",
            (255, 56, 129): "n",
            (255, 153, 170): "o",
            (109, 72, 47): "p",
            (156, 105, 38): "q",
            (255, 180, 112): "r",
            (0, 0, 0): "s",
            (81, 82, 82): "t",  # Dark grey
            (137, 141, 144): "u",  # Grey
            (212, 215, 217): "v",  # Light grey
            (255, 255, 255): "w",  # White
    }

    min_distance = float('inf')
    closest_char = "."

    for color, char in color_mapping.items():
        # Calculate the Euclidean distance between pixel and color
        distance = sum((a - b) ** 2 for a, b in zip(pixel, color)) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_char = char

    return closest_char



# Ask for the name of the PNG file
file_name = input("Enter the name of the PNG file (with .png extension): ")

# Open the image file
image = Image.open(file_name)

# Convert image to RGB mode
image = image.convert("RGB")

print(image.size[0])
print(image.size[1])

# Ask the user for x and y coordinates
x = int(input("Enter the x coordinate: "))
y = int(input("Enter the y coordinate: "))

driver = webdriver.Chrome()

driver.get("https://rplace.live/")

time.sleep(5)

# Calculate the number of times to press up and left keys
x_steps = 999 - x
y_steps = 999 - y

actions = ActionChains(driver)

# Move left
for _ in range(x_steps):
    actions.send_keys(Keys.ARROW_LEFT)

# Move up
for _ in range(y_steps):
    actions.send_keys(Keys.ARROW_UP)

actions.perform()

time.sleep(5)
while True:
    # Loop through each pixel of the image
    for y_coord in range(image.size[1]):
        for x_coord in range(image.size[0]):
            # Get the color of the pixel
            pixel_color = image.getpixel((x_coord, y_coord))
            
            print(pixel_color)
            # Get the character corresponding to the closest color
            character = get_character(pixel_color)
            print(f'pixel to place: ${character}')
            CurrentPixelCharacter = get_character(CheckCurrentColor())
            print(f'pixel present: ${CurrentPixelCharacter}')
            if CurrentPixelCharacter != character:

                # Press the corresponding key
                actions.send_keys(character)
                actions.send_keys(Keys.ENTER)
                actions.send_keys(Keys.ARROW_RIGHT)
                actions.perform()
                time.sleep(2)  # Add delay of 2 seconds between each pixel placement
            else:
                actions.send_keys(Keys.ARROW_RIGHT)
                actions.perform()
                time.sleep(0.1)
            
        
        # Move to the next row
        if y_coord < image.size[1] - 1:  # Don't move down after the last row
            actions.send_keys(Keys.ARROW_DOWN)
            print("down")
            actions.perform()
            # After completing the rows, move back to the starting position
            for _ in range(image.size[0]):
                actions.send_keys(Keys.ARROW_LEFT)
            print("left")
            
            actions.perform()
            time.sleep(0.1)


    print("finished restarting")
    actions.send_keys(Keys.ARROW_DOWN)
    for _ in range(image.size[0]):
        actions.send_keys(Keys.ARROW_LEFT)
    for y_coord in range(image.size[1]):
        actions.send_keys(Keys.ARROW_UP)
    actions.perform()

time.sleep(5)
driver.quit()
