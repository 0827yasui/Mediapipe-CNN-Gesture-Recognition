import cv2 as cv

HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (0, 9), (9,10), (10,11), (11,12),
        (0,13), (13,14), (14,15), (15,16),
        (0,17), (17,18), (18,19), (19,20),
        (5, 9), (9,13), (13,17)
    ]

def landmark_to_point(frame, landmark):
    x = int(landmark.x * frame.shape[1])
    y = int(landmark.y * frame.shape[0])
    return (x, y)

class Draw():
    def __init__(self):
        # /////////////////////////
        #   デバッグメッセージ
        # /////////////////////////
        pass

    def face_landmarkers_dot(self, frame, face_result):
        if face_result.face_landmarks:
            for face_landmarks in face_result.face_landmarks:
                for landmark in face_landmarks:
                    x, y = landmark_to_point(frame, landmark)
    
                    cv.circle(
                        frame,
                        (x, y),
                        1,
                        (0, 255, 255),
                        -1
                    )

    def hand_landmarkers_dot(self, frame, hand_result):
        if hand_result.hand_landmarks:
            for hand_landmarks in hand_result.hand_landmarks:
                for landmark in hand_landmarks:
                    x, y = landmark_to_point(frame, landmark)
    
                    cv.circle(
                        frame,
                        (x, y),
                        5,
                        (255, 0, 0),
                        -1
                    )


    def face_landmarkers_line(self, frame, face_result):
        for face_landmarks in face_result.face_landmarks:    
            points = []

            for landmark in face_landmarks:
                x, y = landmark_to_point(frame, landmark)
                points.append((x, y))

            for i in range(len(points) - 1):
                cv.line(
                    frame,
                    points[i],
                    points[i + 1],
                    (255, 255, 0),
                    1
                )

    def hand_landmarkers_line(self, frame, hand_result):
        for hand_landmarks in hand_result.hand_landmarks:    
            points = []

            for landmark in hand_landmarks:
                x, y = landmark_to_point(frame, landmark)
                points.append((x, y))
    
            for start, end in HAND_CONNECTIONS:
                cv.line(
                    frame,
                    points[start],
                    points[end],
                    (0, 255, 0),
                    2
                )

    def put_text(self, frame, text, position, font_scale, color, thickness):
        return cv.putText(
            frame,
            text,
            position,
            cv.FONT_HERSHEY_SIMPLEX,
            font_scale,
            color,
            thickness
        )