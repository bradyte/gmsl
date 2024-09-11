#!/usr/bin/env python3

from smbus2 import SMBus, i2c_msg
import csv
import time

class GMSL2:
    def __init__(self, device_address):
        self.device_address = device_address >> 1  # convert to 7-bit notation
        self.device_id = self.register_read(0x0D)
        self.device_revision = self.register_read(0x0E)

    def register_read(self, register_address, print_reg=False):
        write = i2c_msg.write(self.device_address, self._convert_16bit(register_address))
        read = i2c_msg.read(self.device_address, 1)
        
        with SMBus(1) as bus:
            bus.i2c_rdwr(write, read)
        # time.sleep(0.001)

        read_value = list(read)[0]

        if print_reg:
            print(f'Read Register: 0x{register_address:04x} Value: 0x{read_value:02x}')

        return read_value

    def register_write(self, register_address, register_value):
        write_data = self._convert_16bit(register_address)
        write_data.append(register_value)
        
        write = i2c_msg.write(self.device_address, write_data)
        
        with SMBus(1) as bus:
            bus.i2c_rdwr(write)
        # time.sleep(0.001)

    def cpp_register_write(self, cpp_file, print_reg=True):
        with open(cpp_file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    val = int(row[0], 0)  # check if the row is a command
                    num_bytes = val
                    if num_bytes == 0:
                        delay = int(row[1], 0)
                        time.sleep(0.001 * delay)
                        print(f'delayed {delay}ms ...')
                    else:
                        addr = int(row[1], 0) >> 1
                        msb = int(row[2], 0)
                        lsb = int(row[3], 0)
                        write_val = int(row[4], 0)
                        
                        write = i2c_msg.write(addr, [msb, lsb, write_val])

                        with SMBus(1) as bus:
                            bus.i2c_rdwr(write)
                        time.sleep(0.001)

                        write = i2c_msg.write(addr, [msb, lsb])
                        read = i2c_msg.read(addr, 1)
                        
                        with SMBus(1) as bus:
                            bus.i2c_rdwr(write, read)
                        # time.sleep(0.001)
                        read_value = list(read)[0]
                        if print_reg:
                            print(f'Wrote Register: 0x{((msb << 8) + lsb):04x} Value: 0x{read_value:02x}')

                except IndexError:  # ignore blank lines
                    pass
                except ValueError:  # ignore comments
                    pass

    def _convert_16bit(self, register_address):
        register_msb = register_address >> 8
        register_lsb = register_address & 0xFF

        return [register_msb, register_lsb]
        
    def device_info(self):
        print(
            f'GMSL device info:\n'
            f'------------------------------------\n'
            f'7-bit Address: 0x{self.device_address:02x}\n'
            f'ID: 0x{self.device_id:02x}\n'
            f'Revision: 0x{self.device_revision:02x}\n'
            f'------------------------------------\n'
        )

def main():
    gmsl2 = GMSL2(0x4e)  # create GMSL object
    gmsl2.device_info()  # get info on GMSL device

    register_value = gmsl2.register_read(0x0000, print_reg=True)  # read register, return value, print if needed
    
    gmsl2.register_write(0x0019, 0xAA)  # write to register with value

    gmsl2.register_read(0x0019, print_reg=True)  # read and print register value

    cpp_file = 'AD-GMSLCAMRPI-ADP_717_724.cpp'
    gmsl2.cpp_register_write(cpp_file)  # read in cpp file

if __name__ == "__main__":
    main()

