/*
 * motor_A.h
 *
 *  Created on: 07.03.2019
 *      Author: andre
 */

#ifndef DRIVE_MOTOR_A_H_
#define DRIVE_MOTOR_A_H_

#include <stdint.h>
#include "fsl_gpio.h"
#include "pin_mux.h"

#define MOTOR_A_PI_TOPIC "motor"

#define MOTOR_MAX_VALUE               100

void motor_A_SetPwm(int8_t value);

void motor_A_init(void);

#endif /* DRIVE_MOTOR_A_H_ */
