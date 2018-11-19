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
 * $Id: ftm2.c 94 2018-04-25 11:07:33Z zajost $
 *
 *--------------------------------------------------------------------
 */

#include "platform.h"
#include "ftm2.h"

/**
 * Default handler is called if there is no handler for the FTM2 channel or tof interrupt
 */
void Default_Handler_FTM2()
{
  __asm("bkpt");
  // Still a hacker? ;-)
}

void FTM2CH0_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
void FTM2CH1_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
//void FTM2CH2_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
//void FTM2CH3_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
//void FTM2CH4_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
//void FTM2CH5_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
//void FTM2CH6_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
//void FTM2CH7_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));
void FTM2TOF_IRQHandler(void) __attribute__ ((weak, alias("Default_Handler_FTM2")));

#define CHF_CHIE_MASK       (FTM_CnSC_CHF_MASK | FTM_CnSC_CHIE_MASK)
#define TOF_TOIE_MASK       (FTM_SC_TOF_MASK | FTM_SC_TOIE_MASK)

/**
 * Interrupt handler to distribute the different interrupt sources of the FTM2:
 * - channel 0..7
 * - timer overflow
 */
void FTM2_IRQHandler(void)
{
  if ((FTM2_C0SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
    FTM2CH0_IRQHandler(); //Trigger HCSR04 Ultrasonic distance sensor
  if ((FTM2_C1SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
    FTM2CH1_IRQHandler(); //Echo HCSR04 Ultrasonic distance sensor
  //Not availabel for ftm2
//  if ((FTM2_C2SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
//    FTM2CH2_IRQHandler();
//  if ((FTM2_C3SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
//    FTM2CH3_IRQHandler();
//  if ((FTM2_C4SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
//    FTM2CH4_IRQHandler();
//  if ((FTM2_C5SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
//    FTM2CH5_IRQHandler();
//  if ((FTM2_C6SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
//    FTM2CH6_IRQHandler();
//  if ((FTM2_C7SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
//    FTM2CH7_IRQHandler();
  if ((FTM2_SC & TOF_TOIE_MASK) == TOF_TOIE_MASK)
    FTM2TOF_IRQHandler();
}

void ftm2Init(void)
{
  // _todo #7.3-01 set clockgating for FTM2
  SIM_SCGC6 |= SIM_SCGC6_FTM2_MASK;

  FTM2_SC = (FTM2_SC & (~FTM2_SC_MASK)) | (FTM2_SC_VALUE);
  FTM2_MOD = FTM2_MOD_VALUE;

  FTM2_C0SC = (FTM2_C0SC & (~FTM2_C0SC_MASK)) | FTM2_C0SC_VALUE;
  FTM2_C1SC = (FTM2_C1SC & (~FTM2_C1SC_MASK)) | FTM2_C1SC_VALUE;

  FTM2_C0V = (FTM2_C0V & (~FTM2_C0V_MASK)) | FTM2_C0V_VALUE;
  FTM2_C1V = (FTM2_C1V & (~FTM2_C1V_MASK)) | FTM2_C1V_VALUE;

  // _todo #7.3-03 Enable FTM2 interrupt on NVIC with Prio: PRIO_FTM2 (defined in platform.h)
  NVIC_SetPriority(FTM2_IRQn, PRIO_FTM2);       // set interrupt priority
  NVIC_EnableIRQ(FTM2_IRQn);                    // enable interrupt
}
