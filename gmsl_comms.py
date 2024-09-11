from gmsl2 import GMSL2

gmsl2 = GMSL2(0x4e)  # create GMSL object
gmsl2.device_info()  # get info on GMSL device

register_value = gmsl2.register_read(0x0000, print_reg=True)  # read register, return value, print if needed
gmsl2.register_write(0x0019, 0xAA)  # write to register with value
gmsl2.register_read(0x0019, print_reg=True)
cpp_file = 'AD-GMSLCAMRPI-ADP_717_724.cpp'
gmsl2.cpp_register_write(cpp_file)