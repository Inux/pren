/*
 * HCSR04.h
 *
 *  Created on: 15.11.2018
 *      Author: andre
 */

#ifndef SOURCES_SENSORS_HCSR04_H_
#define SOURCES_SENSORS_HCSR04_H_

/* PORTD_PCR5: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,ISF=1,??=0,??=0,??=0,??=0,IRQC=0,LK=0,??=0,??=0,??=0,??=0,MUX=4,??=0,DSE=0,ODE=0,PFE=0,??=0,SRE=0,PE=0,PS=0 */
#define PORTD_PCR5_VALUE   0x01000400U
#define PORTD_PCR5_MASK    0xFFFFFFFFU
/* PORTD_PCR7: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,ISF=1,??=0,??=0,??=0,??=0,IRQC=0,LK=0,??=0,??=0,??=0,??=0,MUX=4,??=0,DSE=0,ODE=0,PFE=0,??=0,SRE=0,PE=0,PS=0 */
#define PORTD_PCR7_VALUE   0x01000400U
#define PORTD_PCR7_MASK    0xFFFFFFFFU

#define SPEED_OF_SOUND_MM_S 343500 //343500 mm/s ==> 343,5 m/s
#define SPEED_OF_SOUND_MM_MS 343.5

uint32_t hcsr04_ticks;
float hcsr04_dist_mm;
float hcsr04_time_ms;
bool hcsr04_objectDetected;

void hcsr04Init(void);
void hcsr04PrintCurrentStatus(void);

#endif /* SOURCES_SENSORS_HCSR04_H_ */
