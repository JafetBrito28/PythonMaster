import socket

def scan_ports(target, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  #Timeout de medio segundo para evitar bloqueos
                result = s.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    service_name = socket.getservbyport(port)
                    print(f"Puerto {port} abierto ({service_name})")
        except socket.gaierror:
            print(f"Error: No se pudo resolver el host '{target}'")
            return
        except:
            pass  # Ignora otros errores (por ejemplo, si el puerto está bloqueado)

    if not open_ports:
        print(f"No se encontraron puertos abiertos en {target} entre {start_port} y {end_port}")
    return open_ports

# Ejemplo de uso:
target = "www.example.com"  # Reemplaza con el host que quieras escanear
start_port = 1
end_port = 100
open_ports = scan_ports(target, start_port, end_port)

print("Puertos abiertos encontrados:", open_ports)  # Muestra los puertos abiertos en una lista
