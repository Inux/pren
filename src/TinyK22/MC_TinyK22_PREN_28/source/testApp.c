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
  ack_Init();
  drive_Init();

  strncpy(test_ackh.topic, testTopic, sizeof(test_ackh.topic));
  test_ackh.timeoutHandler = TestAckTimeoutHandler;

  strncpy(led_ackh.topic, ledTopic, sizeof(led_ackh.topic));

  piRegisterFrameLineHandler(&flh, testTopic, "Just someting to test", TestCommandHander, &test_ackh);
  piRegisterFrameLineHandler(&led_flh, ledTopic, "turn it on", LedCommandHander, &led_ackh);

  LOG_INFO("TinyK22 PREN Team 28... ready in TEST Mode");

  while(1) {
    McuWait_Waitms(1);
    //testMotor_A();

    m++;
    if (m > 25)
    {
      m = 0;
      driveToWork();
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

    j++;
    if (j > 30*100)
    {
      j = 0;
      //piWriteString(testTopic, "Test message please ack with 'ack,test'", &test_ackh);
    }
  }
}
