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

#include <ftm2.h>
#include "platform.h"
#include "ftm_util.h"

/**
 * Default handler is called if there is no handler for the FTM0 channel or tof interrupt
 */
void Default_Handler_FTM2()
{
  __asm("bkpt");
  // Still a hacker? ;-)
}

//void FTM2CH0_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
void FTM2CH1_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
void FTM2TOF_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));

#define CHF_CHIE_MASK       (FTM_CnSC_CHF_MASK | FTM_CnSC_CHIE_MASK)
#define TOF_TOIE_MASK       (FTM_SC_TOF_MASK | FTM_SC_TOIE_MASK)

uint32_t nbrOfImpulses;

uint32_t ftm2GetNbrOfImpulses()
{
  return nbrOfImpulses;
}


void FTM2CH0_IRQHandler()
{
  FTM2_C0SC &= ~FTM_CnSC_CHF_MASK;
  nbrOfImpulses++;
}

/**
 * Interrupt handler to distribute the different interrupt sources of the FTM:
 * - channel 0..1
 * - timer overflow
 */
void FTM2_IRQHandler(void)
{
  if ((FTM2_C0SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
    FTM2CH0_IRQHandler();
  if ((FTM2_C1SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
    FTM2CH1_IRQHandler();
  if ((FTM2_SC & TOF_TOIE_MASK) == TOF_TOIE_MASK)
    FTM2TOF_IRQHandler();
}

void ftm2Init(void)
{
  nbrOfImpulses = 0;

  //Configure PTB18 for FTM2_CH0
  PORTB_PCR18 = PORT_PCR_MUX(3);

  // _todo ML#9.01 set clockgating for FTM0
  SIM_SCGC6 |= SIM_SCGC6_FTM2_MASK;

  // sets the modulo
  //  FTM2_MOD = FTM2_MODULO;

  // _todo ML#9.02 configure the timer with "system clock" as clocksource and with a "Prescaler" of 1 => 60 MHz
  FTM2_SC = FTM_SC_CLKS(1) | FTM_SC_PS(0); // | FTM_SC_TOIE(1);

  FTM2_C0SC = FTM_CnSC_INPUT_CAPTURE_RISING | FTM_CnSC_CHIE(1);

  // _todo ML#9.03 Enable FTM0 interrupt on NVIC with Prio: PRIO_FTM0 (defined in platform.h)
  NVIC_SetPriority(FTM2_IRQn, PRIO_FTM2);       // set interrupt priority
  NVIC_EnableIRQ(FTM2_IRQn);                    // enable interrupt
}
