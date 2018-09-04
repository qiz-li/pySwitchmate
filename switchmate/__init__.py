"""Library to handle connection with Switchmate"""

import bluepy

class Switchmate:
    """Representation of a Switchmate."""

    def __init__(self, mac) -> None:
        sel.mac = mac
        self._device = None
        self._connect()

    def _connect(self) -> bool:
        if self._device:
            try:
                self._device.disconnect()
            except bluepy.btle.BTLEException:
                pass
        try:
            self._device = bluepy.btle.Peripheral(self._mac,
                                                  bluepy.btle.ADDR_TYPE_RANDOM)
        except bluepy.btle.BTLEException:
            _LOGGER.error("Failed to connect to switchmate")
            return False
        return True

    def _sendpacket(self, key, retry=2) -> bool:
        try:
            self._device.writeCharacteristic(HANDLE, key, True)
        except bluepy.btle.BTLEException:
            _LOGGER.error("Cannot connect to switchmate. Retrying")
            if retry < 1:
                return False
            if not self._connect():
                return False
            self._sendpacket(key, retry-1)
        return True
      
    def update(self) -> None:
        """Synchronize state with switch."""
        import bluepy
        try:
           return self._device.readCharacteristic(HANDLE) == ON_KEY
        except bluepy.btle.BTLEException:
            self._connect()

    def turn_on(self) -> None:
        """Turn the switch on."""
        self._sendpacket(ON_KEY)

    def turn_off(self) -> None:
        """Turn the switch off."""
        self._sendpacket(OFF_KEY)
