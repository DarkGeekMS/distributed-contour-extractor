import time
import zmq
import cv2

# consumer2
"""
    takes  binary image and pushes its contours to the output_node.
    Args:
        addressReceive: string of the ip address followed by the port to make the connection with collector_node.
        addressSend   : string of the ip address followed by the port to make the connection with output_node.

"""

def consumer2(addressReceive, addressSend):

    #make the connections
    context = zmq.Context()
    # receive binary image
    consumer2_receiver = context.socket(zmq.PULL)
    consumer2_receiver.connect(addressReceive)
    # send its contours to output_node
    consumer2_sender = context.socket(zmq.PUSH)
    consumer2_sender.connect(addressSend)


    while True:  #to be changed

        #receive the binary frame
        work = consumer2_receiver.recv_pyobj()
        data = work['binary']

        #get the contours
        _, contours, _ = cv2.findContours(data, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        result = {'contours' : contours}

        #send the contours
        consumer2_sender.send_pyobj(result)