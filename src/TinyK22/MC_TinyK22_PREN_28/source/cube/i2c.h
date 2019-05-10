/*
 * i2c.h
 *
 *  Created on: 09.05.2019
 *      Author: andre
 */

#ifndef CUBE_I2C_H_
#define CUBE_I2C_H_

tError i2cReadCmdData(uint8_t adr, uint8_t cmd, uint8_t *data, uint8_t length);
tError i2cWriteCmdData(uint8_t adr, uint8_t cmd, uint8_t *data, uint8_t length);

void i2cInit(void);

#endif /* CUBE_I2C_H_ */
