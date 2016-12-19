#!/usr//bin/python

class DS18B20:
    # TODO default device to first found
    # TODO throw exception if device file not found
    def __init__(self, device):
        self.device = device

    def read_centigrade(self):
        path = '/sys/bus/w1/devices/' + self.device + '/w1_slave'
        with open(path) as f:
            lines = []
            status = ''
            while status != 'YES':
                lines = f.readlines()
                status = lines[0].split()[-1]

            temp = lines[1].split()[-1].split('=')[-1]
            return int(temp)/1000.0

    def read_fahrenheit(self):
        return self.read_centigrade()*9.0/5.0 + 32.0
