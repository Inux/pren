/*
 * ms_counter.c
 *
 *  Created on: 09.05.2019
 *      Author: andre
 */

#include "fsl_ftm.h"
#include "ms_counter.h"
#include "peripherals.h"
#include "ms_counter.h"


static volatile uint32_t nbrMs = 0;

/**
 * returns the nbr of milliseconds passed since the last system reset
 */
uint32_t getNbrMs(void)
{
  return nbrMs;
}

void FTM3_MS_COUNTER_TOF_IRQHandler(void)
{
  if (FTM_GetStatusFlags(FTM_3_MS_COUTNER_PERIPHERAL) & kFTM_TimeOverflowFlag)
  {
    nbrMs++;
    FTM_ClearStatusFlags(FTM_3_MS_COUTNER_PERIPHERAL, kFTM_TimeOverflowFlag);
  }
}

void FTM3_MS_COUNTER_IRQHandler(void)
{
  if (FTM_GetEnabledInterrupts(FTM_3_MS_COUTNER_PERIPHERAL) & kFTM_TimeOverflowInterruptEnable)
    FTM3_MS_COUNTER_TOF_IRQHandler();
}



void ms_Counter_Init(void)
{
  nbrMs = 0;
}
