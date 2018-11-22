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
 * $Id: ftm1.c 102 2018-05-01 14:06:17Z zajost $
 *
 *--------------------------------------------------------------------
 */

#include <ftm1.h>
#include "platform.h"

/**
 * Default handler is called if there is no handler for the FTM0 channel or tof interrupt
 */
void Default_Handler_FTM1()
{
  __asm("bkpt");
  // Still a hacker? ;-)
}

void FTM1CH0_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM1")));
void FTM1CH1_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM1")));
void FTM1TOF_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM1")));

#define CHF_CHIE_MASK       (FTM_CnSC_CHF_MASK | FTM_CnSC_CHIE_MASK)
#define TOF_TOIE_MASK       (FTM_SC_TOF_MASK | FTM_SC_TOIE_MASK)

/**
 * Interrupt handler to distribute the different interrupt sources of the FTM:
 * - channel 0..1
 * - timer overflow
 */
void FTM1_IRQHandler(void)
{
  if ((FTM1_C0SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
    FTM1CH0_IRQHandler();
  if ((FTM1_C1SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
    FTM1CH1_IRQHandler();
  if ((FTM1_SC & TOF_TOIE_MASK) == TOF_TOIE_MASK)
    FTM1TOF_IRQHandler();
}

void ftm1Init(void)
{
  // _todo ML#9.01 set clockgating for FTM0
  SIM_SCGC6 |= SIM_SCGC6_FTM1_MASK;

  // sets the modulo
  FTM1_MOD = FTM1_MODULO;

  // _todo ML#9.02 configure the timer with "system clock" as clocksource and with a "Prescaler" of 1 => 60 MHz
  FTM1_SC = FTM_SC_CLKS(1) | FTM_SC_PS(0);

  // _todo ML#9.03 Enable FTM0 interrupt on NVIC with Prio: PRIO_FTM0 (defined in platform.h)
  NVIC_SetPriority(FTM1_IRQn, PRIO_FTM1);       // set interrupt priority
  NVIC_EnableIRQ(FTM1_IRQn);                    // enable interrupt
}
