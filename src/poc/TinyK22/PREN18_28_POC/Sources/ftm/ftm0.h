/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         Common settings of the FTM0
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          26.03.20018
 *
 * $Id: ftm0.h 94 2018-04-25 11:07:33Z zajost $
 *
 *--------------------------------------------------------------------
 */

#ifndef SOURCES_FTM0_H_
#define SOURCES_FTM0_H_

#include "ftm0.h"
#include "platform.h"

#define FTM0_CLOCK              BUSCLOCK
#define FTM0_CLOCK_DEVIDER      64

#define FMT0_FREQ               (FTM0_CLOCK/FTM0_CLOCK_DEVIDER)
#define FTM0_TICKS2MS(x)        (x/(FMT0_FREQ/1000))
//#define FTM0_TICKS2US(x)        (x/(FMT0_FREQ/1000000))
#define FTM0_MS2TICKS(x)        ((FMT0_FREQ/1000)*(x))

//Configuration from Processor Expert
/* FTM0_SC: TOF=0,TOIE=0,CPWMS=0,CLKS=1,PS=6 */
#define FTM0_SC_VALUE      0x0EU
#define FTM0_SC_MASK       0xFFU

#define FTM0_MOD_VALUE       0xC350U

/* FTM0_C5SC: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,CHF=0,CHIE=0,MSB=1,ELSB=0,ELSA=1,ICRST=0,DMA=0 */
#define FTM0_C5SC_VALUE      0x24U
#define FTM0_C5SC_MASK       0xFFFFFFEFU
/* FTM0_C7SC: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,CHF=0,CHIE=1,MSB=0,MSA=0,ELSB=1,ELSA=0,ICRST=0,DMA=0 */
#define FTM0_C7SC_VALUE      0x48U
#define FTM0_C7SC_MASK       0xFFFFFFFFU

/* FTM0_C5V: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,VAL=0x61A8 */
#define FTM0_C5V_VALUE       0x61A8U
#define FTM0_C5V_MASK        0xFFFFFFFFU
/* FTM0_C7V: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0 */
#define FTM0_C7V_VALUE       0x00U
#define FTM0_C7V_MASK        0xFFFF0000U

void ftm0Init(void);

#endif /* SOURCES_FTM0_H_ */
