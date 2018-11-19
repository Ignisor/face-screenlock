# Face Screenlock
Face recognition screen locker for Cinnamon. That simple script will use your web-cam to recognise your face and unlock screen when you are in front of the webcam. Or lock your screen when you are away for 3 seconds.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Using

- Python 3.7 :snake: (3.5 must be ok as well, but not tested)
- Webcam

### Installing

- First of all you need to clone the project
    ```
    git clone https://github.com/Ignisor/face-screenlock.git
    ```
- It's recommended to create and use [virtual environment](https://docs.python.org/3/library/venv.html)
- Install requirements
    ```
    pip install -r requirements.txt
    ```
- Plug in your web cam
- Put your photo (full face) in the directory and name it `user`, e.g. `user.jpg`
- Run
    ```
    python run.py
    ```

## Using with other desktop environments
If you want to use it with other than Cinnamon desktop environments. You can change `SCREENSAVER_COMMAND` to command for your desktop environment, e.g. `SCREENSAVER_COMMAND = 'gnome-screensaver-command'`. 
In some cases you may be need to change `LOCK_ARGS` as well. Or even change `lock_screen` function behaviour.
