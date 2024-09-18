from gmsl2 import GMSL2
import time
import logging

logger = logging.getLogger(__name__)

gmsl2_ser = GMSL2(0x80)
gmsl2_des = GMSL2(0x90)


gmsl2_des.register_write(0x0010, 0x19)  # Write SLEEP = 1 to remote device.
logger.info('Write SLEEP = 1 to remote device.')

while (1):
    lock_status = gmsl2_ser.is_locked()
    logger.info(f' ...checking lock status: LOCK = {lock_status}')
    if not (lock_status):
        break
    time.sleep(0.001)


gmsl2_ser.register_write(0x0010, 0x51)  # Write RESET_LINK = 1 to local device.
logger.info('Write RESET_LINK = 1 to local device.')

logger.info('Going to sleep.')
time.sleep(1)
logger.info('Waking up.')


gmsl2_ser.register_write(0x0010, 0x11)  # Write RESET_LINK = 0 to local device.
logger.info('Write RESET_LINK = 0 to local device.')

while (1):
    lock_status = gmsl2_ser.is_locked()
    logger.info(f' ...checking lock status: LOCK = {lock_status}')
    if(lock_status):
        break
    time.sleep(0.001)

time.sleep(0.002)  # delay to show if not fast enough with subsequent write

gmsl2_des.register_write(0x0010, 0x11)  # Write SLEEP = 0 to remote device.
logger.info('Write SLEEP = 0 to remote device.')