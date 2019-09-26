import socket
import constants.config as cfg


def valid_command(input_array):
    """ """
    return input_array[0] in cfg.CONFIG_VALID_REQUESTS


def valid_connection(input_array):
    """ """
    try:
        return socket.getaddrinfo(input_array[1], input_array[2]) is not None
    except:
        return False


def valid_port(input_array):
    """ """
    try:
        return 1024 < int(input_array[2]) < 64000
    except:
        return False