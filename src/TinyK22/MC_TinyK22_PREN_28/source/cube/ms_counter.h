/*
 * ms_counter.h
 *
 *  Created on: 09.05.2019
 *      Author: andre
 */

#ifndef CUBE_MS_COUNTER_H_
#define CUBE_MS_COUNTER_H_

#include "stdint.h"

void ms_Counter_Init(void);

uint32_t getNbrMs(void);

#define millis() (getNbrMs())

#endif /* CUBE_MS_COUNTER_H_ */
