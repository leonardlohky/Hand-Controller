# Hand-Controller

## About
Hand-Controller is a gesture-based recognition system to control your computer. 
It can be used to move the pointer, click and scroll. Also included is a virtual 
gesture-controlled keyboard.

## Features
### Gesture Recognition:
<details>
<summary>Move cursor</summary>
 <figure>
  <figcaption>Move cursor. Used when only the index finger is pointing up.
  This gesture moves the cursor to the desired location. Speed of the cursor 
  movement is proportional to the speed of hand.</figcaption>
</figure>
</details>

<details>
<summary>Left Click</summary>
 <figure>
  <figcaption>Left Click. Used when only the index and middle finger is pointing up 
  and close together. The distance between the tip of the index and middle finger 
  is calculated. If the distance is below the threshold, a single left click is 
  performed.</figcaption>
</figure>
</details>

<details>
<summary>Scroll Up/Down</summary>
 <figure>
  <figcaption>Scroll Up/Down. Used when only the index, middle and ring finger 
  is pointing up. Scroll direction and speed is controlled by the location of 
  tip of the index finger.</figcaption>
</figure>
</details>

<details>
<summary>Bringup Keyboard</summary>
 <figure>
  <figcaption>Bringup Keyboard. Used when only the index, middle, ring and pinky 
  finger. Brings up the virtual gesture-controlled keyboard for typing.</figcaption>
</figure>
</details>

### Virtual Keyboard:
Hover over the key with your index finger that you wish to press. After that, perform
the Left Click gesture as described before to press the key. To go back to "Mouse"
mode, simply hover over the "Mouse" key on the virtual keyboard and perform a
Left Click gesture.

## Getting Started
### Pre-requisites
- Python: 3.8.5
- Environment: Anaconda. Download link [here](https://www.anaconda.com/products/individual)
- Hardware: A computer with webcam

### 1. Requirements.
Install the necessary required packages through the provided `requirements.txt`
file using Anaconda prompt.
```
pip install -r requirements.txt
```

### 2. Installation.
- Clone this repo:
```
git clone https://github.com/leonardlohky/Hand-Controller
```

## Usage
To run the application, you can use an IDE (e.g. Spyder) or navigate to the
location of `main.py` script type in the following in an Anaconda prompt.
```
python main.py
```

## License
Distributed under the [MIT License](LICENSE)

## Acknowledgement
This package was developed based on the original codes by Murtaza's Workshop,
which include:
- [AI Virtual Mouse](https://www.youtube.com/watch?v=8gPONnGIPgw)
- [AI Virtual Keyboard using OpenCV](https://www.youtube.com/watch?v=jzXZVFqEE2I&t=212s)