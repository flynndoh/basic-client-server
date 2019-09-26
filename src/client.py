# IMPORTS
from utils import *
import constants.config as cfg
import constants.responses as responses


# Start of class ---------------------------------------------------------------
class Client:
    """
        The Client class can be instantiated and has various creation/deletion
        methods, in addition to methods that send and receive packets to and from a server.
    """

    def __init__(self, command, server_ip_address, server_port):
        """
            Initialise a client object.
        """
        self.command = command
        self.server_ip_address = server_ip_address
        self.server_port = server_port
        self.server_full_address = (server_ip_address, int(server_port))
        self.sc = None
        self.dt_req_packet = None


    # Operational functions ----------------------------------------------------
    def send_packet(self, packet):
        """
            Given a packet, send it through the open socket.
        """
        if self.sc is not None and packet == self.dt_req_packet:
            print(responses.STATUS_SENDING_PACKET.format(packet, self.server_ip_address, self.server_port))

            try:
                # Set the socket's timeout to a given time
                self.sc.settimeout(cfg.CONFIG_RESPONSE_WAITTIME)

                # Send the created packet to the server over the open socket
                self.sc.sendto(packet, self.server_full_address)

                # Wait for and capture the server's response
                data, bounce_back_address = self.sc.recvfrom(4096)

                if len(data) is not None:
                    print(responses.SUCCESS_RECEIVED_BOUNCE_BACK.format(bounce_back_address[0], bounce_back_address[1]))

                    # If the response packet is valid
                    if self.validate_bounce_back(data, bounce_back_address):
                        self.print_bounce_back(data)

                else:
                    print(responses.ERROR_MALFORMED_BOUNCE_BACK.format(bounce_back_address[0], bounce_back_address[1], data))

            except socket.timeout:
                print(responses.ERROR_BOUNCE_BACK_TIMEOUT.format(responses.CONFIG_RESPONSE_WAITTIME))

            except ConnectionResetError:
                print(responses.ERROR_CONNECTION_REFUSED.format(self.server_ip_address, self.server_port))

        # If the request packet is not the client's packet
        elif packet != self.dt_req_packet:
            print(responses.ERROR_DT_REQUEST_PACKET_MISMATCH)

        # If there is no open socket
        elif self.sc is None:
            print(responses.ERROR_NO_SOCKET)


    def validate_bounce_back(self, data, bounce_back_address):
        """
            Runs the given packet through various validity checks.
            Returns true if every check is passed, false otherwise.
        """
        error_codes = []

        # Check the size of the response
        if len(data) < 13:
            error_codes.append(1)

        # Check that the MagicNo field contains 0x497E
        elif ((data[0] << 8) | data[1]) != 0x497E:
            error_codes.append(2)

        # Check that the PacketType field contains 0x0002
        elif ((data[2] << 8) | data[3]) != 0x0002:
            error_codes.append(3)

        # Check that the LanguageCode field contains a code from the supported languages
        elif ((data[4] << 8) | data[5]) not in cfg.CONFIG_LANGUAGE_CODES:
            error_codes.append(4)

        # Check that the Year field is lower than 2100
        elif ((data[6] << 8) | data[7]) >= 2100:
            error_codes.append(5)

        # Check that the Month field is a number between 1 and 12
        elif not (1 <= data[8] <= 12):
            error_codes.append(6)

        # Check that the Day field is a number between 1 and 31
        elif not (1 <= data[9] <= 31):
            error_codes.append(7)

        # Check that the Hour field is a number between 0 and 23
        elif not (0 <= data[10] <= 23):
            error_codes.append(8)

        # Check that the Minute field is a number between 0 and 59
        elif not (0 <= data[11] <= 59):
            error_codes.append(9)

        # Check that the Length field is a valid representation of the packet
        elif len(data) != (data[12] + 13):
            print("len(data):",len(data))
            print("(data[12] + 13)",(data[12] + 13))
            error_codes.append(10)

        if len(error_codes) == 0:
            print(responses.SUCCESS_VALID_BOUNCE_BACK.format(bounce_back_address[0], bounce_back_address[1], data))
            return True

        else:
            print(responses.ERROR_MALFORMED_BOUNCE_BACK.format(bounce_back_address[0], bounce_back_address[1], data, error_codes))
            return False


    def print_bounce_back(self, data):
        """
            Given a packet, print the contents of the packet in a readable way.
        """
        print("\n--------------------------------------------------")
        print("- MagicNo:        {}".format(hex((data[0] << 8) | data[1])))
        print("- PacketType:     {}".format((data[2] << 8) | data[3]))
        print("- LanguageCode:   {}".format((data[4] << 8) | data[5]))
        print("- Year:           {}".format((data[6] << 8) | data[7]))
        print("- Month:          {:0>2}".format(data[8]))
        print("- Day:            {:0>2}".format(data[9]))
        print("- Hour:           {:0>2}".format(data[10]))
        print("- Minute:         {:0>2}".format(data[11]))
        print("- Length:         {}".format(data[12]))
        print("-" * 50)
        if data[12] > 0:
            print("- Text:           {}".format(data[13:].decode()))
        print("-" * 50)


    # Creation functions -------------------------------------------------------
    def create_udp_socket(self):
        """
            Simply creates and opens a UDP socket.
            The socket is accessible using 'self.sc'.
        """
        if self.sc is None:
            print(responses.STATUS_CREATING_UDP_SOCKET)

            # Create UDP socket
            self.sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        else:
            print(responses.ERROR_SOCKET_ALREADY_EXISTS)


    def create_dt_request_packet(self):
        """
            Creates a date/time request packet.
            Returns a valid packet that is ready to be sent to a server.
            Groups of bytes are accessible via: (byte_a << 8) | byte_b.
        """
        if self.dt_req_packet is None:
            print(responses.STATUS_CREATING_DT_PACKET)

            # Magic number (2 bytes)
            byte_1 = 0x49
            byte_2 = 0x7E

            # Packet type (2 bytes)
            byte_3 = 0x00
            byte_4 = 0x01

            # Request type (2 bytes)
            byte_5 = 0x00
            byte_6 = 0x01  # default to date

            if self.command == "date":
                byte_6 = 0x01
            elif self.command == "time":
                byte_6 = 0x02

            self.dt_req_packet = bytearray([byte_1, byte_2, byte_3, byte_4, byte_5, byte_6])
            return self.dt_req_packet
        else:
            print(responses.ERROR_DT_REQUEST_ALREADY_EXISTS)


    # Deletion functions -------------------------------------------------------
    def delete_udp_socket(self):
        """
            Closes and deletes an open UDP socket.
        """
        if self.sc is not None:
            print(responses.STATUS_CLOSING_UDP_SOCKET)
            self.sc.close()
            print(responses.SUCCESS_DELETING_UDP_SOCKET)
            self.sc = None

        else:
            print(responses.ERROR_NO_SOCKET)


    def delete_dt_request_packet(self):
        """
            Deletes (overwrites) the existing date/time request packet.
        """
        if self.dt_req_packet is not None:
            print(responses.SUCCESS_DELETING_DT_REQ_PACKET)
            self.dt_req_packet = None

        else:
            print(responses.ERROR_NO_REQ_PACKET)


