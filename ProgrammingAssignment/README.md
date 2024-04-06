## Code Overview

The project consists of two main scripts: `210010033_server.py` for the server-side implementation and `210010033_client.py` for the client-side functionality.

### Server Script (`210010033_server.py`)

The `210010033_server.py` script handles incoming client connections, manages client details, and facilitates secure communication and video streaming. Here's an overview of its key components:

- **Handle Client Connections**: Uses threading to handle multiple client connections concurrently.
- **Client Details Management**: Stores client details (names and public keys) for secure communication using RSA encryption.
- **Message Handling**: Receives and processes various types of messages, including JSON messages and video frames.
- **Video Streaming**: Streams video files to clients upon request, dividing videos into segments for efficient streaming.

### Client Script (`210010033_client.py`)

The `210010033_client.py` script allows clients to connect to the server, send encrypted messages, request video streams, and interact with the server. Here are its main functionalities:

- **Connect to Server**: Connects to the server using the provided address and port.
- **Secure Communication**: Utilizes RSA encryption to send and receive encrypted messages securely.
- **Video Streaming**: Requests and displays video streams from the server.
- **User Interaction**: Provides a user-friendly interface for selecting options such as messaging other clients and streaming videos.

### Folder Structure

- `210010033_server.py`: Contains the server-side implementation.
- `210010033_client.py`: Implements the client-side functionality.
- `videos/`: Directory containing video files for streaming.

### Dependencies

- `socket`: For socket programming and network communication.
- `cv2` (OpenCV): Used for video streaming and processing.
- `struct`: For packing and unpacking data for network communication.
- `json`: Handles JSON messages for communication.
- `threading`: Implements multi-threading for concurrent operations.
- `base64`: Encodes and decodes data for secure transmission.

## To run inference

1.Creating a python environment and installing dependencies
```bash
python3 -m venv cn
source cn/bin/activate
pip install sockets json threading opencv-python struct opencv-python-headless cryptography
```

2.Start server
```bash
python 210010033_server.py
```

3.Start client
```bash
python 210010033_client.py
```