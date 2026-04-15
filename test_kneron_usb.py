"""
本機測試：是否偵測到 Kneron USB（常見 VID 0x0D7D）。
請插上 KL520 後在專案根目錄執行: py test_kneron_usb.py
需: pip install pyusb libusb-package
"""
from __future__ import annotations

import subprocess
import sys


def print_pnp_kneron() -> None:
    ps = r"""
Get-PnpDevice -PresentOnly |
  Where-Object { $_.InstanceId -match 'VID_0[Dd]7[Dd]' } |
  Format-Table Status, Class, FriendlyName, InstanceId -AutoSize
"""
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True,
            text=True,
            timeout=30,
        )
        out = (r.stdout or "").strip()
        print("[PnP VID_0D7D]")
        print(out if out else "(無符合項目)")
    except Exception as e:
        print("[PnP] 無法執行:", e)


def print_pyusb() -> None:
    try:
        import usb.backend.libusb1 as usb_be
        import usb.core
        import libusb_package
    except ImportError as e:
        print("[pyusb] 缺少套件:", e)
        print("請執行: py -m pip install pyusb libusb-package")
        sys.exit(1)

    backend = usb_be.get_backend(find_library=libusb_package.find_library)
    print("[pyusb] backend:", backend)
    if backend is None:
        print("[pyusb] 無 libusb 後端。請確認已: py -m pip install libusb-package")
        sys.exit(1)

    vid = 0x0D7D
    dev = usb.core.find(idVendor=vid, backend=backend)
    if dev is None:
        print(f"[pyusb] 找不到 idVendor=0x{vid:04X} 的裝置。")
        print("        請確認板子已上電、USB 已插好、Zadig 已對「正確介面」安裝 WinUSB。")
        return

    print(f"[pyusb] 找到裝置: {dev}")
    try:
        print("         manufacturer:", usb.util.get_string(dev, dev.iManufacturer))
        print("         product:", usb.util.get_string(dev, dev.iProduct))
    except Exception as e:
        print("         (讀字串失敗, 可忽略):", e)


def main() -> None:
    print("=== Kneron USB 本機測試 ===\n")
    print_pnp_kneron()
    print()
    print_pyusb()
    print("\n=== 結束 ===")


if __name__ == "__main__":
    main()
