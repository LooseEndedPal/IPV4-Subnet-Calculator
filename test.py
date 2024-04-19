import socket

def is_valid_ipv4(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False


ip_address = '64.276.67.0'

if is_valid_ipv4(ip_address):
    print("Valid IPv4 address")
else:
    print("Invalid IPv4 address")