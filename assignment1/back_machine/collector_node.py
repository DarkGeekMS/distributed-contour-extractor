import time
import zmq

# collector
"""
    takes  binary image and pushes it to the contours_node.
    Args:
        addressReceive: string of the ip address followed by the port to make the connection with ostu_node.
        addressSend   : string of the ip address followed by the port to make the connection with contours_node.

"""

def collector(addressReceive, addressSend):

    #make the connections
    context = zmq.Context()
    # receive binary image
    collector_receiver = context.socket(zmq.PULL)
    collector_receiver.connect(addressReceive)
    # send the binary image to contours_node
    collector_sender = context.socket(zmq.PUSH)
    collector_sender.connect(addressSend)

    while True: #same as ostu needs to be changed to terminate after the last frame

        #get the frames from ostu node and send them to contours node
        work = collector_receiver.recv_pyobj()
        collector_sender.send_pyobj(work)