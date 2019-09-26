# GENERAL
ERROR_INVALID_PORT_NUMBER = "ERROR: The given port number ({}) is not an integer within the range 1,024 to 64,000."
ERROR_INVALID_CONNECTION = "ERROR: Could not establish a connection to '{}'. Please verify the connection information."
ERROR_INVALID_INPUT = "ERROR: Input is invalid, please check your input and try again."
SUCCESS_VALID_INPUT = "SUCCESS: Input is valid."
INFO_PORT_NUMBERS = "Enter 3 port numbers to listen to:\n (English) (Maori) (German)"
INFO_CLIENT_SETUP = "Enter your request in the format:\n ('date' or 'time') (host) (port)"

# CLIENT ERROR MESSAGES
ERROR_SOCKET_ALREADY_EXISTS = "ERROR: UDP socket already exists. Please call 'client.delete_udp_socket()' before trying to re-create the socket."
ERROR_DT_REQUEST_ALREADY_EXISTS = "ERROR: A date/time request packet already exists. Please call 'client.delete_dt_req_packet()' before trying to re-create the packet."
ERROR_DT_REQUEST_PACKET_MISMATCH = "ERROR: The provided packet does not match the packet in the instance of the Client."
ERROR_NO_SOCKET = "ERROR: No UDP socket currently exists."
ERROR_NO_REQ_PACKET = "ERROR: No date/time request packet currently exists."
ERROR_MALFORMED_BOUNCE_BACK = "ERROR: The server ({}:{}) has provided a malformed bounce back of: \n{}.\nError codes: {}"
ERROR_BOUNCE_BACK_TIMEOUT = "ERROR: Exceeded response wait time of {} second(s)."
ERROR_CONNECTION_REFUSED = "ERROR: The server ({}:{}) has refused the connection attempt."
ERROR_INVALID_COMMAND = "ERROR: '{}' is not a valid command. Please provide one of the following: {}."
ERROR_CLIENT_INVALID_INPUT = "ERROR: Input is invalid, please check your input and try again."


# CLIENT STATUS MESSAGES
STATUS_CREATING_UDP_SOCKET = "STATUS: UDP socket is being created..."
STATUS_CREATING_DT_PACKET = "STATUS: Date/time request packet is being created..."
STATUS_SENDING_PACKET = "STATUS: Sending packet: {} to {}:{}..."
STATUS_CLOSING_UDP_SOCKET = "STATUS: UDP socket is now closing..."
STATUS_STARTING_CLIENT = "STATUS: Starting client..."


# CLIENT SERVER SUCCESS MESSAGES
SUCCESS_RECEIVED_BOUNCE_BACK = "SUCCESS: Received a packet from the server ({}:{})."
SUCCESS_VALID_BOUNCE_BACK = "SUCCESS: The server ({}:{}) has provided a valid bounce back."
SUCCESS_DELETING_UDP_SOCKET = "SUCCESS: UDP socket has been deleted."
SUCCESS_DELETING_DT_REQ_PACKET = "SUCCESS: Date/time request packet has been deleted."

# SERVER ERROR MESSAGES
ERROR_SERVER_INVALID_PORT_NUMBER = "ERROR: All three port numbers ({}, {}, {}) must be integers between 1,024 and 64,000."
ERROR_DUPLICATE_PORT_NUMBER = "ERROR: All three port numbers ({}, {}, {}) must be unique."
ERROR_SERVER_INVALID_INPUT = "ERROR: Input is invalid, please provide exactly three port numbers (1: English, 2: Maori, 3: German)."
ERROR_PORT_FORBIDDEN = "ERROR: At least one of the given port numbers are occupied by another process."
ERROR_SOCKET_BIND_CREATION = "ERROR: Could not create sockets or bind ports."
ERROR_FOREIGN_PORT = "ERROR: The incoming packet was from an unrecognised port number."
ERROR_PROCESS_INCOMING = "ERROR: Failed to process the incoming packet."
ERROR_MALFORMED_REQUEST = "ERROR: The client ({}:{}) has provided a malformed request of: {}."
ERROR_TEXT_PAYLOAD_OVERFLOW = "ERROR: The textual representation payload has exceeded the maximum length of 255."


# SERVER STATUS MESSAGES
STATUS_SERVER_STARTING = "STATUS: Starting server..."
STATUS_CREATING_SOCKETS = "STATUS: Creating three language sockets..."
STATUS_BINDING_PORTS = "STATUS: Binding language ports, English: {}, Maori: {}, German: {}..."
STATUS_STARTING_TO_LISTEN = "STATUS: Listening to open ports..."
STATUS_SERVER_SHUTDOWN = "STATUS: Shutting down server..."
STATUS_CLOSING_SOCKETS = "STATUS: Closing active sockets..."


# SERVER SUCCESS MESSAGES
SUCCESS_SOCKETS_CREATED = "SUCCESS: Three sockets have been created."
SUCCESS_PORTS_BOUND = "SUCCESS: Three language ports are now bound."
SUCCESS_RECEIVED_INCOMING = "SUCCESS: Received packet: {} from the port: {}"
SUCCESS_RESPONSE_PACKET_CREATED = "SUCCESS: Response packet created."
SUCCESS_RESPONSE_PACKET_SENT = "SUCCESS: Response packet sent to {}:{}."
SUCCESS_REQUEST_VALID = "SUCCESS: The client's ({}:{}) request: {} is valid."
