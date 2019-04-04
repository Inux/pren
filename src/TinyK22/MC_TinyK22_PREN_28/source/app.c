/*
 * app.c
 *
 *  Created on: 07.03.2019
 *      Author: andre
 */

#include "crane.h"
#include "cubeDetection.h"
#include "app.h"
#include "McuWait.h"
#include "comAck.h"
#include "pi.h"
#include "drive.h"
#include "phase.h"
#include "comLog.h"

void ack_main()
{
  static int i = 0;
  i++;
  if (i < 50)
  {
    ackCheckQueue();
  }
}

void pi_main()
{
  static int i = 0;
  i++;
  if (i < 10)
  {
    piDoWork();
  }
}

void drive_main()
{
  static int i = 0;
  i++;
  if (i < DELTA_T_MS)
  {
    driveToWork();
  }
}

void RunApp(void)
{
  McuWait_Init();
  pi_Init();
  ack_Init();
  drive_Init();
  phase_Init();
  crane_Init();
  cube_Init();

  LOG_INFO("TinyK22 PREN Team 28... ready");

  while (1)
  {
    McuWait_Waitms(1);
    pi_main();
    ack_main();
    drive_main();
  }
}
