"""Support for the LifeSmart climate devices."""
import logging
import time
from homeassistant.components.climate import ENTITY_ID_FORMAT, ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
)

from homeassistant.const import (
    PRECISION_WHOLE,
    UnitOfTemperature,
)

from . import LifeSmartDevice

_LOGGER = logging.getLogger(__name__)
DEVICE_TYPE = "climate"

LIFESMART_STATE_LIST = [
    HVACMode.OFF,
    HVACMode.AUTO,
    HVACMode.FAN_ONLY,
    HVACMode.COOL,
    HVACMode.HEAT,
    HVACMode.DRY,
]

LIFESMART_STATE_LIST2 = [
    HVACMode.OFF,
    HVACMode.HEAT,
]

FAN_MODES = [FAN_LOW, FAN_MEDIUM, FAN_HIGH]
GET_FAN_SPEED = {FAN_LOW: 15, FAN_MEDIUM: 45, FAN_HIGH: 76}

AIR_TYPES = ["V_AIR_P"]

THER_TYPES = ["SL_CP_DN"]

LIFESMART_STATE_LIST


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up LifeSmart Climate devices."""
    if discovery_info is None:
        return
    devices = []
    dev = discovery_info.get("dev")
    param = discovery_info.get("param")
    devices = []
    if "T" not in dev["data"] and "P3" not in dev["data"]:
        return
    devices.append(LifeSmartClimateDevice(dev, "idx", "0", param))
    async_add_entities(devices)


class LifeSmartClimateDevice(LifeSmartDevice, ClimateEntity):
    """LifeSmart climate devices,include air conditioner,heater."""

    def __init__(self, dev, idx, val, param):
        """Init LifeSmart cover device."""
        super().__init__(dev, idx, val, param)
        self._name = dev["name"]
        cdata = dev["data"]
        self.entity_id = ENTITY_ID_FORMAT.format(
            (dev["devtype"] + "_" + dev["agt"][:-3] + "_" + dev["me"])
            .lower()
            .replace(":", "_")
            .replace("@", "_")
        )
        if dev["devtype"] in AIR_TYPES:
            self._modes = LIFESMART_STATE_LIST
            if cdata["O"]["type"] % 2 == 0:
                self._mode = LIFESMART_STATE_LIST[0]
            else:
                self._mode = LIFESMART_STATE_LIST[cdata["MODE"]["val"]]
            self._attributes.update(
                {"last_mode": LIFESMART_STATE_LIST[cdata["MODE"]["val"]]}
            )
            self._current_temperature = cdata["T"]["v"]
            self._target_temperature = cdata["tT"]["v"]
            self._min_temp = 10
            self._max_temp = 35
            self._fanspeed = cdata["F"]["val"]
        else:
            self._modes = LIFESMART_STATE_LIST2
            if cdata["P1"]["type"] % 2 == 0:
                self._mode = LIFESMART_STATE_LIST2[0]
            else:
                self._mode = LIFESMART_STATE_LIST2[1]
            if cdata["P2"]["type"] % 2 == 0:
                self._attributes.setdefault("Heating", "false")
            else:
                self._attributes.setdefault("Heating", "true")
            self._current_temperature = cdata["P4"]["val"] / 10
            self._target_temperature = cdata["P3"]["val"] / 10
            self._min_temp = 5
            self._max_temp = 35

    @property
    def unique_id(self):
        """A unique identifier for this entity."""
        return self.entity_id

    @property
    def precision(self):
        """Return the precision of the system."""
        return PRECISION_WHOLE

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return UnitOfTemperature.CELSIUS

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        return self._mode

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return self._modes

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 1

    @property
    def fan_mode(self):
        """Return the fan setting."""
        fanmode = None
        if self._fanspeed < 30:
            fanmode = FAN_LOW
        elif self._fanspeed < 65 and self._fanspeed >= 30:
            fanmode = FAN_MEDIUM
        elif self._fanspeed >= 65:
            fanmode = FAN_HIGH
        return fanmode

    @property
    def fan_modes(self):
        """Return the list of available fan modes."""
        return FAN_MODES

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        new_temp = int(kwargs["temperature"] * 10)
        _LOGGER.info("set_temperature: %s", str(new_temp))
        if self._devtype in AIR_TYPES:
            await super().async_lifesmart_epset(self, "0x88", new_temp, "tT")
        else:
            await super().async_lifesmart_epset(self, "0x88", new_temp, "P3")

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        await super().async_lifesmart_epset(self, "0xCE", GET_FAN_SPEED[fan_mode], "F")

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target operation mode."""
        if self._devtype in AIR_TYPES:
            if hvac_mode == HVACMode.OFF:
                await super().async_lifesmart_epset(self, "0x80", 0, "O")
                return
            if self._mode == HVACMode.OFF:
                if await super().async_lifesmart_epset(self, "0x81", 1, "O") == 0:
                    time.sleep(2)
                else:
                    return
            await super().async_lifesmart_epset(
                self, "0xCE", LIFESMART_STATE_LIST.index(hvac_mode), "MODE"
            )
        else:
            if hvac_mode == HVACMode.OFF:
                await super().async_lifesmart_epset(self, "0x80", 0, "P1")
                time.sleep(1)
                await super().async_lifesmart_epset(self, "0x80", 0, "P2")
                return
            else:
                if await super().async_lifesmart_epset(self, "0x81", 1, "P1") == 0:
                    time.sleep(2)
                else:
                    return

    @property
    def supported_features(self):
        """Return the list of supported features."""
        if self._devtype in AIR_TYPES:
            return (
                ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
            )
        else:
            return ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return self._min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return self._max_temp
