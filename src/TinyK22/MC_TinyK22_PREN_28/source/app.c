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
  if (i > 50)
  {
    i = 0;
    ackCheckQueue();
  }
}

void pi_main()
{
  static int i = 0;
  i++;
  if (i > 10)
  {
    i = 0;
    piDoWork();
  }
}

void drive_main()
{
  static int i = 0;
  i++;
  if (i > DELTA_T_MS)
  {
    i = 0;
    driveToWork();
  }
}

void crane_main()
{
  static int i = 0;
  i++;
  if (i > 25)
  {
    i = 0;
    if (phase_GetPhase() == PH_grab_cube)
      craneDoWork();
  }
}

void cube_main()
{
  static int i = 0;
  i++;
  if (i > 50)
  {
    i = 0;
    if (phase_GetPhase() == PH_find_cube)
      cubeDoWork();
  }
}

void RunApp(void)
{
  McuWait_Init();
  pi_Init();
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
    crane_main();
    cube_main();
  }
}
