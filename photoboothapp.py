from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import datetime
import imutils
import cv2
import numpy as np
import socket
import pickle
import struct



class PhotoBoothApp:
    def __init__(self):
        self.frame = None
        self.root = tk.Tk()
        self.root.geometry('1020x500')
        # self.root.resizable(False, False)
        self.root.configure(background='#462d6b')
        # self.panel = None
        self.HOST_IP = None 
        self.VIDEO_PORT = None
        self.CONTROL_PORT = None
        image = Image.open("start_img.jpg") 
        image = ImageTk.PhotoImage(image)
        self.panel = tk.Label(image=image)
        self.panel.image = image
        self.panel.grid(column=0, rowspan=15)

        tk.Label(self.root, text="IP", bg='#462d6b', fg='white', font=10, anchor="e", width=20).grid(row=0, column=1)
        tk.Label(self.root, text="VIDEO PORT", bg='#462d6b', fg='white', font=10, anchor="e", width=20).grid(row=1, column=1)
        tk.Label(self.root, text="CONTROL PORT", bg='#462d6b', fg='white', font=10, anchor="e", width=20).grid(row=2, column=1)

        self.e1 = tk.Entry(self.root)
        self.e1.grid(row=0, column=2)
        self.e2 = tk.Entry(self.root)
        self.e2.grid(row=1, column=2)
        self.e3 = tk.Entry(self.root)
        self.e3.grid(row=2, column=2)

        btn = tk.Button(self.root, text="CONNECT", command=self.start_video_loop)
        btn.grid(row=4, column=1)

        self.stopEvent = threading.Event()
        self.root.wm_title("pi_car GUI")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def start_video_loop(self):
        print( self.HOST_IP, self.VIDEO_PORT, self.CONTROL_PORT, " -- ")
        self.HOST_IP = self.e1.get() 
        self.VIDEO_PORT = int(self.e2.get())
        self.CONTROL_PORT = int(self.e3.get())
        print( self.HOST_IP, self.VIDEO_PORT, self.CONTROL_PORT)
        thread = threading.Thread(target=self.videoLoop, args=())
        thread.start()

    def videoLoop(self):
        # try:
        if self.HOST_IP is not None and self.VIDEO_PORT is not None and self.CONTROL_PORT is not None:
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client_socket.connect((self.HOST_IP, self.VIDEO_PORT))
            data = b""
            payload_size = struct.calcsize("Q")
            
            while not self.stopEvent.is_set():
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
                image = Image.fromarray(show_frame)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    # self.panel.pack(side="left", padx=10, pady=10)
        
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

            client_socket.close()
        else:
            tk.Label(self.root, text="IP").pack(side="IP ERROR", padx=10, pady=10)
        # except:
        #     print("[INFO] caught a RuntimeError")


    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.root.quit()