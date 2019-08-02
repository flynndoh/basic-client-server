# IMPORTS
from client import Client
import socket

# CONFIGURATION VARIABLES
CONFIG_VALID_REQUESTS = ["date", "time"]


# ERROR MESSAGES
ERROR_INVALID_COMMAND = "ERROR: '{}' is not a valid command. Please provide one of the following: {}."
ERROR_INVALID_CONNECTION = "ERROR: Could not establish a connection to '{}'. Please verify the connection information."
ERROR_INVALID_PORT_NUMBER = "ERROR: The given port number ({}) is not within the range 1,024 and 64,000."
ERROR_INVALID_INPUT = "ERROR: Input is invalid, please check your input and try again."


# STATUS MESSAGES
STATUS_STARTING_CLIENT = "STATUS: Starting client..."


# SUCCESS MESSAGES
SUCCESS_VALID_INPUT = "SUCCESS: Input is valid."


# FUNCTIONS
def read_from_terminal():
    """
        Reads input from the terminal. Returns an array of the format:
            [0] -> command
            [1] -> ip address
            [2] -> port
    """
    raw_input = input()
    input_array = raw_input.strip().split()
    return input_array


def valid_command(input_array):
    """ """
    if input_array[0] in CONFIG_VALID_REQUESTS:
        return True
    else:
        return False


def valid_connection(input_array):
    """ """
    try:
        sc = socket.getaddrinfo(input_array[1], input_array[2])
        if sc:
            return True
        else:
            return False
    except:
        return False


def valid_port(input_array):
    """ """
    try:
        if (1024 < int(input_array[2]) < 64000):
            return True
        else:
            return False
    except:
        return False


def check_input(input_array):
    """ """
    if len(input_array) != 3:
        print(ERROR_INVALID_INPUT)
        return False

    if not valid_command(input_array):
        print(ERROR_INVALID_COMMAND.format(input_array[0], CONFIG_VALID_REQUESTS))
        return False

    if not valid_connection(input_array):
        print(ERROR_INVALID_CONNECTION.format(input_array[1]))
        return False

    if not valid_port(input_array):
        print(ERROR_INVALID_PORT_NUMBER.format(input_array[2]))
        return False

    return True


def begin_transaction(input_array):
    """ """
    print(STATUS_STARTING_CLIENT)

    # Instantiate a new client object with the provided command and server information
    client = Client(input_array[0], input_array[1], input_array[2])

    # Create a new UDP socket
    client.create_udp_socket()

    # Create a date/time request packet
    dt_req_packet = client.create_dt_request_packet()

    # Send the packet to the server provided and recieve bounceback
    bounce_back = client.send_packet(dt_req_packet)


# RUNTIME
if __name__ == '__main__':
    input_array = read_from_terminal()
    valid_input = check_input(input_array)

    if valid_input:
        print(SUCCESS_VALID_INPUT)
        begin_transaction(input_array)
        #print()
        #print("x-"*80)
        #print()
