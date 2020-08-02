import argparse
import socket
import sys

import pyaudio
import utils


# default configuration parameters
DEFAULT_SERVER_PORT = 9999
STREAM_FORMAT = pyaudio.paInt16
BUFFER_SIZE = 65536


def run_socket_connection(port, audio_stream):
    while True:
        try:
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.bind(('', int(port)))
            serversocket.listen(5)

            print('Waiting for client connection...')
            transmitter, addr = serversocket.accept()
            print('Client connected.')

            while True:
                data = transmitter.recv(BUFFER_SIZE)
                audio_stream.write(data)

        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(str(e))
        finally:
            serversocket.close()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--dev-id', help='the device ID to use for '
                                                   'audio playback',
                            default=None)
    arg_parser.add_argument('-p', '--port', help='the socket port to bind to '
                                                 '(default:' + str(DEFAULT_SERVER_PORT) + ')',
                            default=DEFAULT_SERVER_PORT)
    args = arg_parser.parse_args()

    audio = pyaudio.PyAudio()

    # get all output devices
    output_devices = utils.get_output_devices(audio)
    if len(output_devices) == 0:
        print('No output device found')
        sys.exit()

    selected_device_id = utils.handle_device_selection(args.dev_id,
                                                       output_devices)
    selected_device_info = output_devices[selected_device_id]
    print('You have selected:', selected_device_info)

    channels = max(selected_device_info["maxInputChannels"],
                   selected_device_info["maxOutputChannels"])

    try:
        stream = audio.open(format=STREAM_FORMAT,
                            channels=channels,
                            rate=int(selected_device_info["defaultSampleRate"]),
                            output=True,
                            frames_per_buffer=BUFFER_SIZE,
                            output_device_index=selected_device_id)

        run_socket_connection(args.port, stream)

    finally:
        print('Shutting down')
        stream.close()
        audio.terminate()


main()
