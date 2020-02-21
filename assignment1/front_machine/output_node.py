import time
import zmq

# result_collector
"""
    takes  controur values of an image and save them in a text file.
    Args:
        address : string of the ip address followed by the port to make the connection with contours_node.
"""

def result_collector(address):

    #make the connections
    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind(address)

    #create an output file

    #TODO : receive the contours and save them in a txt file
    while True:
        work = results_receiver.recv_pyobj()
        data = work['contours']

        #save the result in output file