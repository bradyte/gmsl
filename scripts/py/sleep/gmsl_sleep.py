from gmsl2 import GMSL2
import time
import logging

gmsl2_ser = GMSL2(0x80)
gmsl2_des = GMSL2(0x90)

logging.info('Write SLEEP = 1 to remote device.')
gmsl2_des.register_write(0x0010, 0x19)  # Write SLEEP = 1 to remote device.

while (1):
    lock_status = gmsl2_ser.is_locked()
    logging.info(f' ...checking lock status: LOCK = {lock_status}')
    if not (lock_status):
        break
    time.sleep(0.001)

logging.info('Write RESET_LINK = 1 to local device.')
gmsl2_ser.register_write(0x0010, 0x51)  # Write RESET_LINK = 1 to local device.

logging.info('Going to sleep.')
time.sleep(1)
logging.info('Waking up.')

logging.info('Write RESET_LINK = 0 to local device.')
gmsl2_ser.register_write(0x0010, 0x11)  # Write RESET_LINK = 0 to local device.

while (1):
    lock_status = gmsl2_ser.is_locked()
    logging.info(f' ...checking lock status: LOCK = {lock_status}')
    if(lock_status):
        break
    time.sleep(0.001)

logging.info('Write SLEEP = 0 to remote device.')
gmsl2_des.register_write(0x0010, 0x11)  # Write SLEEP = 0 to remote device.