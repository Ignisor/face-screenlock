import os
import traceback
from multiprocessing import Process, Pipe
from subprocess import call
from threading import Timer

import cv2
import face_recognition
import numpy as np

LOCK_TIMEOUT = 3  # how long to wait before locking the screen
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSAVER_COMMAND = 'cinnamon-screensaver-command'
LOCK_ARGS = {
    True: '--activate',
    False: '--deactivate',
}


def lock_screen(lock):
    call((SCREENSAVER_COMMAND, LOCK_ARGS[lock]))


def find_user_in_frame(conn, frame, user_encoding):
    face_locations = face_recognition.face_locations(frame, model='cnn')
    face_encodings = face_recognition.face_encodings(frame, face_locations, num_jitters=2)

    found_user = False
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces((user_encoding, ), face_encoding, tolerance=0.9)

        found_user = any(matches)
        if found_user:
            break

    conn.send(found_user)


def load_user_encoding():
    try:
        user_image_face_encoding = np.load(os.path.join(BASE_DIR, 'user.npz'))
    except FileNotFoundError:
        user_image = face_recognition.load_image_file(os.path.join(BASE_DIR, 'user.jpg'))
        user_image_face_encoding = face_recognition.face_encodings(user_image, num_jitters=10)[0]
        np.save(os.path.join(BASE_DIR, 'user.npz'), user_image_face_encoding)

    return user_image_face_encoding


def main():
    user_encoding = load_user_encoding()
    video_capture = cv2.VideoCapture(0)  # get a reference to webcam #0 (the default one)

    user_not_found_timer = None

    parent_conn, child_conn = Pipe()
    find_user_process = None
    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if find_user_process is None:
            find_user_process = Process(target=find_user_in_frame, args=(child_conn, rgb_small_frame, user_encoding))
            find_user_process.start()
        elif find_user_process is not None and not find_user_process.is_alive():
            user_found = parent_conn.recv()
            find_user_process = None

            if user_found:
                print('user found')
                lock_screen(False)
                if user_not_found_timer is not None:
                    user_not_found_timer.cancel()
                    user_not_found_timer = None
            else:
                print('user not found')
                if user_not_found_timer is None:
                    user_not_found_timer = Timer(LOCK_TIMEOUT, lock_screen, (True,))
                    user_not_found_timer.start()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            with open(os.path.join(BASE_DIR, 'error.log'), 'a') as error_file:
                traceback.print_exc(file=error_file)
                error_file.write('\n')
