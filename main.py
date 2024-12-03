import bluetooth
from machine import Pin
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)


class BLE():
    def __init__(self, name):
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)  # Upewnij się, że BLE jest aktywne
        self.connHandle = None
        self.connected = False
        self.led = Pin(8, Pin.OUT)  # Pin GPIO 8, dioda
        self.led.on()  # Ustaw stan wysoki (wyłącz diodę na starcie)
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertise()

        # Ustawienia BLE
        self.ble.config(mtu=247)  # Zwiększenie rozmiaru MTU

    def ble_irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            self.connHandle = data[0]
            self.connected = True
            print("Połączono z urządzeniem centralnym.")

        elif event == _IRQ_CENTRAL_DISCONNECT:
            self.connHandle = None
            self.connected = False
            print("Rozłączono. Reklamowanie ponownie uruchomione.")
            self.advertise()

        elif event == _IRQ_GATTS_WRITE:
            if data:
                buffer = self.ble.gatts_read(self.rx)
                message = buffer.decode('UTF-8').strip()
                print(f"Otrzymano komendę: {message}")
                self.process_command(message)
            else:
                print("Brak danych w komendzie.")

    def process_command(self, command):
        command = command.lower()  # Zmiana na małe litery
        if command == "on":
            self.led.off()  # Włącz diodę
            print("Dioda włączona.")
        elif command == "off":
            self.led.on()  # Wyłącz diodę
            print("Dioda wyłączona.")
        else:
            print("Nieznana komenda.")

    def register(self):
        # UUID Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        BLE_NUS = bluetooth.UUID(NUS_UUID)
        BLE_RX = (bluetooth.UUID(RX_UUID), bluetooth.FLAG_WRITE)
        BLE_TX = (bluetooth.UUID(TX_UUID), bluetooth.FLAG_NOTIFY)

        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)

        try:
            ((self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)
        except Exception as e:
            print(f"Błąd rejestracji usług: {e}")

    def advertise(self):
        name = bytes(self.name, 'UTF-8')
        # Reklamowanie z flagą '0x06' (general discoverable)
        self.ble.gap_advertise(
            100,
            bytearray(b'\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name
        )


ble = BLE("ESP32 LED")

