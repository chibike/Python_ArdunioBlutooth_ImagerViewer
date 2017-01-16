import serial.tools.list_ports
p = list(serial.tools.list_ports.comports())
ports = [f[0] for f in p]
print(ports)
