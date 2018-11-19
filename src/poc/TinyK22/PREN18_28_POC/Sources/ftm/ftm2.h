/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         Common settings of the FTM2
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          26.03.20018
 *
 * $Id: ftm2.h 94 2018-04-25 11:07:33Z zajost $
 *
 *--------------------------------------------------------------------
 */

#ifndef SOURCES_FTM2_H_
#define SOURCES_FTM2_H_

#include "ftm2.h"
#include "platform.h"

#define FTM2_CLOCK              BUSCLOCK
#define FTM2_CLOCK_DEVIDER      64

#define FTM2_FREQ               (FTM2_CLOCK/FTM2_CLOCK_DEVIDER)
#define FTM2_TICKS2MS(x)        (x/(FTM2_FREQ/1000))
//#define FTM2_TICKS2US(x)        (x/(FMT0_FREQ/1000000))
#define FTM2_MS2TICKS(x)        ((FTM2_FREQ/1000)*(x))

//Configuration from Processor Expert
/* FTM2_SC: TOF=0,TOIE=0,CPWMS=0,CLKS=1,PS=6 */
#define FTM2_SC_VALUE      0x0EU
#define FTM2_SC_MASK       0xFFU

#define FTM2_MOD_VALUE       0xC350U

/* FTM2_C0SC: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,CHF=0,CHIE=0,MSB=1,ELSB=0,ELSA=1,ICRST=0,DMA=0 */
#define FTM2_C0SC_VALUE      0x24U
#define FTM2_C0SC_MASK       0xFFFFFFEFU
/* FTM2_C1SC: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,CHF=0,CHIE=1,MSB=0,MSA=0,ELSB=1,ELSA=0,ICRST=0,DMA=0 */
#define FTM2_C1SC_VALUE      0x48U
#define FTM2_C1SC_MASK       0xFFFFFFFFU

/* FTM2_C0V: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,VAL=0x61A8 */
#define FTM2_C0V_VALUE       0x61A8U
#define FTM2_C0V_MASK        0xFFFFFFFFU
/* FTM2_C1V: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0,??=0 */
#define FTM2_C1V_VALUE       0x00U
#define FTM2_C1V_MASK        0xFFFF0000U

void ftm2Init(void);

#endif /* SOURCES_FTM2_H_ */
