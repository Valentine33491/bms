#------------------------------------------------------------------------------
# программа выполняет сканирование устройства Bluetooth на наличие 
# платы Jikong BMS.
#------------------------------------------------------------------------------
# системные библиотеки 
import asyncio
import time
#------------------------------------------------------------------------------
# импортируем библиотеки для работы с Bluetooth
from bleak import BleakScanner
from bleak.exc import BleakBluetoothNotAvailableError  # Важно!
#------------------------------------------------------------------------------
# импортируем пользовательские библиотеки
from utils.ansi_cmd import print_ok_box, print_err_box, print_warn_box
#------------------------------------------------------------------------------
# Используем UUID сервиса JK BMS для фильтрации
JK_BMS_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
#------------------------------------------------------------------------------
async def wait_for_bluetooth(timeout=None):
    """
    Ждет, пока Bluetooth не станет доступен.
    Args:
        timeout: максимальное время ожидания в секундах (None = бесконечно)
    Returns:
        True, если Bluetooth стал доступен
    Raises:
        TimeoutError: если истекло время ожидания
    """
    start_time = time.time()
    attempt = 1
    
    print("[      ] Проверяем доступность Bluetooth", end = '\r')
    
    while True:
        try:
            # пробуем начать сканирование - если Bluetooth выключен,
            # будет возвращено BleakBluetoothNotAvailableError
            async with BleakScanner() as scanner:
                await scanner.discover(timeout=1.0)
            # здесь начинается код если bluetooth работает
            print('\r', end = '')
            print_ok_box("Проверяем доступность Bluetooth")
            return True
        except BleakBluetoothNotAvailableError as e:
            # Bluetooth выключен или недоступен
            print("\nПожалуйста, включите Bluetooth на вашем компьютере!", end = '\x1b[A')
            # проверяем таймаут (чтобы навечно не зациклиться)
            if timeout and (time.time() - start_time) > timeout:
                print('\r', end = '')
                print_err_box(f"Проверяем доступность Bluetooth")
                print("", end = '\n')
                raise TimeoutError("Время ожидания включения Bluetooth истекло")
            # 3 секунды ожидания перед следующей попыткой
            await asyncio.sleep(3)
            attempt += 1
        except Exception as e:
            # иные ошибки (например, нет адаптера вообще)
            print(f"Неожиданная ошибка: {e}")
            raise
#------------------------------------------------------------------------------
async def scan_for_bms_with_check():
    """
    Сканирует BMS с предварительной проверкой Bluetooth.
    """
    try:
        # проверка включен ли Bluetooth
        await wait_for_bluetooth(timeout=1)
        # ищем среди устройств Bluetooth нашу плату BMS
        print("\nСканирование JK BMS...")
        devices = await BleakScanner.discover(timeout=10.0, return_adv=True)
        found_bms = []
        for device, adv_data in devices.values():
            device_name = device.name or "Unknown"
            # проверяем имя и UUID сервиса
            has_jk_service = False
            if adv_data.service_uuids:
                if JK_BMS_SERVICE_UUID.lower() in [uuid.lower() for uuid in adv_data.service_uuids]:
                    has_jk_service = True
            
            if device_name.startswith("JK-") or has_jk_service:
                found_bms.append({
                    "name": device_name,
                    "address": device.address,
                    "rssi": adv_data.rssi
                })
                print_ok_box(f"BMS найдена: {device_name} [{device.address}] (сигнал: {adv_data.rssi} dBm)")
        if not found_bms:
            print_err_box("Устройства JK BMS не найдены в радиусе действия")
        return found_bms
    except BleakBluetoothNotAvailableError:
        print_err_box("Bluetooth не доступен. Пожалуйста, проверьте наличие адаптера и включите его.")
        return []
    except TimeoutError:
        print_err_box("Время ожидания включения Bluetooth истекло.")
        return []
    except KeyboardInterrupt:
        print_warn_box("Сканирование прервано пользователем.")
        return []
#------------------------------------------------------------------------------
if __name__ == "__main__":
    # выполним сканирование сети на наличие платы BMS
    asyncio.run(scan_for_bms_with_check())