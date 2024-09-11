from gmsl2 import GMSL2
import time
import logging

gmsl2_ser = GMSL2(0x80)

logging.info('Write WAKE_EN_A = WAKE_EN_B = 0 to local device.')
gmsl2_ser.register_write(0x000C, 0x0A)  # Write WAKE_EN_A = WAKE_EN_B = 0 to local device

logging.info('Write RESET_LINK = 1 to local device.')
gmsl2_ser.register_write(0x0010, 0x51)  # Write RESET_LINK = 1 to local device.

logging.info('Write SLEEP = 1 to remote device.')
gmsl2_ser.register_write(0x0010, 0x19)  # Write SLEEP = 1 to remote device.

logging.info('Going to sleep.')
time.sleep(1)
logging.info('Waking up.')

logging.info('Dummy Transaction')
try:
    gmsl2_ser.register_read(0x0000)
except OSError:
    logging.debug('OSError occured')
    pass
time.sleep(0.005)

logging.info('Write SLEEP = 0 to remote device.')
gmsl2_ser.register_write(0x0010, 0x51)  # Write SLEEP = 0 to remote device.

logging.info('Write RESET_LINK = 0 to local device.')
gmsl2_ser.register_write(0x0010, 0x11)  # Write RESET_LINK = 0 to local device.

while not (gmsl2_ser.is_locked()):
    time.sleep(0.001)
    logging.info(f' ...checking lock status: LOCK = {gmsl2_ser.is_locked()}')

