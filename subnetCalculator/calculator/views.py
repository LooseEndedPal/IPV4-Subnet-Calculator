from django.shortcuts import render
from .forms import SubnetForm

import json
import socket

def home(request):
    if request.method == 'POST':
        form =SubnetForm(request.POST)
        if form.is_valid():
            try:
                ipv4 = form.cleaned_data['address']
                prefix = form.cleaned_data['prefix']
                
                socket.inet_pton(socket.AF_INET, ipv4)
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', 5000))
                message = f"{ipv4}\n{prefix}"
                print(message)
                sock.send(message.encode())
                data = sock.recv(1024).decode()
                dict_data = json.loads(data)
                print(dict_data)
                sock.close()
                return render(request, 'results.html', {'data': dict_data})
            except:
                return render(request, 'invalid.html')
    else:
        form = SubnetForm()
    return render(request, 'subnetForm.html', {'form': form})