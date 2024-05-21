from qtpy import QtCore


ITEM_ID_ROLE = QtCore.Qt.UserRole + 1
ITEM_IS_GROUP_ROLE = QtCore.Qt.UserRole + 2
ITEM_LABEL_ROLE = QtCore.Qt.UserRole + 3
ITEM_WARNED_ROLE = QtCore.Qt.UserRole + 4
ITEM_ERRORED_ROLE = QtCore.Qt.UserRole + 5
PLUGIN_SKIPPED_ROLE = QtCore.Qt.UserRole + 6
PLUGIN_PASSED_ROLE = QtCore.Qt.UserRole + 7
INSTANCE_REMOVED_ROLE = QtCore.Qt.UserRole + 8
PLUGIN_ACTIONS_ROLE = QtCore.Qt.UserRole + 9

__all__ = (
    "ITEM_ID_ROLE",
    "ITEM_IS_GROUP_ROLE",
    "ITEM_LABEL_ROLE",
    "ITEM_WARNED_ROLE",
    "ITEM_ERRORED_ROLE",
    "PLUGIN_SKIPPED_ROLE",
    "PLUGIN_PASSED_ROLE",
    "INSTANCE_REMOVED_ROLE",
    "PLUGIN_ACTIONS_ROLE"
)
