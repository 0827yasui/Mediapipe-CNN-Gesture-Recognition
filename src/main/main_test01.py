import cv2 as cv

from src.setting.use.camera_use import camera_use
from src.setting.use.frame_use import Frame_use
from src.setting.use.mediapipe_use import Mediapipe_use
from src.setting.use.CNN_use import CNN_use
from src.library.frame.draw import Draw


def main():
    camera = camera_use()
    frame_use = Frame_use()
    mediapipe = Mediapipe_use()
    cnn = CNN_use()
    draw = Draw()

    camera.camera_open()

    timestamp_ms = 0

    # CNNへ入力する画像サイズ
    cnn_width = 32
    cnn_height = 32

    while True:
        image = camera.camera_frame_get()

        image = frame_use.resize_(image)
        image = frame_use.flip_(image)

        mp_image = frame_use.image_(image)

        hand_result = mediapipe.hand_detect(
            mp_image,
            timestamp_ms
        )

        frame = frame_use.print_frame_dark_(image)

        draw.hand_landmarkers_dot(
            frame,
            hand_result
        )
        draw.hand_landmarkers_line(
            frame,
            hand_result
        )

        # CNN用Tensorへ変換
        tensor = frame_use.tensor_(
            frame,cnn_width,cnn_height
        )

        # 推論
        output = cnn.forword(tensor)
        prediction = output.argmax(dim=1).item()

        draw.put_text(
            frame,
            f"Output: {prediction}",
            (20, 40),
            1.0,
            (255, 255, 255),
            2
        )

        key = cv.waitKey(1) & 0xFF

        # -----------------------------
        # キー入力による学習
        # -----------------------------

        if key == ord("g"):
            cnn.train(tensor, 0)
        elif key == ord("c"):
            cnn.train(tensor, 1)
        elif key == ord("p"):
            cnn.train(tensor, 2)
        elif key == ord("q"):
            break

        cv.imshow("CNN Test", frame)

        timestamp_ms += 33

    camera.cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()