/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         Common settings of the FTM1
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          03.04.20018
 *
 * $Id: ftm1.h 94 2018-04-25 11:07:33Z zajost $
 *
 *--------------------------------------------------------------------
 */

#ifndef SOURCES_FTM1_H_
#define SOURCES_FTM1_H_

#define FTM1_CLOCK              60000000  // 60 MHz
#define FTM1_MODULO               0x0FFF  // 4095

void ftm1Init(void);

#endif /* SOURCES_FTM1_H_ */
