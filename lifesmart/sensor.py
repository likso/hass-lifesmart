"""Support for lifesmart sensors."""
import logging


from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfPower,
    UnitOfEnergy,
    CONCENTRATION_PARTS_PER_MILLION,
    CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER,
    LIGHT_LUX,
)

DOMAIN = "sensor"
ENTITY_ID_FORMAT = DOMAIN + ".{}"

from . import LifeSmartDevice

_LOGGER = logging.getLogger(__name__)

GAS_SENSOR_TYPES = ["SL_SC_WA ", "SL_SC_CH", "SL_SC_CP", "ELIQ_EM"]

OT_SENSOR_TYPES = ["SL_SC_MHW", "SL_SC_BM", "SL_SC_G", "SL_SC_BG"]


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Perform the setup for LifeSmart devices."""
    devices = []
    dev = discovery_info.get("dev")
    param = discovery_info.get("param")
    devices = []
    for idx in dev["data"]:
        if dev["devtype"] in OT_SENSOR_TYPES and idx in ["Z", "V", "P3", "P4"]:
            devices.append(LifeSmartSensor(dev, idx, dev["data"][idx], param))
        elif dev['devtype'] in GAS_SENSOR_TYPES:
            devices.append(LifeSmartSensor(dev, idx, dev["data"][idx], param))
    async_add_entities(devices)


class LifeSmartSensor(LifeSmartDevice):
    """Representation of a LifeSmartSensor."""

    def __init__(self, dev, idx, val, param):
        """Initialize the LifeSmartSensor."""
        super().__init__(dev, idx, val, param)
        self.entity_id = ENTITY_ID_FORMAT.format(
            (
                dev["devtype"] + "_" + dev["agt"][:-3] + "_" + dev["me"] + "_" + idx
            ).lower()
        )
        devtype = dev["devtype"]
        if devtype in GAS_SENSOR_TYPES:
            self._unit = "None"
            self._device_class = "None"
            self._state = val["val"]
        else:
            if idx == "T" or idx == "P1":
                self._device_class = "temperature"
                self._unit = UnitOfTemperature.CELSIUS
            elif idx == "H" or idx == "P2":
                self._device_class = "humidity"
                self._unit = "%"
            elif idx == "Z":
                self._device_class = "illuminance"
                self._unit = "lx"
            elif idx == "V":
                self._device_class = "battery"
                self._unit = "%"
            elif idx == "P3":
                self._device_class = "None"
                self._unit = "ppm"
            elif idx == "P4":
                self._device_class = "None"
                self._unit = "mg/m3"
            else:
                self._unit = "None"
                self._device_class = "None"
            self._state = val["v"]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    @property
    def device_class(self):
        """Return the device class of this entity."""
        return self._device_class

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """A unique identifier for this entity."""
        return self.entity_id
