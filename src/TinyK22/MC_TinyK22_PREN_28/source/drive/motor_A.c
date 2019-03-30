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

#include "pi.h"
#include "McuUtility.h"


#define PORT_PCR_REG(base, pin)   base->PCR[pin]
#define MOTOR_A_PIN_FORWARD_PCR   PORT_PCR_REG(MOTOR_A_PIN_FORWARD_PORT, MOTOR_A_PIN_FORWARD_PIN)
#define MOTOR_A_PIN_REVERSE_PCR   PORT_PCR_REG(MOTOR_A_PIN_REVERSE_PORT, MOTOR_A_PIN_REVERSE_PIN)

#define MOTOR_F_PWM()           (MOTOR_A_PIN_FORWARD_PCR = PORT_PCR_MUX(3))  // PTDA[12]: FTM1_CH0
#define MOTOR_F_GPIO()          (MOTOR_A_PIN_FORWARD_PCR = PORT_PCR_MUX(1))  // PTD0[1]: GPIO
#define MOTOR_R_PWM()           (MOTOR_A_PIN_REVERSE_PCR = PORT_PCR_MUX(3))  // PTE5[6]: FTM1_CH0
#define MOTOR_R_GPIO()          (MOTOR_A_PIN_REVERSE_PCR = PORT_PCR_MUX(1))  // PTE5[1]: GPIO


tframeLineHandler motor_A_FrameHandler;

static int8_t valueMot;

static void motor_A_UpdatePwmDutyCycle(uint32_t value)
{
  if (value > MOTOR_MAX_VALUE)
  {
    value = MOTOR_MAX_VALUE;
  }

  uint32_t mod = FTM_1_MOTOR_PWM_PERIPHERAL->MOD;
  uint32_t cnv = (mod * value) / MOTOR_MAX_VALUE;
  /* For 100% duty cycle */
  if (cnv >= mod)
  {
      cnv = mod + 1;
  }
  FTM_1_MOTOR_PWM_PERIPHERAL->CONTROLS[0].CnV = cnv;

//  FTM_UpdatePwmDutycycle(FTM_1_MOTOR_PWM_PERIPHERAL, 0, kFTM_EdgeAlignedPwm, value);
  FTM_SetSoftwareTrigger(FTM_1_MOTOR_PWM_PERIPHERAL, true);
}

/**
 * Sets the PWM value of the right wheel
 *
 * @param[in] value
 *   the value between -MOTOR_MAX_VALUE..0..+MOTOR_MAX_VALUE
 *   A value of '0' stops the wheel.
 */
void motor_A_SetPwm(int32_t value)
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
    MOTOR_R_GPIO();
    MOTOR_F_PWM();
  }
  else
  {
    // stop
    MOTOR_F_GPIO();
    MOTOR_R_GPIO();
  }
  motor_A_UpdatePwmDutyCycle(value);
}

tError motor_ACommandHandler(const unsigned char *frameValue)
{
  int32_t val = 0;
  McuUtility_ScanDecimal32sNumber(&frameValue, &val);

  if (val > 100)
  {
    val = 100;
  }
  else if (val < -100)
  {
    val = -100;
  }

  motor_A_SetPwm(val);
}

void motor_A_init()
{
  Motor_A_InitPins();
  GPIO_PortClear(MOTOR_A_PIN_FORWARD_GPIO, 1<<MOTOR_A_PIN_FORWARD_PIN);
  GPIO_PortClear(MOTOR_A_PIN_REVERSE_GPIO, 1<<MOTOR_A_PIN_REVERSE_PIN);

  motor_A_SetPwm(0);

  piRegisterFrameLineHandler(&motor_A_FrameHandler, MOTOR_A_PI_TOPIC, "sets to motor PWM to the given value", &motor_ACommandHandler, NULL);
}
