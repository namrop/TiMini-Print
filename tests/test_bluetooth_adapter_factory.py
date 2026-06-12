from __future__ import annotations

import importlib
import unittest
from unittest.mock import patch

from timiniprint.transport.bluetooth.adapters.adapter_fallback import _FallbackAdapter
from timiniprint.transport.bluetooth.adapters.bleak_adapter import _BleakBleAdapter
from timiniprint.transport.bluetooth.adapters.linux_att import _LinuxAttAdapter

from tests.helpers import reset_adapter_cache


class BluetoothAdapterFactoryTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_adapter_cache()
        self.adapters = importlib.import_module("timiniprint.transport.bluetooth.adapters.__init__")

    def test_get_classic_adapter_platform_selection(self) -> None:
        with patch.object(self.adapters, "IS_WINDOWS", True), patch.object(self.adapters, "IS_LINUX", False), patch.object(
            self.adapters, "IS_MACOS", False
        ):
            a1 = self.adapters._get_classic_adapter()
            a2 = self.adapters._get_classic_adapter()
            self.assertIs(a1, a2)

    def test_get_ble_adapter_cached(self) -> None:
        with patch.dict("os.environ", {}, clear=True), patch.object(self.adapters, "IS_WINDOWS", False), patch.object(
            self.adapters, "IS_LINUX", True
        ), patch.object(self.adapters, "IS_MACOS", False):
            b1 = self.adapters._get_ble_adapter()
            b2 = self.adapters._get_ble_adapter()
            self.assertIs(b1, b2)
            self.assertIsInstance(b1, _FallbackAdapter)

    def test_linux_ble_backend_env_can_force_bleak(self) -> None:
        with patch.dict("os.environ", {"TIMINIPRINT_BLE_BACKEND": "bleak"}, clear=True), patch.object(
            self.adapters, "IS_WINDOWS", False
        ), patch.object(self.adapters, "IS_LINUX", True), patch.object(self.adapters, "IS_MACOS", False):
            adapter = self.adapters._get_ble_adapter()

        self.assertIsInstance(adapter, _BleakBleAdapter)

    def test_linux_ble_backend_env_can_force_direct_att(self) -> None:
        with patch.dict("os.environ", {"TIMINIPRINT_BLE_BACKEND": "linux-att"}, clear=True), patch.object(
            self.adapters, "IS_WINDOWS", False
        ), patch.object(self.adapters, "IS_LINUX", True), patch.object(self.adapters, "IS_MACOS", False):
            adapter = self.adapters._get_ble_adapter()

        self.assertIsInstance(adapter, _LinuxAttAdapter)


if __name__ == "__main__":
    unittest.main()
