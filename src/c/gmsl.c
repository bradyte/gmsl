#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include <sys/ioctl.h>

#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#include "gmsl.h"

struct gmsl_dev ser;
struct gmsl_dev des;


int open_i2c_device(const char* dev_path)
{
    int fd = open(dev_path, O_RDWR);
    if(fd < 0 ) {
        printf("Error opening I2C device %s\n", dev_path);
        return fd;
    }

    return fd;
}

int gmsl_write(int fd, uint8_t dev_addr, uint16_t reg, uint8_t val)
{
    struct i2c_msg msgs[1];
    struct i2c_rdwr_ioctl_data msgset[1];

    uint8_t tx_buf[3] = { reg >> 8, reg & 0xff, val};

    msgs[0].addr = dev_addr;
    msgs[0].flags = 0;
    msgs[0].len = 3;
    msgs[0].buf = tx_buf;

    msgset[0].msgs = msgs;
    msgset[0].nmsgs = 1;

    if (ioctl(fd, I2C_RDWR, &msgset) < 0) {
        printf("Error doing I2C transaction\n");
        return -1;
    }

    return 0;
}



int gmsl_read(struct gmsl_dev dev, uint16_t reg, uint8_t* rx_buf)
{
    struct i2c_msg msgs[2];
    struct i2c_rdwr_ioctl_data msgset[1];

    uint8_t reg_buf[2] = { reg >> 8, reg & 0xff };

    msgs[0].addr = dev.address;
    msgs[0].flags = 0;
    msgs[0].len = 2;
    msgs[0].buf = reg_buf;

    msgs[1].addr = dev.address;
    //Read with no new start bit
    msgs[1].flags = I2C_M_RD | I2C_M_NOSTART;
    msgs[1].len = 1;
    msgs[1].buf = rx_buf;

    msgset[0].msgs = msgs;
    msgset[0].nmsgs = 2;

    if (ioctl(dev.fd, I2C_RDWR, &msgset) < 0) {
        printf("Error doing I2C transaction\n");
        return -1;
    }

    return 0;
}

int gmsl_init(struct gmsl_dev* dev, int fd, uint8_t address)
{
    dev->fd = fd;
    dev->address = address;
}


int main(int argc, char* argv[])
{
    int fd;
    char filename[20];
    uint8_t rx_buf[1];

    if(argc < 2) {
        printf("Not enough args. Expected a I2C device (i.e for /dev/i2c-1, type '1')\n");
        return EXIT_FAILURE;
    }

    snprintf(filename, sizeof(filename), "/dev/i2c-%c", *argv[1]);
	filename[sizeof(filename) - 1] = '\0';

    // Open the I2C device
    fd = open_i2c_device(filename);
    if( fd < 0 ) {
        printf("I2C open failure\n");
        return EXIT_FAILURE;
    }

    gmsl_init(&ser, fd, 0x40);
    gmsl_init(&des, fd, 0x2e);

    
    for(int i; i < 0x10; i++) {
        gmsl_read(ser, i, rx_buf);
        printf("0x%x read byte: %x\n", ser.address, *rx_buf);

        gmsl_read(des, i, rx_buf);
        printf("0x%x read byte: %x\n\n", des.address, *rx_buf);
    }

}

