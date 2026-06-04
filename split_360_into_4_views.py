import cv2
import py360convert
import os

video_path = "insta360_video.mp4"
output_folder = "dataset_4views_debug"

os.makedirs(output_folder, exist_ok=True)

video = cv2.VideoCapture(video_path)

if not video.isOpened():
    print("ERROR: Could not open video.")
    print("Make sure insta360_video.mp4 is in the same folder as this script.")
    exit()

fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"FPS: {fps}")
print(f"Total frames: {total_frames}")

frame_interval = 30
frame_num = 0
saved_num = 0

views = {
    "front": 0,
    "right": 90,
    "back": 180,
    "left": 270
}

while True:
    ret, frame = video.read()

    if not ret:
        break

    if frame_num == 0:
        print(f"First frame shape: {frame.shape}")
        cv2.imwrite("debug_frame.jpg", frame)
        print("Saved debug_frame.jpg. Open it and check what it looks like.")

    if frame_num % frame_interval == 0:

        for view_name, angle in views.items():

            view_img = py360convert.e2p(
                frame,
                fov_deg=90,
                u_deg=angle,
                v_deg=0,
                out_hw=(1024, 1024)
            )

            filename = os.path.join(
                output_folder,
                f"{view_name}_{saved_num:05d}.jpg"
            )

            cv2.imwrite(filename, view_img)

        print(f"Saved 4-view set {saved_num}")

        saved_num += 1

        if saved_num >= 5:
            print("Stopping after 5 sets for testing.")
            break

    frame_num += 1

video.release()

print("Finished test.")
