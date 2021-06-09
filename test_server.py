import socket, cv2, pickle, struct, imutils
import time

host_ip = '172.28.61.54'
VIDEO_RIGHT_PORT = 1122

socket_video_right = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_video_right.bind((host_ip, VIDEO_RIGHT_PORT))
socket_video_right.listen(2)

while True:
    client_socket, addr = socket_video_right.accept()
    print('RIGHT GOT CONNECTION FROM:', addr)
    if client_socket:
        # cap = cv2.VideoCapture(self.right_rtsp)
        cap = cv2.VideoCapture(0)
        while 1:
            try:
                rval, frame = cap.read()
                print(frame.shape)
                if rval:
                    # frame = imutils.resize(frame,width=320)
                    im_arr = cv2.imencode('.jpg', frame)[1].tobytes()
                    a = pickle.dumps(im_arr)
                    # print("RIGHT IMG_SIZE: ", len(a))
                    message = struct.pack("Q",len(a)) + a
                    client_socket.sendall(message)
                else:
                    time.sleep(0.5)
                    cap.release()
                    cap.open(0)
                    # print("rval false CAMERA")

            except:
                cap.release()
                client_socket.close()
                print("EXCEPT")
                break