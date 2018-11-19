/*
 * fmt_util.h
 *
 *  Created on: 16.11.2018
 *      Author: andre
 */

#ifndef SOURCES_FTM_FTM_UTIL_H_
#define SOURCES_FTM_FTM_UTIL_H_

#include "MK22F51212.h"

//*****************************
//BEGIN FTMx_SC Status And Control

//Clock Source Selection --> p.904
typedef enum {
  None = 0,
  SystemClock = 0b01,
  FixedFrequencyClock = 0b10,
  ExternalClockSource = 0b11,
} FMT_SC_CLKS_VALUES;

#define FT_SC_CLKS_NONE     FTM_SC_CLKS(None)
#define FT_SC_CLKS_SYSTEM   FTM_SC_CLKS(SystemClock)
#define FT_SC_CLKS_FIX      FTM_SC_CLKS(FixedFrequencyClock)
#define FT_SC_CLKS_EXTERNAL FTM_SC_CLKS(ExternalClockSource)

//Prescale Factor Selection --> p.904 (use with FTM_SC_PS(x))
typedef enum
{
  DivideBy1   = 0b000,
  DivideBy2   = 0b001,
  DivideBy4   = 0b010,
  DivideBy8   = 0b011,
  DivideBy16  = 0b100,
  DivideBy32  = 0b101,
  DivideBy64  = 0b110,
  DivideBy128 = 0b111,
} FTM_SC_PS_VALUES;

//END   FTMx_SC Status And Control
//*****************************

//*****************************
//BEGIN FTMx_CnSC Channel (n) Status And Control

//mode Selection --> p.906
#define FMT_CnSC_MSB_MSA(x)            (FTM_CnSC_MSB((x&0b10)>>1) | FTM_CnSC_MSA((x&0b01)))
#define FMT_CnSC_ELSB_ELSA(x)          (FTM_CnSC_ELSEB((x&0b10)>>1) | FTM_CnSC_ELB((x&0b01)))

#define FTM_CnSC_NOT_USED              (FMT_CnSC_ELSB_ELSA(0))
#define FTM_CnSC_INPUT_CAPTURE_BASE    (FMT_CnSC_MSB_MSA(0))
#define FTM_CnSC_INPUT_CAPTURE_RISING  (FTM_CnSC_INPUT_CAPTURE_BASE | FMT_CnSC_ELSB_ELSA(0b01))
#define FTM_CnSC_INPUT_CAPTURE_FALLING (FTM_CnSC_INPUT_CAPTURE_BASE | FMT_CnSC_ELSB_ELSA(0b10))
#define FTM_CnSC_INPUT_CAPTURE_BOTH    (FTM_CnSC_INPUT_CAPTURE_BASE | FMT_CnSC_ELSB_ELSA(0b11))
#define FTM_CnSC_OUTPUT_COMPARE_BASE   (FMT_CnSC_MSB_MSA(0b01))
#define FTM_CnSC_OUTPUT_COMPARE_TOGGLE (FTM_CnSC_OUTPUT_COMPARE_BASE | FMT_CnSC_ELSB_ELSA(0b01))
#define FTM_CnSC_OUTPUT_COMPARE_CLEAR  (FTM_CnSC_OUTPUT_COMPARE_BASE | FMT_CnSC_ELSB_ELSA(0b10))
#define FTM_CnSC_OUTPUT_COMPARE_SET    (FTM_CnSC_OUTPUT_COMPARE_BASE | FMT_CnSC_ELSB_ELSA(0b11))
#define FTM_CnSC_EDGE_PWM_BASE         (FMT_CnSC_MSB(1))
#define FTM_CnSC_EDGE_PWM_HIGH_TRUE    (FTM_CnSC_EDGE_PWM_BASE | FMT_CnSC_ELSB_ELSA(0b10))
#define FTM_CnSC_EDGE_PWM_LOW_TRUE     (FTM_CnSC_EDGE_PWM_BASE | FMT_CnSC_ELSA(1))

//Center PWM and Combine PWM not availabel

//END FTMx_CnSC Channel (n) Status And Control
//*****************************

FTM_SC_PS_VALUES FTM_SC_PS_getApproximativeScaler(double devider);






#endif /* SOURCES_FTM_FTM_UTIL_H_ */
