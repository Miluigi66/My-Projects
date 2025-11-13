import cv2
import numpy as np

def camera_viewer():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of teal/turquoise (an uncommon color in many scenes) in HSV
        # Hue ~ 80-100 (OpenCV 0-179), S and V thresholds avoid very pale/dark pixels
        lower_teal = np.array([80, 60, 60])
        upper_teal = np.array([100, 255, 255])

        # Threshold the HSV image to get only teal/turquoise colors
        mask = cv2.inRange(hsv, lower_teal, upper_teal)

        # Clean up the mask (reduce noise)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)

        # Find contours on the binary mask
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv2.contourArea(c) < 100:  # ignore small noise
                continue
            x, y, w, h = cv2.boundingRect(c)
            # draw rectangle on the original frame (green, thickness 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Bitwise-AND mask and original image for visualization
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)

        def mouse_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.putText(frame, f'({x}, {y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.imshow('frame', frame)
        
        cv2.setMouseCallback('frame', mouse_event)

        # Escape key to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break
        if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_viewer()
