from config.parser import get_config_from_json
import argparse
import time
import zmq
import cv2
import math

def consumer(addressReceive, addressSend):
    """
    takes video frame and pushes its binary image.
    Args:
        addressReceive: string of the ip address followed by the port to make the connection with input_node.
        addressSend   : string of the ip address followed by the port to make the connection with collector_node.
    """
    #make the connections
    context = zmq.Context()
    # receive video frames
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect(addressReceive)
    # send binary result
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect(addressSend)


    while True:   # i think we need to change this condition to terminate when the video finishes

        #receive the frame (grayScaled)
        work = consumer_receiver.recv_pyobj()
        frame = work['frame']

        #apply ostu thresholding technique on it
        binary, threshold = cv2.threshold(frame , 0 , 255 , cv2.THRESH_OTSU)
        msg = {'binary' : binary}
        #push the binary result to the collector
        consumer_sender.send_pyobj(msg)

def main():
    """Main driver of ostu consumer node"""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-id', '--node_id', type=int, help='id for the currently running node')
    
    args = argparser.parse_args()

    config = get_config_from_json("back_machine/config/server.json") # get other nodes addresses from json config

    send_address = config.collector_sockets[math.floor(args.node_id/2.0)] # get the send address based on the node id

    consumer(config.input_socket, send_address) # call the OSTU consumer process

if __name__=='__main__':
    main()            