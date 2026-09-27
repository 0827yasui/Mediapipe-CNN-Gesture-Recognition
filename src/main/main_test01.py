import cv2 as cv

from src.setting.use.camera_use import camera_use
from src.setting.use.frame_use import Frame_use
from src.setting.use.mediapipe_use import Mediapipe_use
from src.library.frame.draw import Draw


def main():
    camera = camera_use()
    frame_use = Frame_use()
    mediapipe = Mediapipe_use()
    draw = Draw()

    camera.camera_open()

    timestamp_ms = 0

    try:
        while True:
            image = camera.camera_frame_get()

            if image is None:
                break

            image = frame_use.resize_(image)
            image = frame_use.flip_(image)

            frame = frame_use.print_frame_dark_(image)
            mp_image = frame_use.image_(image)            
            
            hand_result = mediapipe.hand_detect(mp_image, timestamp_ms)
            face_result = mediapipe.face_detect(mp_image, timestamp_ms)

            draw.hand_landmarkers_dot(frame, hand_result)
            draw.hand_landmarkers_line(frame, hand_result)
            draw.face_landmarkers_dot(frame, face_result)

            cv.imshow("Mediapipe Test", frame)
            timestamp_ms += 33
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()