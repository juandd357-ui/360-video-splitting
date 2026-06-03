import cv2
import py360convert
import os

video_path = "insta360.mp4"

os.makedirs("front", exist_ok=True)
os.makedirs("right", exist_ok=True)
os.makedirs("back", exist_ok=True)
os.makedirs("left", exist_ok=True)

video = cv2.VideoCapture(video_path)

frame_num = 0

while True:

    ret, frame = video.read()

    if not ret:
        break

    if frame_num % 30 == 0:

        front = py360convert.e2p(
            frame,
            fov_deg=90,
            u_deg=0,
            v_deg=0,
            out_hw=(512,512)
        )

        right = py360convert.e2p(
            frame,
            fov_deg=90,
            u_deg=90,
            v_deg=0,
            out_hw=(512,512)
        )

        back = py360convert.e2p(
            frame,
            fov_deg=90,
            u_deg=180,
            v_deg=0,
            out_hw=(512,512)
        )

        left = py360convert.e2p(
            frame,
            fov_deg=90,
            u_deg=270,
            v_deg=0,
            out_hw=(512,512)
        )

        cv2.imwrite(f"front/front_{frame_num:05d}.jpg", front)
        cv2.imwrite(f"right/right_{frame_num:05d}.jpg", right)
        cv2.imwrite(f"back/back_{frame_num:05d}.jpg", back)
        cv2.imwrite(f"left/left_{frame_num:05d}.jpg", left)

    frame_num += 1

video.release()

print("Done!")
