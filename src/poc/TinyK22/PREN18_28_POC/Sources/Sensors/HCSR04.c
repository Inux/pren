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

/* PORTD_PCR5: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,ISF=1,??=0,??=0,??=0,??=0,IRQC=0,LK=0,??=0,??=0,??=0,??=0,MUX=4,??=0,DSE=0,ODE=0,PFE=0,??=0,SRE=0,PE=0,PS=0 */
#define PORTD_PCR5_VALUE   0x01000400U
#define PORTD_PCR5_MASK    0xFFFFFFFFU
/* PORTD_PCR7: ??=0,??=0,??=0,??=0,??=0,??=0,??=0,ISF=1,??=0,??=0,??=0,??=0,IRQC=0,LK=0,??=0,??=0,??=0,??=0,MUX=4,??=0,DSE=0,ODE=0,PFE=0,??=0,SRE=0,PE=0,PS=0 */
#define PORTD_PCR7_VALUE   0x01000400U
#define PORTD_PCR7_MASK    0xFFFFFFFFU

#define SPEED_OF_SOUND_MM_S 343500 //343500 mm/s ==> 343,5 m/s
#define SPEED_OF_SOUND_MM_MS 343.5


static uint32_t hcsr04_ticks;
static float hcsr04_dist_mm;
static float hcsr04_time_ms;
static bool hcsr04_objectDetected;

uint32_t hcsr04GetLastTicks()
{
  return hcsr04_ticks;
}

float hcsr04GetLastDist_mm()
{
  return hcsr04_dist_mm;
}

float hcsr04GetLastTime_ms()
{
  return hcsr04_time_ms;
}

void FTM0CH7_IRQHandler(void)
{
  if (FTM0_C7SC & FTM_CnSC_CHF_MASK)
  {
    // check for channel 0 interrupt
    FTM0_C7SC &= ~FTM_CnSC_CHF_MASK;        // clear interrupt flag
    hcsr04_ticks = FTM0_C7V;
    hcsr04_time_ms = FTM0_TICKS2MS((float )hcsr04_ticks);
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

void FTM0CH5_IRQHandler(void)
{
  __asm("bkpt");
  // Still a hacker? ;-) FTM0 CH5 is used as trigger for the HCSR04
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
  PORTD_PCR5 = (PORTD_PCR5 & (~PORTD_PCR5_MASK)) | PORTD_PCR5_VALUE;
  PORTD_PCR7 = (PORTD_PCR7 & (~PORTD_PCR7_MASK)) | PORTD_PCR7_VALUE;

  ftm0Init();

}

