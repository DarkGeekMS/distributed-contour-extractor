import time
import zmq
import cv2

# consumer1
"""
    takes video frame and pushes its binary image.
    Args:
        addressReceive: string of the ip address followed by the port to make the connection with input_node.
        addressSend   : string of the ip address followed by the port to make the connection with collector_node.

"""

def consumer1(addressReceive, addressSend):

    #make the connections
    context = zmq.Context()
    # receive video frames
    consumer1_receiver = context.socket(zmq.PULL)
    consumer1_receiver.connect(addressReceive)
    # send binary result
    consumer1_sender = context.socket(zmq.PUSH)
    consumer1_sender.connect(addressSend)


    while True:   # i think we need to change this condition to terminate when the video finishes

        #receive the frame (grayScaled)
        work = consumer1_receiver.recv_pyobj()
        frame = work['frame']

        #apply ostu thresholding technique on it
        binary, threshold = cv2.threshold(frame , 0 , 255 , cv2.THRESH_OTSU)
        msg = {'binary' : binary}
        #push the binary result to the collector
        consumer1_sender.send_pyobj(msg)