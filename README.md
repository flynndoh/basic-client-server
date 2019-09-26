# Client-Server Communication using Websockets

This is a small piece of software that uses websockets to tell the date and time in 3 different languages: English, Maori and German.
This project features a basic client and server implementation. The client can send a request to the server and ask for the current date or time of day in a requested language.

## Prerequisites
- Python 3 installed
- 3 ports that aren't in use

## User Guide
1. Clone/download the repository to a desired location.
2. Open a terminal session inside of the desired location.
3. Start an instance of the server by running the command ```python3 server.py```. 
4. Start an instance of the client by running the command ```python3 client.py```.
5. In the server shell, enter in 3 unique ports in the range 1,024-64,000. Each port corresponds to a language that the response will be translated to. The first port is English, the second is Maori, the final is German. e.g. ```3333 4444 5555```.
6. In the client shell, enter in a desired request. e.g. ```date localhost 3333```or ```time localhost 3333```.
7. The output in the server's shell will show an acknowledgement of the client's request and then a response will be sent to the client.
8. The output in the client's shell will show the request packet construction, sending and then the received packet's contents.

## Extension
Feel free to extend this software to include other languages and functionality. :)
