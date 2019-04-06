/*
 * quad.c
 *
 *  Created on: 28.03.2019
 *      Author: andre
 */

#include <stdint.h>
#include <stdbool.h>
#include "pin_mux.h"
#include "peripherals.h"
#include "fsl_ftm.h"
#include "MK22F51212.h"
#include "pi.h"
#include "comLog.h"
#include "McuCriticalSection.h"

#define FTM2_CLOCK      (60000000)
#define WHEEL_RADIUS    (13)
#define TICKS_PER_REV   (1024)
#define PI              (3.14159)


static bool newDivTick;
static uint32_t oldTicks_A;
static uint32_t divTicks_A = 0;
uint32_t nbrTicks_A;
uint32_t avgTicks_A;

uint32_t nbrTicks_S;

/**
 * returns the number of ticks occurred since 'Encoder_S_StartCountingTicks(void)'
 */
uint32_t Encoder_S_GetNbrOfTicks()
{
  return nbrTicks_S;
}

/**
 * resets the counter for the Schwenker Encoder
 */
void Encoder_S_StartCountingTicks(void)
{
  nbrTicks_S = 0;
}

/**
 * returns the absolute Value of the speed
 * according to the A Encoder
 * with the last number of ticks occurred in a 10ms period
 */
uint16_t Encoder_A_GetAbsSpeed()
{
  float speed = 0;
  uint32_t ticks = avgTicks_A;

  speed = (100* 2*PI*WHEEL_RADIUS*ticks)/ (TICKS_PER_REV *2);

  return (uint16_t) (speed);
}

/**
 * Hander for the Schwenker Encoder
 */
void Encoder_S_IRQHandler(void)
{
  if (FTM_GetStatusFlags(FTM_2_ENCODER_PERIPHERAL) & kFTM_Chnl0Flag)
  {
    nbrTicks_S++;
    FTM_ClearStatusFlags(FTM_2_ENCODER_PERIPHERAL, kFTM_Chnl0Flag);
  }
}

/**
 * Handler for the Antrieb Encoder
 */
void Encoder_A_IRQHandler(void)
{
  if (FTM_GetStatusFlags(FTM_2_ENCODER_PERIPHERAL) & kFTM_Chnl1Flag)
  {
    nbrTicks_A++;
    FTM_ClearStatusFlags(FTM_2_ENCODER_PERIPHERAL, kFTM_Chnl1Flag);
  }
}

/**
 * Time overflow handler
 * used to count ticks in a exact period of time from the Antireb
 */
void FTM2TOF_IRQHandler(void)
{
  if (FTM_GetStatusFlags(FTM_2_ENCODER_PERIPHERAL) & kFTM_TimeOverflowFlag)
  {
    avgTicks_A = nbrTicks_A;
    nbrTicks_A = 0;
    FTM_ClearStatusFlags(FTM_2_ENCODER_PERIPHERAL, kFTM_TimeOverflowFlag);
  }
}

/**
 * FTM2 IRQ handler for the encoders
 */
void FTM_2_ENCODER_IRQHANDLER(void)
{
  //if ((FTM2_C0SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
  if (FTM_GetEnabledInterrupts(FTM_2_ENCODER_PERIPHERAL) & kFTM_Chnl0InterruptEnable)
    Encoder_S_IRQHandler();
//  if ((FTM2_C1SC & CHF_CHIE_MASK) == CHF_CHIE_MASK)
  if (FTM_GetEnabledInterrupts(FTM_2_ENCODER_PERIPHERAL) & kFTM_Chnl1InterruptEnable)
    Encoder_A_IRQHandler();
//  if ((FTM2_SC & TOF_TOIE_MASK) == TOF_TOIE_MASK)
  if (FTM_GetEnabledInterrupts(FTM_2_ENCODER_PERIPHERAL) & kFTM_TimeOverflowInterruptEnable)
    FTM2TOF_IRQHandler();
}

/**
 * Initializes the Encoder module
 */
void encoder_Init(void)
{
  Encoder_InitPins();

  nbrTicks_A = 0;
  nbrTicks_S = 0;

  newDivTick = false;
  oldTicks_A = 0;
  divTicks_A = 1;

}
