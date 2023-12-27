import cv2
import numpy as np

# List of video URLs
video_urls = ['C:\Python_Project\DigitalMultimedia\Inv\\rats\\video1.mp4',
              'C:\Python_Project\DigitalMultimedia\Inv\\rats\\video2.mp4',
              'C:\Python_Project\DigitalMultimedia\Inv\\rats\\video3.mp4',
              'C:\Python_Project\DigitalMultimedia\Inv\\rats\\video4.mp4',
              'C:\Python_Project\DigitalMultimedia\Inv\\rats\\video5_1.mp4']


for video_url in video_urls:
    # Read the video file
    cap = cv2.VideoCapture(video_url)

    # Read the first frame
    ret, frame = cap.read()

    # Select the initial region for tracking using cv2.selectROI
    track_window = cv2.selectROI('Select Object', frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow('Select Object')

    # Region of Interest (ROI) for tracking
    x, y, w, h = track_window
    roi = frame[y:y+h, x:x+w]

    # Convert the ROI to HSV color space
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Calculate the histogram of the ROI
    roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])

    # Normalize the histogram
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Set termination criteria for mean shift
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec based on your preference
    output_video_name = f"{video_url.split('.')[0]}_CAMShift.avi"
    out = cv2.VideoWriter(output_video_name, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Backproject the histogram on the current frame
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # Apply CAMShift to get the new region
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw the result on the image
        pts = cv2.boxPoints(ret).astype(int)
        frame = cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        # Write the frame into the output video
        out.write(frame)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
            break

    # Release the VideoWriter and VideoCapture objects
    out.release()
    cap.release()
    cv2.destroyAllWindows()

