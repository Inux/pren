/*
 * quad.h
 *
 *  Created on: 28.03.2019
 *      Author: andre
 */

#ifndef DRIVE_QUAD_H_
#define DRIVE_QUAD_H_

#include <stdint.h>

void encoder_Init(void);
uint16_t Encoder_A_GetAbsSpeed(void);

uint32_t Encoder_S_GetNbrOfTicks(void);

void Encoder_S_StartCountingTicks(void);



#endif /* DRIVE_QUAD_H_ */
