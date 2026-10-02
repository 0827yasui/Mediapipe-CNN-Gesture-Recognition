import cv2 as cv
import torch

from src.setting.use.camera_use import camera_use
from src.setting.use.frame_use import Frame_use
from src.setting.use.mediapipe_use import Mediapipe_use
from src.setting.use.CNN_use import CNN_use
from src.library.frame.draw import Draw


def main():
    camera = camera_use()
    frame_use = Frame_use(mode=1)
    mediapipe_use = Mediapipe_use()
    cnn_use = CNN_use(mode=1)
    draw = Draw()

    cnn_use.load()

    camera.camera_open()
    timestamp_ms = 0

    labels = {
        0: "Guu",
        1: "Choki",
        2: "Paa"
    }

    try:
        while True:
            frame = camera.camera_frame_get()

            if frame is None:
                break

            # ---------------------------------------------
            # カメラ画像の前処理
            # ---------------------------------------------
            frame = frame_use.flip_(frame)

            image = frame_use.resize_(frame)
            image = frame_use.image_(image)

            # ---------------------------------------------
            # MediaPipe
            # ---------------------------------------------
            hand_result = mediapipe_use.hand_detect(
                image,
                timestamp_ms
            )

            # ---------------------------------------------
            # 黒画像にランドマークを描画
            # ---------------------------------------------
            result = frame_use.print_frame_dark_(frame)

            draw.hand_landmarkers_dot(result, hand_result)
            draw.hand_landmarkers_line(result, hand_result)

            # ---------------------------------------------
            # CNN用Tensorへ変換
            # ---------------------------------------------
            tensor = frame_use.tensor_(result).unsqueeze(0)

            # ---------------------------------------------
            # CNN
            # ---------------------------------------------
            with torch.no_grad():
                logits = cnn_use.forward(tensor)

                prediction = logits.argmax(
                    dim=1
                ).item()

                confidence = logits[0, prediction].item()

            # ---------------------------------------------
            # 結果
            # ---------------------------------------------
            text = (
                f"{labels[prediction]} "
                f"{confidence * 100:.1f}%"
            )

            print(text)

            draw.put_text(
                result,
                text,
                (10, 30),
                1.0,
                (0, 255, 0),
                2
            )

            cv.imshow(
                "Interface",
                result
            )

            # ESC
            if cv.waitKey(1) == 27:
                break

            timestamp_ms += 33

    finally:
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()