/*
 * HCSR04.h
 *
 *  Created on: 15.11.2018
 *      Author: andre
 */

#ifndef SOURCES_SENSORS_HCSR04_H_
#define SOURCES_SENSORS_HCSR04_H_

uint32_t hcsr04GetLastTicks();
float hcsr04GetLastDist_mm();
float hcsr04GetLastTime_ms();

void hcsr04Init(void);
void hcsr04PrintCurrentStatus(void);

#endif /* SOURCES_SENSORS_HCSR04_H_ */
