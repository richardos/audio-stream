def get_wasapi_devices(pyaudio):
    """
    Get available WASAPI devices.
    :param pyaudio: PyAudio object
    :return: a dictionary containing the device ID mapped with the device
             information
    """
    device_id = -1
    wasapi_devices = dict()
    while True:
        device_id += 1
        try:
            device_info = pyaudio.get_device_info_by_index(device_id)
            api_info = pyaudio.get_host_api_info_by_index(device_info["hostApi"])
            is_wasapi = api_info["name"].find("WASAPI") != -1
            if is_wasapi:
                wasapi_devices[device_id] = device_info
        except IOError:
            # device_id not found
            break

    return wasapi_devices


def get_output_devices(pyaudio):
    """
    Get available output devices.
    :param pyaudio: PyAudio object
    :return: a dictionary containing the device ID mapped with the device
             information
    """
    device_id = -1
    output_devices = dict()
    while True:
        device_id += 1
        try:
            device_info = pyaudio.get_device_info_by_index(device_id)
            is_output = device_info["maxOutputChannels"] > 0
            if is_output:
                output_devices[device_id] = device_info
        except IOError:
            # device_id not found
            break

    return output_devices


def print_device_dict(device_dict):
    """
    Print the given device dictionary in a user friendly way.
    :param device_dict: a dictionary containing the device ID mapped with the
                        device information
    """
    for device_id in device_dict:
        print(str(device_id) + ':', device_dict[device_id]['name'])


def handle_device_selection(selected_device_id_str, valid_devices):
    """
    Checks whether a device selection is valid based on a dictionary of valid
    devices or prompts the user for a new selection otherwise.
    :param selected_device_id_str: the selected device ID (string or None)
    :param valid_devices: valid devices in a dictionary containing the device
                          ID mapped with the device information
    :return: the final device ID selection, which is guaranteed to be valid
             (integer)
    """
    if selected_device_id_str is None:
        # no ID specified
        valid_device_selected = False
    else:
        # device ID is specified, check if valid
        selected_device_id = int(selected_device_id_str)
        if selected_device_id in valid_devices:
            valid_device_selected = True
        else:
            valid_device_selected = False
            print('Invalid device ID given (' + str(selected_device_id) + ').')

    if not valid_device_selected:
        # device ID invalid or not specified, prompt for selection
        print('Available devices:')
        print_device_dict(valid_devices)

        selected_device_id = int(input('Choose a device from the list above: '))
        while selected_device_id not in valid_devices:
            selected_device_id = int(input('Invalid device ID, please try again: '))

    return selected_device_id
