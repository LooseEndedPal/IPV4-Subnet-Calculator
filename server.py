import socket
import json

def ipv4Class(number):
    if 1 <= number <= 126:
        return 'A'
    elif 128 <= number <= 191:
        return 'B'
    elif 192 <= number <= 223:
        return 'C'
    else:
        return 'invalid'


def subnet(netClass, prefix):
    octets = 0
    octetRemains = 0
    mask = []
    if netClass == 'A':
        octets = 1
        octetRemains = 3
    elif netClass == 'B':
        octets = 2
        octetRemains = 2
    elif netClass == 'C':
        octets = 3
        octetRemains = 1
    else:
        return 'invalid'
    
    for x in range(octets):
        mask.append('255')
    
    bitRemains = prefix % 8
    
    if bitRemains == 0:
        for x in range(octetRemains):
            mask.append('0')
    else:
        octetvalue = 0
        for x in range(bitRemains):
            octetvalue += 2 ** (7 - x)   
        
        mask.append(str(octetvalue))
        octetRemains -= 1
        if octetRemains > 0:
            for x in range(octetRemains):
                mask.append('0')
    return '.'.join(mask)

def server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_address = ('localhost', 5000)
            sock.bind(server_address)
            sock.listen(5)
            print('Server listening')
            client, address = sock.accept()
            data = client.recv(2048).decode()
            
            print(data)
            
            if not data:
                break
            
            ipv4, prefix = data.split('\n')
            prefix = int(prefix)
            address = ipv4.split('.')
            numSubnets = 2 ** (prefix % 8)
            numHosts = 2 ** (32 - prefix)
            validHosts = 2 ** (32 - prefix) - 2
            netClass = ipv4Class(int(address[0]))
            
            mask = subnet(netClass, prefix)
            networkAddress = '.'.join(address[:3]) + '.0'
            firstAddress = '.'.join(address[:3]) + '.1'
            lastAddress = '.'.join(address[:3]) + '.' +str(validHosts)
            broadcastAddress = '.'.join(address[:3]) + '.' + str(validHosts + 1)

            data = {
                    'IPV4_Address': '.'.join(address), 
                    'Prefix': prefix,
                    'Class': netClass, 
                    'Subnet_Mask' : mask, 
                    'Number_of_Subnets' : numSubnets,
                    'Number_of_Hosts ': numHosts, 
                    'Number_of_Valid_Hosts': validHosts, 
                    'Network_Address': networkAddress, 
                    'First_Host_Address': firstAddress,
                    'Last_Host_Address':lastAddress, 
                    'Broadcast_Address':broadcastAddress
                    }

            print(data)
            
            json_data = json.dumps(data)
            client.send(json_data.encode())
            
            client.close()
        except:
            print('Something went wrong')
            sock.close()
        
        
if __name__ == '__main__':
    server()
