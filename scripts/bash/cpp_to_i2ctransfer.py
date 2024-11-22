#!/usr/bin/env python3

from smbus2 import SMBus, i2c_msg

i2c_bus = 1
dev_addr = 0x40  # use 7-bit notation

def i2c_write(i2c_bus, dev_addr, reg_addr, reg_value):
    reg_msb = reg_addr >> 8
    reg_lsb = reg_addr & 0xFF

    write_data = [reg_msb, reg_lsb]
    write_data.append(reg_value)

    write = i2c_msg.write(dev_addr, write_data)
        
    with SMBus(i2c_bus) as bus:
        bus.i2c_rdwr(write)
    time.sleep(0.001)

    i2ctransfer_string = f'i2ctransfer -y -f {i2c_bus} w3@0x{dev_addr:02X} 0x{write_data[0]:02X} 0x{write_data[1]:02X} 0x{reg_value:02X}'
    print(i2ctransfer_string)
    return (i2ctransfer_string)

def main():
    with open('gmsl.txt', 'w') as file:
        file.write(i2c_write(1, 0x40, 0x250, 0xaa))

if __name__ == "__main__":
    main()