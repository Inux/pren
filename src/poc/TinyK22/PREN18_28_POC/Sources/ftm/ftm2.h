/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         Common settings of the FTM2
 * \file
 * \author        Andreas Rebsamen
 * \date          14.12.2018
 *
 *--------------------------------------------------------------------
 */

#ifndef SOURCES_FTM2_H_
#define SOURCES_FTM2_H_

#include "stdint.h"

#define FTM2_CLOCK              60000000  // 60 MHz
#define FTM2_MODULO               0x0FFF  // 4095

void ftm2Init(void);

uint32_t ftm2GetNbrOfImpulses();
uint32_t ftm2GetRevMin();
uint32_t ftm2GetLastDivTicks();

#endif /* SOURCES_FTM2_H_ */
