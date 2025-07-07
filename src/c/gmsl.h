#ifndef __GMSL_H_
#define __GMSL_H_

#include <stdint.h>



struct gmsl_dev
{
    int fd;             //I2C file descriptor
    uint8_t address;    // 7-bit I2C address
};



#endif