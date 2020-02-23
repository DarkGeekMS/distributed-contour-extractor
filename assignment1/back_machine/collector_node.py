from config.parser import get_config_from_json
import argparse
import time
import zmq

def collector(addressReceive, addressSend):
    """
    takes  binary image and pushes it to the contours_node.
    Args:
        addressReceive: string of the ip address followed by the port to make the connection with ostu_node.
        addressSend   : string of the ip address followed by the port to make the connection with contours_node.
    """
    #make the connections
    context = zmq.Context()
    # receive binary image
    collector_receiver = context.socket(zmq.PULL)
    collector_receiver.bind(addressReceive)
    # send the binary image to contours_node
    collector_sender = context.socket(zmq.PUSH)
    collector_sender.bind(addressSend)

    while True: #same as ostu needs to be changed to terminate after the last frame

        #get the frames from ostu node and send them to contours node
        work = collector_receiver.recv_pyobj()
        collector_sender.send_pyobj(work)

def main():
    """Main driver of collector node"""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-id', '--node_id', type=int, help='id for the currently running node')
    argparser.add_argument('-n', '--total_num', type=str, help='total number of consumer nodes')
    
    args = argparser.parse_args()

    config = get_config_from_json("back_machine/config/server.json") # get other nodes addresses from json config

    recv_address = config.collector_sockets[args.node_id-1] # get the receive address based on the node id
    send_address = config.remote_sockets[args.node_id-1] # get the send address based on the node id

    collector(recv_address, send_address) # call the OSTU consumer process

if __name__=='__main__':
    main()        