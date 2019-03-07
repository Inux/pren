/*
 * testApp.c
 *
 *  Created on: 07.03.2019
 *      Author: andre
 */

#include <stdint.h>
#include "fsl_debug_console.h"
#include <stdio.h>
#include "board.h"
#include "motor_A.h"

void delay(void) // TODO: Remove, ugly
{
  for (uint32_t i = 0; i < 8000000; i++)
  {
  }
}

void testMotor_A() // TODO: Remove, ugly
{
  static int8_t value;
  static int8_t step = 1;

  const int maxValue = 25;

  if ((value >= maxValue && step > 0) ||
      (value <= -maxValue && step < 0))
  {
    step = -step;
  }

  value += step;
  motor_A_SetPwm(value);

  static uint8_t counter = 0;
  if (!(counter++ % 5))
  {
    PRINTF("%d\n", value);
  }
}

void RunTestApp(void)
{
  motor_A_init();
  while(1) {
    LED_BLUE_TOGGLE();
    delay();
    testMotor_A();
  }
}
