# -*- coding: utf-8 -*-

import bluetooth._bluetooth as bluez

from collections import deque
from bluetooth_utils import (
    toggle_device,
    enable_le_scan,
    parse_le_advertising_events,
    disable_le_scan,
    raw_packet_to_str,
)

from logger import get_logger

MAX_LENTH = 10
RESULT = dict()
SOCK = 0

logger = get_logger()


def push_metric(mac, temperature, humidity, batteryVoltage, batteryPercent, rssi):
    logger.info(
        "mac:{} temperature:{} humidity:{} batteryVoltage:{} batteryPercent:{} rssi:{} ".format(
            mac, temperature, humidity, batteryVoltage, batteryPercent, rssi
        )
    )

    if mac not in RESULT:
        RESULT[mac] = deque(maxlen=MAX_LENTH)

    RESULT[mac].appendleft(
        [mac, temperature, humidity, batteryVoltage, batteryPercent, rssi]
    )


def metrics():
    return RESULT


def handler(mac, adv_type, data, rssi):
    data_str = raw_packet_to_str(data)
    preeamble = "161a18"
    packetStart = data_str.find(preeamble)
    offset = packetStart + len(preeamble)
    strippedData_str = data_str[
        offset : offset + 26
    ]  # if shorter will just be shorter then 13 Bytes
    strippedData_str = data_str[
        offset:
    ]  # if shorter will just be shorter then 13 Bytes

    # Check for ATC preamble
    if data_str[6:10] == "1a18":
        temperature = (
            int.from_bytes(
                bytearray.fromhex(strippedData_str[12:16]),
                byteorder="little",
                signed=True,
            )
            / 100.0
        )
        humidity = (
            int.from_bytes(
                bytearray.fromhex(strippedData_str[16:20]),
                byteorder="little",
                signed=False,
            )
            / 100.0
        )
        batteryVoltage = (
            int.from_bytes(
                bytearray.fromhex(strippedData_str[20:24]),
                byteorder="little",
                signed=False,
            )
            / 1000.0
        )
        batteryPercent = int.from_bytes(
            bytearray.fromhex(strippedData_str[24:26]), byteorder="little", signed=False
        )

        push_metric(mac, temperature, humidity, batteryVoltage, batteryPercent, rssi)


def start(debug=False):
    # https://github.com/JsBergbau/MiTemperature2/blob/master/LYWSD03MMC.py#L614
    dev_id = 0
    toggle_device(dev_id, True)
    SOCK = bluez.hci_open_dev(dev_id)

    # Set filter to "True" to see only one packet per device
    enable_le_scan(SOCK, filter_duplicates=False)

    try:
        # Called on new LE packet
        parse_le_advertising_events(SOCK, handler=handler, debug=debug)
    # Scan until Ctrl-C
    except KeyboardInterrupt:
        disable_le_scan(SOCK)


def stop():
    disable_le_scan(SOCK)
