import machine
import network
import utime
from secrets import PASSWORD, SSID


class WiFiManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WiFiManager, cls).__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self):
        if not self._initialised:
            self._wlan = network.WLAN(network.STA_IF)
            self._wlan.active(True)
            self._initialised = True

    def connect(self):
        try:
            if not self._wlan.isconnected():
                print("Connecting to Wi-Fi...", end="")

                startTime = utime.time()
                maxWaitTimeInSeconds = 60

                self._wlan.connect(SSID, PASSWORD)
                while not self._wlan.isconnected():
                    if (utime.time() > (startTime + maxWaitTimeInSeconds)):
                        raise RuntimeError(
                            f"Failed to connect to Wi-Fi within {maxWaitTimeInSeconds} seconds.")
                    utime.sleep(0.5)
                    print(".", end="")
                print("\nConnected to Wi-Fi!")
            else:
                print("Already connected to Wi-Fi.")
            print("IP:", self._wlan.ifconfig()[0])
        except Exception as e:
            print(f"\nWi-Fi connection failed: {e}")
            print("Resetting WLAN interface...")
            self._wlan.disconnect()
            self._wlan.active(False)
            raise
        finally:
            # Ensure WLAN is left in a defined state
            if not self._wlan.isconnected():
                self._wlan.active(False)

    def is_connected(self):
        return self._wlan.isconnected()

    def get_ip(self):
        return self._wlan.ifconfig()[0] if self._wlan.isconnected() else None
