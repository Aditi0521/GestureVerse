import mediapipe as mp
import cv2
import numpy as np
import time
import os
from django.shortcuts import render, redirect
from django.template.context_processors import request


def main():
    # Constants
    ml = 150
    max_x, max_y = 250 + ml, 50
    curr_tool = "select tool"
    time_init = True
    rad = 40
    var_inits = False
    thick = 4
    prevx, prevy = 0, 0
    selected_color = (255, 255, 255)  # Initialize selected color

    # Function to get tools
    def getTool(x):
        if x < 50 + ml:
            return "line"
        elif x < 100 + ml:
            return "rectangle"
        elif x < 150 + ml:
            return "draw"
        elif x < 200 + ml:
            return "circle"
        else:
            return "erase"

    # Function to check if index finger raised
    def index_raised(yi, y9):
        if (y9 - yi) > 40:
            return True
        return False

    # Function to handle color selection with smooth transitions
    def select_color_smooth(x):
        nonlocal selected_color  # Ensure we're modifying the selected_color from the outer scope
        if x < 50:
            target_color = (255, 0, 0)  # Blue
        elif x < 100:
            target_color = (0, 255, 0)  # Green
        elif x < 150:
            target_color = (0, 0, 255)  # Red
        elif x < 200:
            target_color = (0, 255, 255)  # Yellow
        else:
            target_color = (255, 255, 255)  # White

        # Smooth transition using interpolation
        selected_color = tuple(int(a * 0.8 + b * 0.2) for a, b in zip(selected_color, target_color))

    # Initialize hands module
    hands = mp.solutions.hands
    hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
    draw = mp.solutions.drawing_utils

    # Initialize mask for blackboard
    blackboard = np.zeros((600, 800, 3), dtype=np.uint8)  # Black canvas

    # Color palette
    palette = np.zeros((300, 50, 3), dtype=np.uint8)
    palette[0:50, :] = [255, 0, 0]  # Blue
    palette[50:100, :] = [0, 255, 0]  # Green
    palette[100:150, :] = [0, 0, 255]  # Red
    palette[150:200, :] = [0, 255, 255]  # Yellow
    palette[200:250, :] = [255, 255, 255]  # White

    # Define clear button parameters
    clear_button_size = (100, 40)
    clear_button_pos = (590, 0)

    # Define save button parameters
    save_button_size = (100, 40)
    save_button_pos = (700, 0)

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  # Set the width of the webcam feed
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)  # Set the height of the webcam feed

    # Load tools frame
    tools = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'pic1.jpg'))
    tools = cv2.resize(tools, (max_x - ml, max_y))  # Resize tools frame

    while True:
        _, frm = cap.read()
        frm = cv2.flip(frm, 1)
        frm = cv2.resize(frm, (800, 600))  # Resize the frame to match new dimensions
        rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
        op = hand_landmark.process(rgb)

        # Reset virtual pointer location on blackboard
        blackboard_copy = blackboard.copy()

        x, y = 0, 0

        if op.multi_hand_landmarks:
            for i in op.multi_hand_landmarks:
                draw.draw_landmarks(frm, i, hands.HAND_CONNECTIONS)
                x, y = int(i.landmark[8].x * 800), int(i.landmark[8].y * 600)

                if x < max_x and y < max_y and x > ml:
                    if time_init:
                        ctime = time.time()
                        time_init = False
                    ptime = time.time()

                    cv2.circle(frm, (x, y), rad, (0, 255, 255), 2)
                    rad -= 1

                    if (ptime - ctime) > 0.8:
                        curr_tool = getTool(x)
                        # print("Your current tool set to:", curr_tool)
                        time_init = True
                        rad = 40
                else:
                    time_init = True
                    rad = 40

                if 0 < x < 50:  # Check if hand is within the color palette region
                    select_color_smooth(y)
                    # print("Selected Color:", selected_color)

                if curr_tool == "draw":
                    xi, yi = int(i.landmark[12].x * 800), int(i.landmark[12].y * 600)
                    y9 = int(i.landmark[9].y * 600)

                    if index_raised(yi, y9):
                        cv2.line(blackboard, (prevx, prevy), (x, y), selected_color, thick)
                        prevx, prevy = x, y
                    else:
                        prevx = x
                        prevy = y

                if curr_tool == "line" or curr_tool == "rectangle" or curr_tool == "circle":
                    yi = int(i.landmark[12].y * 600)
                    y9 = int(i.landmark[9].y * 600)

                    if index_raised(yi, y9):
                        if not var_inits:
                            xii, yii = x, y
                            var_inits = True
                    else:
                        if var_inits:
                            if curr_tool == "line":
                                cv2.line(blackboard, (xii, yii), (x, y), selected_color, thick)
                            elif curr_tool == "rectangle":
                                cv2.rectangle(blackboard, (xii, yii), (x, y), selected_color, thick)
                            elif curr_tool == "circle":
                                radius = int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5)
                                cv2.circle(blackboard, (xii, yii), radius, selected_color, thick)
                            var_inits = False

                elif curr_tool == "erase":
                    xi, yi = int(i.landmark[12].x * 800), int(i.landmark[12].y * 600)
                    y9 = int(i.landmark[9].y * 600)

                    if index_raised(yi, y9):
                        cv2.circle(blackboard, (x, y), 30, (0, 0, 0), -1)

        # Draw virtual pointer on the blackboard
        cv2.circle(blackboard_copy, (x, y), 5, (0, 0, 255), -1)

        # Display tools on the blackboard
        blackboard_copy[:max_y, ml:max_x] = cv2.addWeighted(tools, 0.7, blackboard_copy[:max_y, ml:max_x], 0.3, 0)

        # Display color palette
        blackboard_copy[0:300, 0:50] = palette

        # Display clear button
        cv2.rectangle(blackboard_copy, clear_button_pos, (clear_button_pos[0] + clear_button_size[0],
                                                          clear_button_pos[1] + clear_button_size[1]), (255, 255, 255),
                      -1)
        cv2.putText(blackboard_copy, "Clear", (clear_button_pos[0] + 10, clear_button_pos[1] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 0), 2)

        # Display save button
        cv2.rectangle(blackboard_copy, save_button_pos, (save_button_pos[0] + save_button_size[0],
                                                         save_button_pos[1] + save_button_size[1]), (255, 255, 255), -1)
        cv2.putText(blackboard_copy, "Save", (save_button_pos[0] + 10, save_button_pos[1] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 0), 2)

        # Display the current tool name on the blackboard
        cv2.putText(blackboard_copy, "Current Tool: " + curr_tool.capitalize(), (10, 580), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255), 2)

        # Display blackboard
        cv2.imshow("Virtual Blackboard", blackboard_copy)

        # Check for clear button click
        if clear_button_pos[0] < x < clear_button_pos[0] + clear_button_size[0] \
                and clear_button_pos[1] < y < clear_button_pos[1] + clear_button_size[1]:
            blackboard = np.zeros((600, 800, 3), dtype=np.uint8)  # Reset blackboard

        # Check for save button click
        if save_button_pos[0] < x < save_button_pos[0] + save_button_size[0] \
                and save_button_pos[1] < y < save_button_pos[1] + save_button_size[1]:
            # Display a prompt for the user to enter the filename
            filename = ""
            while True:
                blackboard_copy = blackboard.copy()  # Create a copy of the blackboard
                cv2.rectangle(blackboard_copy, (200, 250), (600, 350), (255, 255, 255),
                              -1)  # Create a pop-up window
                cv2.putText(blackboard_copy, "Enter the image name to save:", (220, 300), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 0), 2)
                cv2.putText(blackboard_copy, filename, (220, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                            2)  # Display the entered filename
                cv2.imshow("Virtual Blackboard", blackboard_copy)
                key = cv2.waitKey(1)

                # Check for key press events
                if key == 13:  # If Enter key is pressed
                    if filename.strip() != "":  # Check if filename is not empty
                        break  # Exit the loop if filename is entered
                elif key == 27:  # If Escape key is pressed
                    break  # Exit the loop if Escape key is pressed
                elif key == 8:  # If Backspace key is pressed
                    filename = filename[:-1]  # Remove the last character from filename
                elif 32 <= key <= 126:  # If a printable ASCII character is pressed
                    filename += chr(key)  # Append the character to filename

            # Check if filename is not empty
            if filename.strip() != "":
                # Append ".png" extension if not already provided
                if not filename.strip().lower().endswith(".png"):
                    filename += ".png"

                cv2.imwrite(filename.strip(), blackboard)
                print("Drawing saved as:", filename.strip())
            else:
                print("No filename entered. Drawing not saved.")

        key = cv2.waitKey(1)
        if key == 27:  # If ESC key is pressed
            print("Execution successful")
            break

            # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
