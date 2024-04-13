## Computer Networks Programming Assignment

- This Python application is a basic video chat system that utilizes sockets for client-server communication. It ensures secure transmission through RSA encryption for messages. Users can exchange text messages and request video streaming from the server, with video frames being transmitted over the network. The users are also notified of other user joining or leaving the server.

- The project consists of two main scripts: `210010033_server.py` for the server-side implementation and `210010033_client.py` for the client-side functionality.

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
    - There are two types of messages shared between server and client, one is JSON having identifier `MESSAGE_TYPE_JSON` through which the usual messaging between the server and client occurs; and another is the frame data having `MESSAGE_TYPE_FRAME` throught which video streaming occurs. Frame data is obtained via capturing through cv2.
    - **`pack_message()`**: A function for packing messages into a struct for communication purposes depending on their type accordingly.
- **Note**: Server runs on `localhost`, `port 10000`


### Client Script (`210010033_client.py`)

The `210010033_client.py` script allows clients to connect to the server, send encrypted messages, request video streams, and interact with the server. Here are its main functionalities:

- **User Interaction**: Provides a user-friendly interface for selecting options such as messaging other clients, streaming video and leaving the server.
- **Connect to Server**: Connects to the server using the provided address and port.
- **Secure Communication**: Utilizes RSA encryption to send and receive encrypted messages securely. 
    - `generate_rsa_key_pair()`: used for generating the public, private key pair for the client.
    - `encrypt_string()`: to encrypt the message using the public key.
    - `decrypt_string()`: to decrypt the message using the private key.
    - When the connection is made, the server sends its name and the public key to the server.
    - Once, name and public key is sent, we start the receiving thread which shall now be responsible for receiving messages from the server.
- **Receiving Updates**:
    - `receive_updates_from_server()` is responsible for receiving messages from the server and call respective functions for handling the messages depeding on the type(`MESSAGE_TYPE_JSON` or `MESSAGE_TYPE_FRAME`) and further differentiaing depending on the identifier sent in the JSON message.
    - `handle_json_message()`: Function responsible for handling JSON and calling respective functions on the basis of the identifier.
    - `handle_buffer()`: Function responsible for handling messages(of type `MESSAGE_TYPE_JSON`) received while video streaming.
- **Video Streaming**: Requests and displays video streams from the server.
    - `handle_video_frame()`: Function responsible for receiving and displaying the video frame received from the server.


### Folder/File Structure

- `210010033_server.py`: Contains the server-side implementation.
- `210010033_client.py`: Implements the client-side functionality.
- `videos/`: Directory containing video files for streaming in the same directory as `210010033_server.py` and `210010033_client.py`.

### Dependencies

- `sockets`: For socket programming and network communication.
- `opencv-python` (OpenCV): Used for video streaming and processing.
- `struct`: For packing and unpacking data for network communication.
- `json`: Handles JSON messages for communication.
- `threading`: Implements multi-threading for concurrent operations.
- `base64`: Encodes and decodes data for secure transmission.
- `cryptography`: Essential for secure communication by providing tools for encryption, decryption, key generation, and digital signatures.

### To run inference

#### Creating a python environment and installing dependencies using python3
```bash
python3 -m venv cn
source cn/bin/activate
pip install bson==0.5.10 cffi==1.16.0 cryptography==42.0.5 dnspython==2.6.1 numpy==1.26.4 opencv-python==4.9.0.80 opencv-python-headless==4.9.0.80 psutil==5.9.8 pycparser==2.22 pycryptodome==3.20.0 pymongo==4.6.3 python-dateutil==2.9.0.post0 setuptools==68.2.2 six==1.16.0 sockets==1.0.0
```

#### Download `210010033_server.py` and `210010033_client.py` in the same directory where the virtual environment(activated) is present

#### Start server
```bash
python 210010033_server.py
```

#### Start client
```bash
python 210010033_client.py
```

#### Enter a name when prompted on the client side.

#### Follow the options provided to send messages, request video streaming or quit depending on choice.

#### Note:
- Ensure that the server is running before starting any client connections.
- Video files should be placed in the videos/ directory on the server side and each file name _should_ have all the three required qualities present with `<video_name>_<quality>.mp4` where `quality` can take the values 240p, 720p and 1440p.

### Demo Video
[Click here](https://drive.google.com/file/d/1nXJAHAFTE8iFEYO_nRaVGMvDGlVhdOZK/view?usp=sharing)