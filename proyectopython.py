import serial
import time

class ArduinoController:
    def _init_(self, port, baud_rate):
        self.arduino = serial.Serial(port, baud_rate)
        time.sleep(2)  # Esperar a que se establezca la conexión

    def enviar_comando(self, comando):
        self.arduino.write(comando.encode())

arduino = ArduinoController('COMX', 9600)  # Reemplaza 'COMX' con el puerto serie adecuado

while True:
    opcion = input("Ingrese el comando (1: Incrementar servo 1, 2: Decrementar servo 1, 3: Incrementar servo 2, 4: Decrementar servo 2): ")
    if opcion in ['1', '2', '3', '4']:
        arduino.enviar_comando(opcion)
    else:
        print("Comando inválido. Por favor, ingrese 1, 2, 3 o 4.")