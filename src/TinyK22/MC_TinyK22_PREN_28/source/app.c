/*
 * app.c
 *
 *  Created on: 07.03.2019
 *      Author: andre
 */

#include "app.h"
#include "McuWait.h"
#include "comAck.h"

void ack_main()
{
  static i = 0;
  i++;
  if (i < 50)
  {
    ackCheckQueue();
  }
}

void pi_main()
{
  static i = 0;
  i++;
  if (i < 10)
  {
    piDoWork();
  }
}

void RunApp(void)
{
  McuWait_Init();
  pi_init();
  ack_init();

  while (1)
  {
    McuWait_Waitms(1);
    pi_main();
    ack_main();
  }
}
