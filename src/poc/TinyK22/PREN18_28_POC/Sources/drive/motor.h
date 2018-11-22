/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         motor driver
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          03.04.20018
 *
 * $Id: motor.h 116 2018-05-11 14:30:59Z zajost $
 *
 *--------------------------------------------------------------------
 */

#ifndef SOURCES_DRIVE_MOTOR_H_
#define SOURCES_DRIVE_MOTOR_H_

#define MOTOR_MAX_VALUE               127

void motorIncrementPwm(int8_t value);

void motorSetPwm(int8_t value);
void motorInit(void);

#endif /* SOURCES_DRIVE_MOTOR_H_ */
