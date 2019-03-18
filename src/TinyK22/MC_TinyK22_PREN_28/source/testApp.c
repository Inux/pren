/*
 * testApp.c
 *
 *  Created on: 07.03.2019
 *      Author: andre
 */

#include <stdint.h>
#include "fsl_debug_console.h"
#include <stdio.h>
#include <stdint.h>
#include "board.h"
#include "motor_A.h"
#include "pi.h"
#include "McuWait.h"
#include "McuUtility.h"


void testMotor_A() // TODO: Remove, ugly
{
  static int8_t value;
  static int8_t step = 1;

  const int maxValue = 50;

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
    //PRINTF("%d\n", value);
  }
}

static tframeLineHandler flh;       // terminal command line handler
char *testTopic = "test";

tError TestCommandHander(const unsigned char *frameValue)
{
  piWriteString(testTopic, frameValue);
}

static tframeLineHandler led_flh;       // terminal command line handler
char *ledTopic = "led";

tError LedCommandHander(const unsigned char *frameValue)
{
  int32_t val = -1;
  McuUtility_ScanDecimal32sNumber(&frameValue, &val);
  if (val == 1)
  {
    LED_BLUE_ON();
  }
  else if (val == 0)
  {
    LED_BLUE_OFF();
  }
}

void RunTestApp(void)
{
  motor_A_init();
  //motor_A_SetPwm(15);
  McuWait_Init();
  pi_init();
  piRegisterFrameLineHandler(&flh, testTopic, "Just someting to test", TestCommandHander);
  piRegisterFrameLineHandler(&led_flh, ledTopic, "turn it on", LedCommandHander);

  while(1) {
    McuWait_Waitms(100);
    //testMotor_A();
    piDoWork();
  }
}
