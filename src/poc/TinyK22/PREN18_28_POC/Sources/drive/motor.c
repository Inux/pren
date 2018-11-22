/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         motor driver
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          03.04.20018
 *
 * $Id: motor.c 116 2018-05-11 14:30:59Z zajost $
 *
 * http://www.hessmer.org/blog/2013/12/28/ibt-2-h-bridge-with-arduino/
 *
 *--------------------------------------------------------------------
 */

#include <ftm1.h>
#include "platform.h"
#include "motor.h"
#include "term.h"
#include "util.h"
#include "ftm_util.h"
#include <string.h>

// _todo ML#9.04 complete the macros to switch a pin configuration from GPIO to FTM-Mode and vice versa
#define MOTOR_F_PWM()           (PORTA_PCR12 = PORT_PCR_MUX(3))  // PTDA[12]: FTM1_CH0
#define MOTOR_F_GPIO()          (PORTA_PCR12 = PORT_PCR_MUX(1))  // PTD0[1]: GPIO
#define MOTOR_R_PWM()           (PORTB_PCR0 = PORT_PCR_MUX(3))  // PTE5[6]: FTM1_CH0
#define MOTOR_R_GPIO()          (PORTB_PCR0 = PORT_PCR_MUX(1))  // PTE5[1]: GPIO

static tCommandLineHandler clh;       // terminal command line handler
static int8_t valueMot;


/**
 * Increments or decrements the PWM value oft the right wheel
 * @param[in] value
 *   a positive or negative value to add
 */
void motorIncrementPwm(int8_t value)
{
  int32_t v = valueMot + value;
  if (v > MOTOR_MAX_VALUE) v = MOTOR_MAX_VALUE;
  if (v < -MOTOR_MAX_VALUE) v = -MOTOR_MAX_VALUE;
  motorSetPwm((int8_t)v);
}


/**
 * Sets the PWM value of the right wheel
 *
 * @param[in] value
 *   the value between -MOTOR_MAX_VALUE..0..+MOTOR_MAX_VALUE
 *   A value of '0' stops the wheel.
 */
void motorSetPwm(int8_t value)
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
  int16_t v = (uint16_t)(((FTM1_MODULO + 1) * ((uint32_t)value)) / MOTOR_MAX_VALUE);
  FTM1_C0V = v;
}

/**
 * Command line parser for this file.
 * This code is complete and works.
 *
 * @param[in] cmd
 *   the command to parse
 */
tError motorParseCommand(const unsigned char *cmd)
{
  tError result = EC_INVALID_ARG;
  if (strcmp(cmd, "help") == 0)
  {
    termWriteLine("mot (motor) commands:");
    termWriteLine("  help");
    termWriteLine("  set [-100..100]");
    termWriteLine("  status");
    result = EC_SUCCESS;
  }
  else if (strncmp(cmd, "set", sizeof("set")-1) == 0)
  {
    cmd += sizeof("set");
    int16_t v;
    result = utilScanDecimal16s(&cmd, &v);
    if (result != EC_SUCCESS) return result;
    motorSetPwm((int16_t)((MOTOR_MAX_VALUE * v) / 100));
  }
  return result;
}



/**
 * Initializes the motor driver
 */
void motorInit(void)
{
  // _todo ML#9.05 Configure the pin direction of the 2 pins as output.
  GPIOA_PDDR = 1<<12;
  GPIOB_PDDR = 1<<0;

  // _todo ML#9.06 set the pin value of all of the 2 pins to '0'
  GPIOA_PCOR = 1<<12;
  GPIOB_PCOR = 1<<0;

  // configures the pin muxing of all of the 2 pins as GPIO-Pin.
  // the output level will be '0' because of the configuration above.
  MOTOR_F_GPIO();
  MOTOR_R_GPIO();

  // _todo ML#9.07 configure channel as edge aligned PWM with high-true pulses
  FTM1_C0SC = FTM_CnSC_EDGE_PWM_HIGH_TRUE;

  // register terminal command line handler
  termRegisterCommandLineHandler(&clh, "mot", "(motor)", motorParseCommand);
}