# End of class =================================================================


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


def check_input(input_array):
    """
        This is the parent function that calls specific checking functions.
        Returns true if all tests are passed, false otherwise.
    """
    if len(input_array) != 3:
        print(responses.ERROR_INVALID_INPUT)
        return False

    if not valid_command(input_array):
        print(responses.ERROR_INVALID_COMMAND.format(input_array[0], cfg.CONFIG_VALID_REQUESTS))
        return False

    if not valid_connection(input_array):
        print(responses.ERROR_INVALID_CONNECTION.format(input_array[1]))
        return False

    if not valid_port(input_array):
        print(responses.ERROR_INVALID_PORT_NUMBER.format(input_array[2]))
        return False

    return True


def start_client(input_array):
    """
        Instantiates a client object and instructs it to create a socket,
        create a date/time request packet and send it to a server.
    """
    print(responses.STATUS_STARTING_CLIENT)

    # Instantiate a new client object with the provided command and server information
    client = Client(input_array[0], input_array[1], input_array[2])

    # Create a new UDP socket
    client.create_udp_socket()

    # Create a date/time request packet
    dt_req_packet = client.create_dt_request_packet()

    # Send the packet to the server provided
    client.send_packet(dt_req_packet)


# RUNTIME
if __name__ == '__main__':
    input_array = read_from_terminal()
    valid_input = check_input(input_array)

    if valid_input:
        print(responses.SUCCESS_VALID_INPUT)
        start_client(input_array)
