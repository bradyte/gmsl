#!/usr/bin/env python3

from smbus2 import SMBus, i2c_msg
import sys
import csv
import time
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s.%(msecs)d] %(levelname)s\t- %(message)s",
    datefmt='%H:%M:%S',
    level=logging.DEBUG
                    )

class GMSL2:
    """This class is intended to help with simple communication with GMSL based 
    devices. Currently, designed for the Raspberry Pi 4 I2C interface and 
    defaults to I2C bus 1. Registers between devices are fairly unique but the
    registers in this module are shared between different GMSL devices.

    :param device_address: the 8-bit I2C GMSL device address
    :type device_address: unsigned char
    :param i2c_bus: the I2C bus number used on the Raspberry Pi (default is '1')
    :type i2c_bus: int
    """

    """The 'registers' dictionary contains the key-value pair of the register 
    name and 16-bit register address taken from the datasheet.
    """
    registers = {
        'REG0':  0x0000,
        'REG13': 0x000D,
        'REG14': 0x000E,
        'CTRL3': 0x0013,
    }

    """The 'device_ids' dictionary contains the key-value pair ot the device id
    and the device name as a string.    
    """
    device_ids = {
        0xbf: 'MAX96717',
        0xbe: 'MAX96716A',
    }

    def __init__(self, device_address, i2c_bus=1):
        self.device_id = None
        self.device_revision = None
        self.device_address = device_address >> 1  # convert to standard 7-bit notation    
        self.i2c_bus = i2c_bus
        self._check_connection()

    def _check_connection(self):
        """Checks to see if there is any GMSL device connected
        """
        try:
            self.register_read(self.registers['REG0'])
            self.device_id = self.register_read(self.registers['REG13'])
            self.device_revision = self.register_read(self.registers['REG14'])
            logger.info(f'Device {self.device_ids[self.device_id]} detected at 0x{self.device_address:02x}')
        except:
            logger.error('No GMSL device detected. Exiting...')
            sys.exit(1)

    def register_read(self, register_address):
        """Perform a basic register read at the provided register address.

        :param register_address: the 16-bit register address
        :type register_address: unsigned int
        :return: the 8-bit register value
        :rtype: int
        """
        write = i2c_msg.write(self.device_address, self._convert_16bit(register_address))
        read = i2c_msg.read(self.device_address, 1)

        self._smbus_read_handler(write, read)
        read_value = list(read)[0]

        logger.debug(f"[device: 0x{self.device_address:02x}]{'read from':>10}"
                    f" addr: 0x{register_address:04x}"
                    f" value: 0x{read_value:02x} (0b{read_value:08b})")
        return read_value
    
    def register_block_read(self, register_address, offset):
        """Perform a block read of registers from a starting register address
        to the end of the offset.

        :param register_address: the 16-bit register address
        :type register_address: unsigned int
        :param offset: number of registers to read to
        :type offset: int
        :return: the 8-bit register value
        :rtype: int
        """
        block_data = []
        for i in range(register_address, register_address+offset):
            block_data.append(self.register_read(i))
        return block_data

    def register_write(self, register_address, register_value):
        """Perform a basic register write to the provided register address.

        :param register_address: the 16-bit register address
        :type register_address: unsigned int
        :param register_value: the 8-bit register value to write
        :type register_value: unsigned char
        """
        write_data = self._convert_16bit(register_address)
        write_data.append(register_value)
        write = i2c_msg.write(self.device_address, write_data)

        self._smbus_write_handler(write)

        logger.debug(f"[device: 0x{self.device_address:02x}]{'write to':>10}"
                    f" addr: 0x{register_address:04x}"
                    f" value: 0x{register_value:02x}")

    def cpp_register_write(self, cpp_file):
        with open(cpp_file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    val = int(row[0], 0)  # check if the row is a command
                    num_bytes = val
                    if num_bytes == 0:
                        delay = int(row[1], 0)
                        time.sleep(0.001 * delay)
                        logging.info(f'delayed {delay}ms ...')
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
                        time.sleep(0.001)
                        read_value = list(read)[0]

                except IndexError:  # ignore blank lines
                    pass
                except ValueError:  # ignore comments
                    pass

    def _convert_16bit(self, register_address):
        """This function converts a 16-bit register address into two 8-bit
        values representing the MSB and LSB.

        :param register_address: the 16-bit GMSL register address
        :param type: int
        :return: the MSB and LSB of the 16-bit address in 8 bit notation
        :rtype: list
        """
        register_msb = register_address >> 8
        register_lsb = register_address & 0xff
        return [register_msb, register_lsb]
        
    def is_locked(self):
        """Checks to see if the GMSL link is locked.

        :return: `True` if locked, `False` otherwise
        :rtype: bool
        """
        return bool(self.register_read(self.registers['CTRL3']) & 0x08)

    def device_info(self):
        """This function simply prints from basic info about the connected
        device to the terminal.
        """
        print(
            f'\nGMSL device info:\n'
            f'------------------------------\n'
            f'Device:\t\t{self.device_ids[self.device_id]}\n'
            f'7-bit Address:\t0x{self.device_address:02x}\n'
            f'Silicon Rev:\t0x{self.device_revision:02x}\n'
            f'------------------------------\n'
        )

    def _smbus_read_handler(self, write, read):
        """Handles performing a read with the SMBus protocol and manages errors.

        :param write: list of concatenated bytes to write
        :type write: list
        :param read: buffer for read data
        :type read: unsigned char
        """
        with SMBus(self.i2c_bus) as bus:
            try:
                bus.i2c_rdwr(write, read)
            except OSError as e:
                logger.error(f'Unable to read on the I2C bus: {e}')
                sys.exit(1)
            except BlockingIOError as e:
                logger.error(f'Unable to read on the I2C bus: {e}')
                sys.exit(1)    
        time.sleep(0.001)

    def _smbus_write_handler(self, write):
        """Handles performing a write with the SMBus protocol and manages errors.

        :param write: list of concatenated bytes to write
        :type write: list
        """
        with SMBus(self.i2c_bus) as bus:
            try:
                bus.i2c_rdwr(write)
            except OSError as e:
                logger.error(f'Unable to write on the I2C bus: {e}')
                sys.exit(1)
            except BlockingIOError as e:
                logger.error(f'Unable to write on the I2C bus: {e}')
                sys.exit(1)
        time.sleep(0.001)

def main():
    gmsl2 = GMSL2(0x80, 1)  # create GMSL object
    gmsl2.device_info()  # get info on GMSL device

    # register_value = gmsl2.register_read(0x0000)  # read register, return value
    # print(f'Register value is: 0x{register_value:2X}')

    # register_value = gmsl2.register_read(0x0019)
    # print(f'Register value is: 0x{register_value:2X}')
    # gmsl2.register_write(0x0019, 0x55)  # write to register with value
    # register_value = gmsl2.register_read(0x0019)
    # print(f'Register value is: 0x{register_value:2X}')

    # cpp_file = 'AD-GMSLCAMRPI-ADP_717_724.cpp'
    # gmsl2.cpp_register_write(cpp_file)  # read in cpp file

if __name__ == "__main__":
    main()
