from config.parser import get_config_from_json
import argparse
import time
import zmq

def result_collector(address, outputPath):
    """
    takes  controur values of an image and save them in a text file.
    Args:
        address   : string of the ip address followed by the port to make the connection with contours_node.
        outputPath: string path to the output text.
    """    
    #make the connections
    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind(address)

    #create an output file
    file = open(outputPath, 'w+')
    counter = 0

    #receive the contours and save them in a txt file
    while True:
        work = results_receiver.recv_pyobj()
        data = work['contours']

        #save the result in output file
        file.write("Frame #{}: \n".format(counter))
        file.write(data)
        file.write("\n")

        counter += 1   

    file.close()     

def main():
    """Main driver of output node"""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-t', '--text_path', type=str, help='path to the output text')
    
    args = argparser.parse_args()

    config = get_config_from_json("front_machine/config/server.json") # get other nodes addresses from json config

    result_collector(config.output_socket, args.text_path) # call the output collector process

if __name__=='__main__':
    main()    