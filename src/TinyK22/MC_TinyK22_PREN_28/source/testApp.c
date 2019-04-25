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
#include <string.h>
#include "board.h"
#include "motor_A.h"
#include "pi.h"
#include "McuWait.h"
#include "McuUtility.h"
#include "comAck.h"
#include "comLog.h"
#include "quad.h"
#include "fsl_ftm.h"
#include "peripherals.h"
#include "drive.h"
#include "driveCom.h"
#include "crane.h"

void Test_Motor_S(void)
{
  piWriteNum32s("craneTicks", (int32_t)Encoder_S_GetNbrOfTicks(), NULL);
}

void testMotor_A()
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

static tframeLineHandler flh;
char *testTopic = "test";
static tAckHandler test_ackh;

tError TestCommandHander(const unsigned char *frameValue)
{
  //piWriteString(testTopic, frameValue);

  Encoder_S_StartCountingTicks();
  ackSend(&test_ackh);

  return EC_SUCCESS;
}

void TestAckTimeoutHandler()
{
  LOG_INFO("timeout occurred ");
//  LOG_WARN("timeout occurred thats a waring");
//  LOG_CRITICAL("timeout occurred thats a critical thing");
//  LOG_ERROR("timeout occurred thats an error");
  test_ackh.outstanding = false;
}

static tframeLineHandler led_flh;
char *ledTopic = "led";
static tAckHandler led_ackh;

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

  ackSend(&led_ackh);

  return EC_SUCCESS;
}

void RunTestApp(void)
{
  int i = 0;
  int j = 0;
  int k = 0;
  int l = 0;
  int m = 0;

  McuWait_Init();
  pi_Init();
  drive_Init();
  crane_Init();

  strncpy(test_ackh.topic, testTopic, sizeof(test_ackh.topic));
  test_ackh.timeoutHandler = TestAckTimeoutHandler;

  strncpy(led_ackh.topic, ledTopic, sizeof(led_ackh.topic));

  piRegisterFrameLineHandler(&flh, testTopic, "Just someting to test", TestCommandHander, &test_ackh);
  piRegisterFrameLineHandler(&led_flh, ledTopic, "turn it on", LedCommandHander, &led_ackh);

  LOG_INFO("TinyK22 PREN Team 28... ready in TEST Mode");

  while(1) {
    McuWait_Waitms(1);

    j++;
    if (j > 100)
    {
      j = 0;
      Test_Motor_S();
    }

    l++;
    if (l > 25)
    {
      craneDoWork();
    }

    k++;
    if (k > 50)
    {
      k = 0;
      piDoWork();
    }

    i++;
    if (i > 50)
    {
      i = 0;
      ackCheckQueue();
    }
  }
}
