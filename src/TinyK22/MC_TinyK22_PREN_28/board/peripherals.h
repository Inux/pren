/***********************************************************************************************************************
 * This file was generated by the MCUXpresso Config Tools. Any manual edits made to this file
 * will be overwritten if the respective MCUXpresso Config Tools is used to update this file.
 **********************************************************************************************************************/

#ifndef _PERIPHERALS_H_
#define _PERIPHERALS_H_

/***********************************************************************************************************************
 * Included files
 **********************************************************************************************************************/
#include "fsl_common.h"
#include "fsl_clock.h"
#include "fsl_ftm.h"

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/***********************************************************************************************************************
 * Definitions
 **********************************************************************************************************************/
/* Definitions for BOARD_InitPeripherals functional group */
/* Definition of peripheral ID */
#define FTM_1_MOTOR_PWM_PERIPHERAL FTM1
/* Definition of the clock source frequency */
#define FTM_1_MOTOR_PWM_CLOCK_SOURCE CLOCK_GetFreq(kCLOCK_BusClk)
/* FTM_1_Motor_PWM interrupt vector ID (number). */
#define FTM_1_MOTOR_PWM_IRQN FTM1_IRQn
/* FTM_1_Motor_PWM interrupt handler identifier. */
#define FTM_1_MOTOR_PWM_IRQHANDLER FTM1_IRQHandler

/***********************************************************************************************************************
 * Global variables
 **********************************************************************************************************************/
extern const ftm_config_t FTM_1_Motor_PWM_config;

/***********************************************************************************************************************
 * Initialization functions
 **********************************************************************************************************************/
void BOARD_InitPeripherals(void);

/***********************************************************************************************************************
 * BOARD_InitBootPeripherals function
 **********************************************************************************************************************/
void BOARD_InitBootPeripherals(void);

#if defined(__cplusplus)
}
#endif

#endif /* _PERIPHERALS_H_ */
