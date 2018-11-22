/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         Drive with PID
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          04.04.20018
 *
 * $Id: drive.h 116 2018-05-11 14:30:59Z zajost $
 *
 *--------------------------------------------------------------------
 */

#ifndef SOURCES_DRIVE_DRIVE_H_
#define SOURCES_DRIVE_DRIVE_H_

void driveSetParameters(uint8_t pKp, uint8_t pKi);
void driveSetSpeed(int16_t speed);
void driveToWork(void);
void driveInit(void);


#endif /* SOURCES_DRIVE_DRIVE_H_ */
