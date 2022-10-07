import sensor
import threading
from flask import Flask, Response
from app_config import app_config

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    return Response(render(), mimetype="text/plain")


def render():
    sensor_config = app_config()["sensor"]

    template = """
mi_temperature{{mac="{mac}", name="{name}"}} {temperature}
mi_humidity{{mac="{mac}", name="{name}"}} {humidity}
mi_battery_voltage{{mac="{mac}", name="{name}"}} {battery_voltage}
mi_battery_percent{{mac="{mac}", name="{name}"}} {battery_percent}
mi_rssi{{mac="{mac}", name="{name}"}} {rssi}
"""

    metrics_str = """mitemperature2_exporter{version="1.0.0"} 1\n"""
    data = sensor.metrics()

    for mac in data.keys():
        name = sensor_config["humanize"].get(mac, mac)

        _, temperature, humidity, batteryVoltage, batteryPercent, rssi = data[mac][0]
        metrics_str += template.format(
            mac=mac,
            temperature=temperature,
            humidity=humidity,
            battery_voltage=batteryVoltage,
            battery_percent=batteryPercent,
            rssi=rssi,
            name=name,
        )
    return metrics_str


if __name__ == "__main__":
    config = app_config()

    debug = True if config["app"]["debug"] else False
    host = config["app"]["host"]
    port = config["app"]["port"]

    sensor_monitor = threading.Thread(target=sensor.start, args=(debug,))
    sensor_monitor.start()
    app.run(host=host, port=port, debug=debug)
