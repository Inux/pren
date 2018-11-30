/*
 * VL6180X.h
 *
 *  Created on: 30.11.2018
 *      Author: andre
 */

#ifndef SOURCES_SENSORS_VL6180X_H_
#define SOURCES_SENSORS_VL6180X_H_

#include "platform.h"

tError proxSensInit();
tError proxSensWriteReg(uint16_t reg, uint8_t data);
tError proxSensReadReg(uint16_t reg, uint8_t* data);
tError proxSensRange(uint8_t* data);

uint8_t proxSensAddress =  0x29;

#endif /* SOURCES_SENSORS_VL6180X_H_ */
