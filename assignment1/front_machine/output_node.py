from config.parser import get_config_from_json
import pandas as pd
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

    #create an output dictionary
    out_dict = {"Frame Number": [], "Contours": []}
    counter = 0

    #receive the contours and save them in a txt file
    while True:
        work = results_receiver.recv_pyobj()
        data = work['contours']

        #add the results to output dictionary
        out_dict["Frame Number"].append("Frame #{}".format(counter))
        out_dict["Contours"].append(data)
        counter += 1   

        #create a dataframe and write outputs
        out_df = pd.DataFrame(out_dict, columns=["Frame Number", "Contours"])    
        out_df.to_csv(outputPath)   

def main():
    """Main driver of output node"""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-t', '--text_path', type=str, help='path to the output text')
    argparser.add_argument('-n', '--total_num', type=str, help='total number of consumer nodes')
    
    args = argparser.parse_args()

    config = get_config_from_json("front_machine/config/server.json") # get other nodes addresses from json config

    result_collector(config.output_socket, args.text_path) # call the output collector process

if __name__=='__main__':
    main()    