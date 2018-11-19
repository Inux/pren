/*
 * HCSR04.c
 *
 *  Created on: 15.11.2018
 *      Author: andre
 */

#include "ftm0.h"
#include "MK22F51212.h"
#include "HCSR04.h"
#include "util.h"
#include "term.h"

void FTM2CH1_IRQHandler(void)
{
  if (FTM2_C1SC & FTM_CnSC_CHF_MASK)
  {
    // check for channel 0 interrupt
    FTM2_C1SC &= ~FTM_CnSC_CHF_MASK;        // clear interrupt flag
    hcsr04_ticks = FTM2_C1SC;
    hcsr04_time_ms = FTM2_TICKS2MS((float )hcsr04_ticks);
    hcsr04_dist_mm = (hcsr04_time_ms * SPEED_OF_SOUND_MM_MS / 2);
  }
  else
  {
    hcsr04_ticks = -1;
  }

  if (hcsr04_dist_mm < 170)
  {
    GPIOC_PSOR |= (1 << 2);
    hcsr04_objectDetected = TRUE;
  }
  else
  {
    GPIOC_PCOR |= (1 << 2);
  }
}

void FTM2CH0_IRQHandler(void)
{
  __asm("bkpt");
  // Still a hacker? ;-) FTM2 CH0 is used as trigger for the HCSR04
}

/**
 * prints the current status to the terminal
 * Information Format:
 * ticks: {nbrOfTicks}; time: {timeInMs}ms; dist: {distInmm}mm;
 */
void hcsr04PrintCurrentStatus(void)
{
  char buf[128];
  buf[0] = '\0';
  utilStrcat(buf, sizeof(buf), "ticks: ");
  utilStrcatNum32u(buf, sizeof(buf), hcsr04_ticks);
  utilStrcat(buf, sizeof(buf), "; time: ");
  utilStrcatNum32u(buf, sizeof(buf), (uint32_t) hcsr04_time_ms);
  utilStrcat(buf, sizeof(buf), "ms; dist: ");
  utilStrcatNum32u(buf, sizeof(buf), (uint32_t) hcsr04_dist_mm);
  utilStrcat(buf, sizeof(buf), "mm;");
  termWriteLine(buf);

  if (hcsr04_objectDetected)
  {
    hcsr04_objectDetected = FALSE;
    termWriteLine("Object detected");
  }
}

/*
 * Initializes the system for the hcr04 Ultrasonic sensor
 */
void hcsr04Init(void)
{
  PORTB_PCR18 = PORT_PCR_MUX(3);
  PORTB_PCR7 = PORT_PCR_MUX(3);

  ftm2Init();

}

