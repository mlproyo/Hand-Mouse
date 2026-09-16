# Hand Tracking Virtual Mouse 

A computer vision project that uses hand tracking via webcam to control mouse-like cursor movement, using **OpenCV** and **MediaPipe**.

>  **Disclaimer:** This was my first time working with computer vision. I mostly followed a tutorial to build this, so it's a learning project rather than an original implementation. Expect rough edges and incomplete features.

##  Features (Planned / In Progress)

- Real-time hand landmark detection using MediaPipe
- Tracks index and middle fingertip positions
- Frame reduction zone for mapping hand movement to screen coordinates
- Smoothening applied to reduce cursor jitter
- Designed to eventually map hand movement to actual mouse control (cursor movement, click gestures, etc.)

> Note: as of this version, the script detects and tracks fingertip landmarks but does not yet move the system cursor — that logic (`pyautogui`/`ctypes` mouse control) is still to be implemented.

##  Requirements

- Python 3.x
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- numpy

All dependencies are listed in `mouse_requirements.txt`.

##  Setup & Installation

1. **Clone the repository**
```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
```

2. **Create a virtual environment**
```bash
   python -m venv mouseenv
```

3. **Activate the virtual environment**
```bash
   mouseenv\Scripts\activate
```

4. **Install dependencies**
```bash
   pip install -r mouse_requirements.txt
```

##  Usage

Run the main script:

```bash
python hand_tracking.py
```

- Show your hand to the webcam — landmarks are detected and their coordinates tracked.
- Press **`q`** to quit the application.

##  How It Works

1. **Video capture** — Frames are read from the webcam and flipped horizontally for a mirror-like view.
2. **Hand detection** — MediaPipe's `Hands` solution processes each RGB frame and returns 21 landmark points per detected hand.
3. **Landmark extraction** — Each landmark's pixel coordinates (`cx`, `cy`) are stored in a list (`lmList`), indexed by landmark ID.
4. **Fingertip tracking** — The index fingertip (landmark 8) and middle fingertip (landmark 12) coordinates are pulled out for future gesture/cursor logic.
5. **Screen mapping (planned)** — `wScr`/`hScr` (screen resolution via `ctypes`), `frameR` (frame reduction margin), and `smoothening` are already set up to eventually map hand position within a defined frame region to actual screen coordinates for cursor movement.

##  Notes

- Screen resolution is retrieved using the Windows API (`ctypes.windll.user32`), so this script is currently **Windows-only**.
- Landmark drawing (`mp_draw.draw_landmarks`) is commented out in the current version — uncomment it if you want to visualize the hand skeleton on screen.
- This is very much a work-in-progress / learning exercise, built primarily by following an online tutorial to understand the basics of hand tracking with MediaPipe.

##  Credits

- Hand tracking powered by [MediaPipe](https://google.github.io/mediapipe/solutions/hands.html)
- Built while following an online tutorial on hand-tracking mouse control(https://youtu.be/8gPONnGIPgw?si=j6tjVqYRRd9ul-y6) 
