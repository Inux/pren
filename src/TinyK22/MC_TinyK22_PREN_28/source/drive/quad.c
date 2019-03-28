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
#define WHEEL_RADIUS    (11)
#define TICKS_PER_REV   (1024)
#define PI              (3.14159)


bool newDivTick;
uint32_t oldTicks_A;
uint32_t divTicks_A;

uint32_t nbrTicks_S;

uint32_t Encoder_S_GetNbrOfTicks()
{
  return nbrTicks_S;
}

void Encoder_S_StartCountingTicks(void)
{
  nbrTicks_S = 0;
}

uint16_t Encoder_A_GetAbsSpeed()
{
  McuCriticalSection_CriticalVariable();
  uint16_t speed = 0;

  if (divTicks_A > 0 && newDivTick)
  {
    McuCriticalSection_EnterCritical();
    newDivTick = false;
    McuCriticalSection_ExitCritical();

    speed = WHEEL_RADIUS * 2*PI * FTM2_CLOCK / (2* divTicks_A * TICKS_PER_REV);
  }

  return speed;
}

#define FTM_CnV_REG(base,index)                  ((base)->CONTROLS[index].CnV)

void Encoder_S_IRQHandler(void)
{
  //FTM2_C0SC &= ~FTM_CnSC_CHF_MASK;
  FTM_ClearStatusFlags(FTM_2_ENCODER_PERIPHERAL, kFTM_Chnl0Flag);
  nbrTicks_S++;
}

void Encoder_A_IRQHandler(void)
{
  McuCriticalSection_CriticalVariable();
  //FTM2_C1SC &= ~FTM_CnSC_CHF_MASK;
  FTM_ClearStatusFlags(FTM_2_ENCODER_PERIPHERAL, kFTM_Chnl1Flag);

  uint32_t newTicks_A = FTM_CnV_REG(FTM_2_ENCODER_PERIPHERAL,1);
  divTicks_A = newTicks_A - oldTicks_A;
  McuCriticalSection_EnterCritical();
  newDivTick = true;
  McuCriticalSection_ExitCritical();
  oldTicks_A = newTicks_A;
}

void FTM2TOF_IRQHandler(void)
{
  LOG_ERROR("FTM2 Encoder TOF occurred");
  FTM_ClearStatusFlags(FTM_2_ENCODER_PERIPHERAL, kFTM_TimeOverflowFlag);
}

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

void quad_Init(void)
{
  Encoder_InitPins();
  FTM_SetTimerPeriod(FTM_2_ENCODER_PERIPHERAL, 0);

  nbrTicks_S = 0;

  newDivTick = false;
  oldTicks_A = 0;
  divTicks_A = 1;

}
