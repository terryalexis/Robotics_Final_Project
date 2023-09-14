# Final Project README

This folder includes the material used to develop team P.A.S.E's final project in CS5510-6510. The materials are split into folders based on general tasks that a Tello drone must do to find and land on an orange piece of paper.

## Installation

These instructions are written under the assumption that python3 is installed.

Create and activate virtual environment

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install the requirements using the requirements.txt file provided in this directory
* Note: You may need to update pip 

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

***need scikit-image and skimage package for paper detection 
   
## Executing tello drone search and land operation

Steps to run the operation:

1. In a simple, indoor obstacle field with an off-white linoleum floor, turn on a charged Tello drone and place the drone on the ground. Tello will be flashing a yellow light waiting for commands.

2. Connect to the Tello drone via laptop connection. Change laptop network to the drone's network (e.g. TELLO-D8C17B). The drone will still be flashing yellow. 

3. Run main.py. Accept any "Accept access?***" windows which may pop up. The drone will then display a green light while executing commands.

The drone will then conduct search and land procedures, which include observing the environment (with a forward facing camera and imu), determining safe regions to continue searching in, detecting an orange paper, flying to the safe regions or the paper, and landing on the paper.

Drone battery run time is 6-13 min. After landing, the drone will display a red light, waiting for next commands.



