import argparse
import socket
import sys
import time

import pyaudio
import utils


# default configuration parameters
DEFAULT_SERVER_IP = '127.0.0.1'
DEFAULT_SERVER_PORT = 9999
STREAM_FORMAT = pyaudio.paInt16
BUFFER_SIZE = 16384

srvconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def callback(in_data, frame_count, time_info, status):
    global srvconn
    srvconn.send(in_data)
    return in_data, pyaudio.paContinue


def main():
    global srvconn

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--dev-id', help='the device ID to use for '
                                                   'audio transmition',
                            default=None)
    arg_parser.add_argument('-ip', help="the server's IP address (default: "
                                        + str(DEFAULT_SERVER_IP) + ")",
                            default=DEFAULT_SERVER_IP)
    arg_parser.add_argument('-p', '--port', help="the server's port to connect "
                                                 "to (default: " + str(DEFAULT_SERVER_PORT) + ")",
                            default=DEFAULT_SERVER_PORT)
    args = arg_parser.parse_args()

    audio = pyaudio.PyAudio()

    # get all WASAPI devices
    wasapi_devices = utils.get_wasapi_devices(audio)
    if len(wasapi_devices) == 0:
        print('No WASAPI device found')
        sys.exit()

    selected_device_id = utils.handle_device_selection(args.dev_id,
                                                       wasapi_devices)
    selected_device_info = wasapi_devices[selected_device_id]
    print('You have selected:', selected_device_info)

    input('Press enter to start streaming')

    # Open stream
    channels = max(selected_device_info["maxInputChannels"],
                   selected_device_info["maxOutputChannels"])
    stream = audio.open(format=STREAM_FORMAT,
                        channels=channels,
                        rate=int(selected_device_info["defaultSampleRate"]),
                        input=True,
                        frames_per_buffer=BUFFER_SIZE,
                        input_device_index=selected_device_info["index"],
                        stream_callback=callback,
                        as_loopback=True)

    # Start stream
    try:
        print('Connecting to server...')
        srvconn.connect((args.ip, int(args.port)))
        print('Connected.')
        stream.start_stream()
        print("Started.")

        while stream.is_active():
            time.sleep(0.1)
    finally:
        # Stop stream
        stream.stop_stream()
        stream.close()
        print("Stopped.")

        # Cleanup
        srvconn.close()
        audio.terminate()


main()
