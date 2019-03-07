/*
 * motor_A.c
 *
 *  Created on: 07.03.2019
 *      Author: andre
 */

#include "motor_A.h"

#include "fsl_gpio.h"
#include "pin_mux.h"
#include "peripherals.h"
#include "MK22F51212.h"


#define PORT_PCR_REG(base, pin)   base->PCR[pin]
#define MOTOR_A_PIN_FORWARD_PCR   PORT_PCR_REG(MOTOR_A_PIN_FORWARD_PORT, MOTOR_A_PIN_FORWARD_PIN)
#define MOTOR_A_PIN_REVERSE_PCR   PORT_PCR_REG(MOTOR_A_PIN_FORWARD_PORT, MOTOR_A_PIN_FORWARD_PIN)

#define MOTOR_F_PWM()           (MOTOR_A_PIN_FORWARD_PCR = PORT_PCR_MUX(3))  // PTDA[12]: FTM1_CH0
#define MOTOR_F_GPIO()          (MOTOR_A_PIN_FORWARD_PCR = PORT_PCR_MUX(1))  // PTD0[1]: GPIO
#define MOTOR_R_PWM()           (MOTOR_A_PIN_REVERSE_PCR = PORT_PCR_MUX(3))  // PTE5[6]: FTM1_CH0
#define MOTOR_R_GPIO()          (MOTOR_A_PIN_REVERSE_PCR = PORT_PCR_MUX(1))  // PTE5[1]: GPIO

static int8_t valueMot;

static void motor_A_UpdatePwmDutyCycle(uint8_t percentage)
{
  if (percentage > 100)
  {
    percentage = 100;
  }

  FTM_UpdatePwmDutycycle(FTM_1_MOTOR_PWM_PERIPHERAL, 0, kFTM_EdgeAlignedPwm, percentage);
}

/**
 * Sets the PWM value of the right wheel
 *
 * @param[in] value
 *   the value between -MOTOR_MAX_VALUE..0..+MOTOR_MAX_VALUE
 *   A value of '0' stops the wheel.
 */
void motor_A_SetPwm(int8_t value)
{
  if (value > MOTOR_MAX_VALUE) value = MOTOR_MAX_VALUE;
  if (value < -MOTOR_MAX_VALUE) value = -MOTOR_MAX_VALUE;
  valueMot = value;

  if (value < 0)
  {
    // drive backward
    value = -value;             // value has to be a positive channel value!
    MOTOR_F_GPIO();       // set motor right A as GPIO Pin (high-level)
    MOTOR_R_PWM();        // set motor right B as timer Pin (pwm signal)
  }
  else if (value > 0)
  {
    // drive forward
    // _todo ML#9.08 complete the else-if statement
    MOTOR_R_GPIO();
    MOTOR_F_PWM();
  }
  else
  {
    // stop
    // _todo ML#9.09 complete the else statement
    MOTOR_F_GPIO();
    MOTOR_R_GPIO();
  }
  motor_A_UpdatePwmDutyCycle(value);
}

void motor_A_init()
{
  Motor_A_InitPins();
  motor_A_SetPwm(0);
}
