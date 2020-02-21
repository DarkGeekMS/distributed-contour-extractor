import time
import zmq
import cv2

# producer
"""
    takes video and pushes its frame.
    Args:
        address  : string of the ip address followed by the port to make the connection with ostu_node.
        videoPath: string path to any video.

"""
def producer(address , videoPath):

    #make the connections
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind(address)

    #open the video
    cap = cv2.VideoCapture(videoPath)

    #if video not exists exit with error message
    if (cap.isOpened()== False):
        print("Error opening video file")
        exit()

    # Read until video is completed
    while(cap.isOpened()):
        # get frame by frame from the video
        ret, frame = cap.read()
        if ret == True:
            #convert the frame to gray scaled one
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # keep the frame in dictionary to send it as json object
            work_message = { 'frame' : gray }

            #send the frame
            zmq_socket.send_pyobj(work_message)
        # if error occurs break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()