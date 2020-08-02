# Python audio streaming

A simple client-server setup for streaming audio across devices over TCP sockets using Python.

## Requirements
### transmitter
- [PyAudio fork][1] with loopback option (for transmitter)

### receiver
- [PyAudio][2]

The implementation was tested on a Raspberry Pi and a Windows 8.1 PC over Wi-Fi connection:
- Raspberry Pi (receiver/socket server) 
    - Rasbian 9
    - Python 3.5
    - PyAudio installed via package manager (`apt-get install python3-pyaudio`)
- Windows 8.1 (transmitter/socket client)
    - Python 3.6
    - PyAudio 0.2.11 prebuilt for win 64 (downloaded from [here][3]) 

## Usage
**Note:** Both transmitter and receiver scripts require the `utils.py` module.
### transmitter
```
transmitter_win.py [-h] [-d DEV_ID] [-ip IP] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -d DEV_ID, --dev-id DEV_ID
                        the device ID to use for audio transmition
  -ip IP                the server's IP address (default: 127.0.0.1)
  -p PORT, --port PORT  the server's port to connect to (default: 9999)
```

### receiver
```
usage: receiver.py [-h] [-d DEV_ID] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -d DEV_ID, --dev-id DEV_ID
                        the device ID to use for audio playback
  -p PORT, --port PORT  the socket port to bind to (default:9999)
```

[1]: https://github.com/intxcc/pyaudio_portaudio
[2]: https://pypi.org/project/PyAudio/
[3]: https://github.com/intxcc/pyaudio_portaudio/releases
