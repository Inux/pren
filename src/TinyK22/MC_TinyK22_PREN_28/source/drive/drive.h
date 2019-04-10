/*
 * drive.h
 *
 *  Created on: 28.03.2019
 *      Author: andre
 */

#ifndef DRIVE_DRIVE_H_
#define DRIVE_DRIVE_H_

#include <stdint.h>


#define DELTA_T_MS             25

void driveToWork(void);

void driveSetSpeed(int32_t speed);

void driveSetKp(uint8_t KpR);
void driveSetKi(uint8_t KiR);

void drive_Init(void);



#endif /* DRIVE_DRIVE_H_ */
