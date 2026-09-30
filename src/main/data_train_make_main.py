import cv2 as cv

from src.setting.use.camera_use import camera_use
from src.setting.use.frame_use import Frame_use
from src.setting.use.mediapipe_use import Mediapipe_use
from src.library.frame.draw import Draw
from src.library.data.file_open.jpg_input import JPG_Input


def main():
    camera = camera_use()
    frame_use = Frame_use(mode=0)
    mediapipe_use = Mediapipe_use()
    draw = Draw()
    jpg = JPG_Input(mode=0)
    label = 0

    camera.camera_open()
    timestamp_ms = 0

    try:
        while True:
            frame = camera.camera_frame_get()
            if frame is None:
                break

            image = frame_use.resize_(frame)
            frame = frame_use.flip_(frame)
            image = frame_use.image_(image)
            hand_result = mediapipe_use.hand_detect(image, timestamp_ms)

            result = frame_use.print_frame_dark_(frame)
            draw.hand_landmarkers_dot(result, hand_result)
            draw.hand_landmarkers_line(result, hand_result)

            cv.imshow("Hand Image", result)
            key = cv.waitKey(1)

            if key == ord("g"):
                jpg.input(result, 0)
            elif key == ord("c"):
                jpg.input(result, 1)
            elif key == ord("p"):
                jpg.input(result, 2)
            elif key == 27:
                break

            timestamp_ms += 33
    finally:
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
