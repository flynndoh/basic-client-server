# IMPORTS
import socket
import select
import datetime


# CONFIGURATION VARIABLES
COMMAND_TYPES = [0x0001, 0x0002]    # 1:date, 2:time
MONTHS_MAORI = ["Kohitatea", "Hui-tanguru", "Poutu-te-rangi", "Paenga-whawha", "Haratua", "Pipiri", "Hongongoi", "Here-turi-koka", "Mahuru", "Whiringa-a-nuku", "Whiringa-a-rangi", "Hakihea"]
MONTHS_GERMAN = ["Januar", "Februar", "Marz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]


# ERROR MESSAGES
ERROR_INVALID_PORT_NUMBER = "ERROR: All three port numbers ({}, {}, {}) must be integers between 1,024 and 64,000."
ERROR_DUPLICATE_PORT_NUMBER = "ERROR: All three port numbers ({}, {}, {}) must be unique."
ERROR_INVALID_INPUT = "ERROR: Input is invalid, please provide exactly three port numbers (1: English, 2: Maori, 3: German)."
ERROR_PORT_FORBIDDEN = "ERROR: At least one of the given port numbers are occupied by another process."
ERROR_SOCKET_BIND_CREATION = "ERROR: Could not create sockets or bind ports."
ERROR_NO_SOCKET = "ERROR: No UDP sockets currently exist."
ERROR_FOREIGN_PORT = "ERROR: The incoming packet was from an unrecognised port number."
ERROR_PROCESS_INCOMING = "ERROR: Failed to process the incoming packet."
ERROR_MALFORMED_REQUEST = "ERROR: The client ({}:{}) has provided a malformed request of: {}."
ERROR_TEXT_PAYLOAD_OVERFLOW = "ERROR: The textual representation payload has exceeded the maximum length of 255."


# STATUS MESSAGES
STATUS_SERVER_STARTING = "STATUS: Starting server..."
STATUS_CREATING_SOCKETS = "STATUS: Creating three language sockets..."
STATUS_BINDING_PORTS = "STATUS: Binding language ports, English: {}, Maori: {}, German: {}..."
STATUS_STARTING_TO_LISTEN = "STATUS: Listening to open ports..."
STATUS_SERVER_SHUTDOWN = "STATUS: Shutting down server..."
STATUS_CLOSING_SOCKETS = "STATUS: Closing active sockets..."


# SUCCESS MESSAGES
SUCCESS_VALID_INPUT = "SUCCESS: Input is valid."
SUCCESS_SOCKETS_CREATED = "SUCCESS: Three sockets have been created."
SUCCESS_PORTS_BOUND = "SUCCESS: Three language ports are now bound."
SUCCESS_RECEIVED_INCOMING = "SUCCESS: Received packet: {} from the port: {}"
SUCCESS_RESPONSE_PACKET_CREATED = "SUCCESS: Response packet created."
SUCCESS_RESPONSE_PACKET_SENT = "SUCCESS: Response packet sent to {}:{}."
SUCCESS_REQUEST_VALID = "SUCCESS: The client's ({}:{}) request: {} is valid."


# Start of class ---------------------------------------------------------------
class Server:
    """
        The Server class can be instantiated and has various creation/deletion
        methods, in addition to methods that send and receive packets to and from a client.
    """

    def __init__(self, port1, port2, port3):
        """
            Initialise a server object
        """
        # Initialise ports
        self.ports = {
                        "English" : int(port1),
                        "Te reo Maori" : int(port2),
                        "German" : int(port3)
                     }

        # Initialise sockets
        self.english_sc = None
        self.maori_sc = None
        self.german_sc = None


    # Operational functions ----------------------------------------------------
    def begin_listening(self):
        """
            Begins listening to the open socekts and calls methods to process
            incoming packets when they are detected.
            Returns true when a packet comes in through a valid port, and false otherwise.
        """
        print(STATUS_STARTING_TO_LISTEN)
        sockets = [self.english_sc, self.maori_sc, self.german_sc]

        try:
            incoming, outgoing, exceptions = select.select(sockets, [], [])

            if incoming[0] == self.english_sc:
                self.process_incoming(incoming[0], self.english_sc, self.ports['English'])
                return True

            elif incoming[0] == self.maori_sc:
                self.process_incoming(incoming[0], self.maori_sc, self.ports['Te reo Maori'])
                return True

            elif incoming[0] == self.german_sc:
                self.process_incoming(incoming[0],  self.german_sc, self.ports['German'])
                return True

            else:
                print(ERROR_FOREIGN_PORT)
                return False

        except:
            print(ERROR_NO_SOCKET)
            return False


    def process_incoming(self, incoming, sc, port):
        """
            Given an incoming buffer, process all incoming packets on that buffer.
            Once a packet is marked as valid, create an appropriate response packet and
            send to the client's address.
        """
        try:
            data, bounce_back_address = sc.recvfrom(4096)
            print(SUCCESS_RECEIVED_INCOMING.format(data, port))

            if self.validate_request(data, bounce_back_address):

                # Form a response packet
                packet = self.create_dt_response_packet(data, port)
                if packet != None:
                    print(SUCCESS_RESPONSE_PACKET_CREATED)

                    # Send response packet to client
                    sc.sendto(packet, bounce_back_address)
                    print(SUCCESS_RESPONSE_PACKET_SENT.format(bounce_back_address[0], bounce_back_address[1]))

            else:
                print(ERROR_MALFORMED_REQUEST.format(bounce_back_address[0], bounce_back_address[1], data))

        except:
            print(ERROR_PROCESS_INCOMING)


    def validate_request(self, data, bounce_back_address):
        """
            Runs the given packet through various validity checks.
            Returns true if every check is passed, false otherwise.
        """
        error_codes = []

        # Check the size of the request
        if len(data) != 6:
            error_codes.append(1)

        # Check that the MagicNo field contains 0x497E
        elif ((data[0] << 8) | data[1]) != 0x497E:
            error_codes.append(2)

        # Check that the PacketType field contains 0x0001
        elif ((data[2] << 8) | data[3]) != 0x0001:
            error_codes.append(3)

        # Check that the RequestType field contains either 0x0001 or 0x0002
        elif ((data[4] << 8) | data[5]) not in COMMAND_TYPES:
            error_codes.append(4)

        if len(error_codes) == 0:
            print(SUCCESS_REQUEST_VALID.format(bounce_back_address[0], bounce_back_address[1], data))
            return True

        else:
            return False


    # Creation functions -------------------------------------------------------
    def create_udp_sockets(self):
        """
            Creates three udp sockets and binds them to the given port numbers.
        """
        try:
            print(STATUS_CREATING_SOCKETS)
            self.english_sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.maori_sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.german_sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(SUCCESS_SOCKETS_CREATED)

            print(STATUS_BINDING_PORTS.format(self.ports['English'], self.ports['Te reo Maori'], self.ports['German']))
            self.english_sc.bind(('localhost', self.ports['English']))
            self.maori_sc.bind(('localhost', self.ports['Te reo Maori']))
            self.german_sc.bind(('localhost', self.ports['German']))
            print(SUCCESS_PORTS_BOUND)

        except OSError:
            print(ERROR_PORT_FORBIDDEN)

        except:
            print(ERROR_SOCKET_BIND_CREATION)


    def create_dt_response_packet(self, data, port):
        """
            Create an appropriate date/time response packet.
            Returns a valid response packet in the requested language.
        """
        now = datetime.datetime.now()

        # Magic number (2 bytes)
        byte_1 = 0x49
        byte_2 = 0x7E

        # Packet type (2 bytes)
        byte_3 = 0x00
        byte_4 = 0x02

        # Language Code (2 bytes)
        byte_5 = 0x00

        # English
        if port == self.ports['English']:
            byte_6 = 0x01

            # Date request
            if ((data[4] << 8) | data[5]) == 0x0001:
                textual_representation = "Today’s date is {} {:0>2}, {:0>4}".format(now.strftime("%B"), now.day, now.year)

            # Time request
            elif ((data[4] << 8) | data[5]) == 0x0002:
                textual_representation = "The current time is {:0>2}:{:0>2}".format(now.hour, now.minute)

        # Te reo Maori
        elif port == self.ports['Te reo Maori']:
            byte_6 = 0x02

            # Date request
            if ((data[4] << 8) | data[5]) == 0x0001:
                textual_representation = "Ko te ra o tenei ra ko {} {:0>2}, {:0>4}".format(MONTHS_MAORI[now.month-1], now.day, now.year)

            # Time request
            elif ((data[4] << 8) | data[5]) == 0x0002:
                textual_representation = "Ko te wa o tenei wa {:0>2}:{:0>2}".format(now.hour, now.minute)

        # German
        elif port == self.ports['German']:
            byte_6 = 0x03

            # Date request
            if ((data[4] << 8) | data[5]) == 0x0001:
                textual_representation = "Heute ist der {:0>2}. {} {:0>4}".format(now.day, MONTHS_GERMAN[now.month-1], now.year)

            # Time request
            elif ((data[4] << 8) | data[5]) == 0x0002:
                textual_representation = "Die Uhrzeit ist {:0>2}:{:0>2}".format(now.hour, now.minute)

        # Year (2 bytes)
        byte_7 = (now.year >> 8) & 0xFF
        byte_8 = now.year & 0xFF

        # Month (1 byte)
        byte_9 = now.month & 0xFF

        # Day (1 byte)
        byte_10 = now.day & 0xFF

        # Hour (1 byte)
        byte_11 = now.hour & 0xFF

        # Minute (1 byte)
        byte_12 = now.minute & 0xFF

        # Length (1 byte)
        text_in_bytes = textual_representation.encode()
        byte_13 = len(text_in_bytes) & 0xFF

        if len(text_in_bytes) > 0xFF:
            print(ERROR_TEXT_PAYLOAD_OVERFLOW)
            return None

        dt_res_packet = bytearray([ byte_1, byte_2, byte_3, byte_4, byte_5,
                                    byte_6, byte_7, byte_8, byte_9, byte_10,
                                    byte_11, byte_12, byte_13 ])

        # Text
        for byte in text_in_bytes:
            dt_res_packet.append(byte)

        return dt_res_packet


# End of class =================================================================


def read_from_terminal():
    """
        Reads input from the terminal. Returns an array of the format:
            [0] -> port number 1    (English)
            [1] -> port number 2    (Te reo Maori)
            [2] -> port number 3    (German)
    """
    raw_input = input()
    input_array = raw_input.strip().split()
    return input_array


def valid_port(input_array):
    """
        Checks the command line arguments are:
            - between 1024 and 64000 (not inclusive)
            - are unique
        Returns true if the test is passed, false otherwise.
    """
    port_array = []

    try:
        for port in input_array:
            if (1024 < int(port) < 64000) and int(port) not in port_array:
                port_array.append(int(port))

            elif not (1024 < int(port) < 64000):
                print(ERROR_INVALID_PORT_NUMBER.format(input_array[0], input_array[1], input_array[2]))
                return False

            elif int(port) in port_array:
                print(ERROR_DUPLICATE_PORT_NUMBER.format(input_array[0], input_array[1], input_array[2]))
                return False

    except:
        print(ERROR_INVALID_PORT_NUMBER.format(input_array[0], input_array[1], input_array[2]))
        return False

    if len(port_array) == 3:
        return True


def check_input(input_array):
    """
        This is the parent function that calls specific checking functions.
        Returns true if all tests are passed, false otherwise.
    """
    if len(input_array) != 3:
        print(ERROR_INVALID_INPUT)
        return False

    if not valid_port(input_array):
        return False

    return True


def start_server(input_array):
    """
        Instantiates a server object and instructs it to create and listen
        to three sockets for incoming packets.
    """
    print(STATUS_SERVER_STARTING)

    # Instantiate a new server object which listens to the provided ports
    server = Server(input_array[0], input_array[1], input_array[2])

    # Create 3 UDP sockets
    server.create_udp_sockets()

    # Begin listening for packets
    while 1:
        server.begin_listening()

    print(STATUS_CLOSING_SOCKETS)
    server.english_sc.close()
    server.maori_sc.close()
    server.german_sc.close()
    print(STATUS_SERVER_SHUTDOWN)


# RUNTIME
if __name__ == '__main__':
    input_array = read_from_terminal()
    valid_input = check_input(input_array)

    if valid_input:
        print(SUCCESS_VALID_INPUT)
        start_server(input_array)
