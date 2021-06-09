import tkinter as tk
import numpy as np
import socket
import pickle
import struct
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2
import os

HOST_IP = '172.28.61.198' # paste your server ip address here
VIDEO_PORT = 1122
CONTROL_PORT = 1123

def write_slogan():
    print("Tkinter is easy to use!")


def get_frame(root):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST_IP, VIDEO_PORT))
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(20) # 4K
            if not packet: break
            data+=packet
        packed_msg_size = data[0:payload_size]

        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(256)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        show_frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), 1)
        cv2.imshow("RECEIVING VIDEO", show_frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
    client_socket.close()


root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
button.pack(side=tk.LEFT)
slogan = tk.Button(frame,
                   text="Hello",
                   command=write_slogan)
slogan.pack(side=tk.LEFT)

root.mainloop()



# lets make the client code



# create socket

    
