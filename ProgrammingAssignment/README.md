## Computer Networks Programming Assignment

The project consists of two main scripts: `210010033_server.py` for the server-side implementation and `210010033_client.py` for the client-side functionality.

### Server Script (`210010033_server.py`)

The `210010033_server.py` script handles incoming client connections, manages client details, and facilitates secure communication and video streaming. Here's an overview of its key functions:

- **Client Handling**: Every time a new client joins, a thread is created for handling its connnection
    - **`handle_client_connection()`**: Uses threading to handle multiple client connections concurrently. Its is responsible for receiving messages from the client in JSON format and call respective function to handle the requests.
    - **Client Details Management**:Client details (names and public keys) for secure communication using RSA encryption are stored in the `client_details` dictionary.
- **Message Broadcasting**:
    - **`broadcast()`**: A function responsible for broadcasting messages to all the clients currently connected to the server.
    - **`remove_client()`**: A function used to update dictionary whenever a client quits and broadcast a message accordingly.
- **Video Streaming**:
    - **`stream_video()`**: A function reponsible for streaming video frame by frame to the client.
- **Message structure**:
    - There are two types of messages shared between server and client, one is JSON having identifier `MESSAGE_TYPE_JSON` and another is the frame data having `MESSAGE_TYPE_FRAME`. The usual messaging between the server and client occurs through JSON. For streaming video, frame data is sent via capturing through cv2.
    - **`pack_message()`**: A function for packing messages into a struct for communication purposes


### Client Script (`210010033_client.py`)

The `210010033_client.py` script allows clients to connect to the server, send encrypted messages, request video streams, and interact with the server. Here are its main functionalities:


- **Connect to Server**: Connects to the server using the provided address and port.
- When the connection is made, the server sends its name and the public key to the server.
- Once, name and public key is sent, we start the receiving thread which shall now be responsible for receiving messages from the server.
- The main thread would be responsible for sending messages to the server.
- **Secure Communication**: Utilizes RSA encryption to send and receive encrypted messages securely. `generate_rsa_key_pair()` used for generating the public, private key pair for the client.`encrypt_string()` to encrypt the message using the public key.`decrypt_string()` to decrypt the message using the private key.
- `receive_updates_from_server()` is responsible for receiving messages from the server and call repsective functions for handling the messages depeding on the type(`MESSAGE_TYPE_JSON` or `MESSAGE_TYPE_FRAME`) and further differentiaing depending on the identifier sent in the JSON message.
- **Video Streaming**: Requests and displays video streams from the server.
- `handle_video_frame()`: Function responsible for receiving and displaying the frame data received from the server.
- `handle_json_message()`: Function responsible for handling JSON and calling respective functions on the basis of the identifier.
-`handle_buffer()`: Function responsible for handling messages(of type `MESSAGE_TYPE_JSON`) received while video streaming.
- **User Interaction**: Provides a user-friendly interface for selecting options such as messaging other clients and streaming videos.

### Folder Structure

- `210010033_server.py`: Contains the server-side implementation.
- `210010033_client.py`: Implements the client-side functionality.
- `videos/`: Directory containing video files for streaming.
-  `requirements.txt`: File containing python package list for smooth functioning of the project.

### Dependencies

- `socket`: For socket programming and network communication.
- `cv2` (OpenCV): Used for video streaming and processing.
- `struct`: For packing and unpacking data for network communication.
- `json`: Handles JSON messages for communication.
- `threading`: Implements multi-threading for concurrent operations.
- `base64`: Encodes and decodes data for secure transmission.

## To run inference

1.Creating a python environment and installing dependencies using python3
```bash
python3 -m venv cn
source cn/bin/activate
pip install -r requirements.txt
```

2.Start server
```bash
python 210010033_server.py
```

3.Start client
```bash
python 210010033_client.py
```

4.Demo provided in the video(video_link)