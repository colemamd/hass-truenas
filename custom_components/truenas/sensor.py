from typing import Any, Callable, List, Mapping, Optional

from aiotruenas_client import CachingMachine as Machine
from aiotruenas_client.dataset import Dataset
from aiotruenas_client.disk import Disk, DiskType
from aiotruenas_client.pool import Pool
from homeassistant.components.sensor import DEVICE_CLASS_TEMPERATURE
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import slugify

from . import TrueNASDatasetEntity, TrueNASDiskEntity, TrueNASPoolEntity, TrueNASSensor
from .const import (
    ATTR_DS_AVAIL_BYTES,
    ATTR_DS_COMMENTS,
    ATTR_DS_COMP_RATIO,
    ATTR_DS_NAME,
    ATTR_DS_POOL_NAME,
    ATTR_DS_TOTAL_BYTES,
    ATTR_DS_TYPE,
    ATTR_DS_USED_BYTES,
    ATTR_POOL_GUID,
    ATTR_POOL_NAME,
    DOMAIN,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable,
):
    """Set up the TrueNAS switches."""
    entities = _create_entities(hass, entry)
    async_add_entities(entities)


def _get_machine(hass: HomeAssistant, entry: ConfigEntry) -> Machine:
    machine = hass.data[DOMAIN][entry.entry_id]["machine"]
    assert machine is not None
    return machine


def _create_entities(hass: HomeAssistant, entry: ConfigEntry) -> List[Entity]:
    entities = []

    machine = _get_machine(hass, entry)
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    name = entry.data[CONF_NAME]

    for disk in machine.disks:
        entities.append(DiskTemperatureSensor(entry, name, disk, coordinator))

    for pool in machine.pools:
        entities.append(PoolSensor(entry, name, pool, coordinator))

    for dataset in machine.datasets:
        entities.append(DatasetSensor(entry, name, dataset, coordinator))

    return entities


class DatasetSensor(TrueNASDatasetEntity, TrueNASSensor, Entity):
    _dataset: Dataset

    def __init__(
        self,
        entry: ConfigEntry,
        name: str,
        dataset: Dataset,
        coordinator: DataUpdateCoordinator,
    ) -> None:
        self._dataset = dataset
        super().__init__(entry, name, coordinator)

    @property
    def name(self) -> str:
        """Return the name of the dataset."""
        return f"{self._dataset.pool_name + self._dataset.id} Dataset"

    @property
    def unique_id(self):
        """Return the Unique ID of the dataset."""
        return slugify(self._dataset.id)

    @property
    def extra_state_attributes(self):
        """Return extra Pool attributes"""
        assert self._dataset is not None
        value = self._get_comments()
        return {
            ATTR_DS_NAME: f"{self._dataset.id}",
            ATTR_DS_POOL_NAME: f"{self._dataset.pool_name}",
            ATTR_DS_COMMENTS: f"{value}",
            ATTR_DS_TYPE: f"{self._dataset.type.name}",
            ATTR_DS_COMP_RATIO: f"{self._dataset.compression_ratio}",
            ATTR_DS_AVAIL_BYTES: f"{self._dataset.available_bytes}",
            ATTR_DS_USED_BYTES: f"{self._dataset.used_bytes}",
            ATTR_DS_TOTAL_BYTES: f"{self._dataset.total_bytes}",
        }

    @property
    def icon(self):
        """Return an icon for the dataset."""
        return "mdi:file-cabinet"

    def _get_state(self):
        """Returns the status of the dataset."""
        return self.available


class DiskTemperatureSensor(TrueNASDiskEntity, TrueNASSensor, Entity):
    _disk: Disk

    def __init__(
        self,
        entry: ConfigEntry,
        name: str,
        disk: Disk,
        coordinator: DataUpdateCoordinator,
    ) -> None:
        self._disk = disk
        super().__init__(entry, name, coordinator)

    @property
    def name(self) -> str:
        """Return the name of the disk."""
        assert self._disk is not None
        return f"Disk {self._disk.serial} Temperature"

    @property
    def unique_id(self) -> str:
        assert self._disk is not None
        return slugify(
            f"{self._entry.unique_id}-{self._disk.serial}_temperature_sensor",
        )

    @property
    def icon(self) -> str:
        """Return an icon for the disk."""
        return "mdi:thermometer"

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_TEMPERATURE

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    def _get_state(self) -> Optional[int]:
        """Returns the current temperature of the disk."""
        if self.available:
            return self._disk.temperature
        return None


class PoolSensor(TrueNASPoolEntity, TrueNASSensor, Entity):
    _pool: Pool

    def __init__(
        self,
        entry: ConfigEntry,
        name: str,
        pool: Pool,
        coordinator: DataUpdateCoordinator,
    ) -> None:
        self._pool = pool
        super().__init__(entry, name, coordinator)

    @property
    def name(self) -> str:
        """Return the name of the pool."""
        return f"{self._pool.name} Pool"

    @property
    def unique_id(self):
        """Return the Unique ID of the pool."""
        return slugify(self._pool.guid)

    @property
    def extra_state_attributes(self):
        """Return extra Pool attributes"""
        assert self._pool is not None
        return {
            ATTR_POOL_NAME: f"{self._pool.name}",
            ATTR_POOL_GUID: f"{self._pool.guid}",
        }

    @property
    def icon(self):
        """Return an icon for the pool."""
        return "mdi:database"

    def _get_state(self):
        """Returns the current state of the pool."""
        if not isinstance:
            return None
        return self._pool.status.name
