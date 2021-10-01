"""Constants for the FreeNAS integration."""
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

DOMAIN = "truenas"

ATTR_DS_AVAIL_BYTES = "Available Bytes"
ATTR_DS_COMMENTS = "Dataset Comments"
ATTR_DS_COMP_RATIO = "Compression Ratio"
ATTR_DS_NAME = "Dataset"
ATTR_DS_POOL_NAME = "Dataset Pool"
ATTR_DS_TOTAL_BYTES = "Total Bytes"
ATTR_DS_TYPE = "Dataset Type"
ATTR_DS_USED_BYTES = "Used Bytes"
ATTR_ENCRYPT = "Encrypted"
ATTR_POOL_GUID = "GUID"
ATTR_POOL_NAME = "Pool Name"

CONF_AUTH_MODE = "auth_mode"
CONF_AUTH_PASSWORD = "Username + Password"
CONF_AUTH_API_KEY = "API Key"

DEFAULT_SCAN_INTERVAL_SECONDS = 30

SERVICE_JAIL_START = "jail_start"
SCHEMA_SERVICE_JAIL_START = {}
SERVICE_JAIL_STOP = "jail_stop"
SCHEMA_SERVICE_JAIL_STOP = {
    vol.Optional("force"): cv.boolean,
}
SERVICE_JAIL_RESTART = "jail_restart"
SCHEMA_SERVICE_JAIL_RESTART = {}

SERVICE_VM_START = "vm_start"
SCHEMA_SERVICE_VM_START = {
    vol.Optional("overcommit"): cv.boolean,
}
SERVICE_VM_STOP = "vm_stop"
SCHEMA_SERVICE_VM_STOP = {
    vol.Optional("force"): cv.boolean,
}
SERVICE_VM_RESTART = "vm_restart"
SCHEMA_SERVICE_VM_RESTART = {}
