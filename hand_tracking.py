import cv2
import mediapipe as mp
import math
from pathlib import Path
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import vgamepad as vg

def is_hand_open(hand):
    index_open = hand[8].y < hand[6].y
    middle_open = hand[12].y < hand[10].y
    ring_open = hand[16].y < hand[14].y
    pinky_open = hand[20].y < hand[18].y

    return (
        index_open
        and middle_open
        and ring_open
        and pinky_open
    )

# Location of the hand tracking model
MODEL_PATH = Path(
    r"C:\Users\chara\OneDrive\Documents\VSW\models\hand_landmarker.task"
)

print("Model path:", MODEL_PATH)
print("Model exists:", MODEL_PATH.exists())

# Configure MediaPipe
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2,
)

# Start hand tracker
with vision.HandLandmarker.create_from_options(options) as landmarker:
    gamepad = vg.VX360Gamepad()
    smoothed_steering = 0.0
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()

        if not success:
            print("Could not access the camera.")
            break

        # Convert OpenCV's BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hands
        result = landmarker.detect(mp_image)

       # Variables for wrist positions
        left_wrist_x = None
        left_wrist_y = None

        right_wrist_x = None
        right_wrist_y = None

        throttle = 0.0
        brake = 0.0
        paused = False
        left_hand_open = False
        right_hand_open = False
        # Read each detected hand
        for hand_index, hand in enumerate(result.hand_landmarks):
            handedness = result.handedness[hand_index][0].category_name

            hand_open = is_hand_open(hand)

            print(handedness, "hand open:", hand_open)

            if handedness == "Left":
                left_hand_open = hand_open

            elif handedness == "Right":
                right_hand_open = hand_open
            # Check for a thumb-up gesture
            thumb_tip = hand[4]
            thumb_ip = hand[3]

            thumb_up = thumb_tip.y < thumb_ip.y
            if handedness == "Right":
                if thumb_up:
                    throttle = 1.0
                else:
                    throttle = 0.0
                print("Throttle:", throttle)
            elif handedness == "Left":

                if thumb_up:
                    brake = 0.0
                else:
                    brake = 1.0

                print("Brake:", brake)

            # Landmark 0 = wrist
            wrist = hand[0]

            if handedness == "Left":
                left_wrist_x = wrist.x
                left_wrist_y = wrist.y

            elif handedness == "Right":
                right_wrist_x = wrist.x
                right_wrist_y = wrist.y

            # Draw landmarks
            for landmark in hand:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                     -1
                )

        if left_hand_open and right_hand_open:
            paused = True
        else:
            paused = False
        print("Paused:", paused)
        # Print the stored values
        if left_wrist_x is not None and right_wrist_x is not None:

            print(
                "Left:", round(left_wrist_x, 2),
                "| Right:", round(right_wrist_x, 2)
            )

            # Calculate the center between both wrists
            center_x = (left_wrist_x + right_wrist_x) / 2

            print("Center X:", round(center_x, 2))
            # Difference between the two wrists
            dx = right_wrist_x - left_wrist_x
            dy = right_wrist_y - left_wrist_y

            print(
                "dx:", round(dx, 2),
                "| dy:", round(dy, 2)
            )
            # Calculate angle between the two wrists
            angle = math.degrees(math.atan2(dy, dx))
            # Convert negative angles into the 0-360 range
            if angle < 0:
                angle += 360

            print("Normalized angle:", round(angle, 2), "degrees")
            # Neutral hand position
            neutral_angle = 180.0
            # Difference from neutral
            steering_angle = angle - neutral_angle
            print("Steering angle:", round(steering_angle, 2))
            # Maximum steering angle
            max_angle = 30.0
            # Convert angle to -1.0 to +1.0
            steering = steering_angle / max_angle
            # Limit steering to -1.0 to +1.0
            steering = max(-1.0, min(1.0, steering))
            # Ignore tiny movements around the center
            dead_zone = 0.10

            if abs(steering) < dead_zone:
                steering = 0
            # Smooth the steering movement
            smooth_factor = 0.1
            smoothed_steering = (
                smoothed_steering
                + (steering - smoothed_steering) * smooth_factor
            )
            print("Steering:", round(steering, 2))
            print("Smoothed steering:", round(smoothed_steering, 2))
        if paused:
            smoothed_steering = 0.0
            throttle = 0.0
            brake = 0.0
        gamepad.left_joystick_float(
            x_value_float=smoothed_steering,
            y_value_float=0.0
        )

        gamepad.right_trigger_float(
            value_float=throttle
        )

        gamepad.left_trigger_float(
            value_float=brake
        )

        gamepad.update()
        cv2.putText(
            frame,
            f"Steering: {smoothed_steering:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        # Steering visual bar
        bar_x = 20
        bar_y = 45
        bar_width = 300
        bar_height = 15

        # Convert steering from -1..1 to a position from 0..300
        steering_position = int((smoothed_steering + 1) / 2 * bar_width)

        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (100, 100, 100),
            2
        )

        cv2.circle(
            frame,
            (bar_x + steering_position, bar_y + bar_height // 2),
            8,
            (0, 255, 0),
            -1
        )


        cv2.putText(
            frame,
            f"Throttle: {'ON' if throttle == 1.0 else 'OFF'}",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        # Throttle bar
        throttle_width = 200
        throttle_height = 20
        throttle_x = 20
        throttle_y = 140
        throttle_fill = int(throttle * throttle_width)

        cv2.rectangle(
            frame,
            (throttle_x, throttle_y),
            (throttle_x + throttle_width, throttle_y + throttle_height),
            (100, 100, 100),
            2
        )   

        cv2.rectangle(
            frame,
            (throttle_x, throttle_y),
            (throttle_x + throttle_fill, throttle_y + throttle_height),
            (0, 255, 0),
            -1
        )
        # Brake bar
        brake_width = 200
        brake_height = 20
        brake_x = 20
        brake_y = 170

        brake_fill = int(brake * brake_width)
        cv2.rectangle(
            frame,
            (brake_x, brake_y),
            (brake_x + brake_width, brake_y + brake_height),
            (100, 100, 100),
            2
        )
        cv2.rectangle(
            frame,
            (brake_x, brake_y),
            (brake_x + brake_fill, brake_y + brake_height),
            (0, 0, 255),
            -1
        )

        cv2.putText(
            frame,
            f"Brake: {'ON' if brake == 1.0 else 'OFF'}",
            (20, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        # System status
        if paused:
            status_text = "STATUS: PAUSED"
            status_color = (0, 0, 255)
        else:
            status_text = "STATUS: ACTIVE"
            status_color = (0, 255, 0)

        cv2.putText(
            frame,
            status_text,
            (20, 205),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            status_color,
            2
        )
        cv2.imshow("Hand Tracking", frame)

        # Press Q to quit
        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            neutral_angle = angle
            print("Calibration complete! Neutral angle:", round(neutral_angle, 2))

        if key == ord("q"):
            break
    

    gamepad.reset()
    gamepad.update()

    camera.release()
    cv2.destroyAllWindows()