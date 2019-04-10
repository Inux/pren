/*
 * cube.c
 *
 *  Created on: 04.04.2019
 *      Author: andre
 */


#include "com.h"
#include "pi.h"
#include "comAck.h"
#include "McuUtility.h"
#include "string.h"

static tAckHandler cubeAckHandler;
static tframeLineHandler cubeFrameHandler;


void cubeAckTimeoutHandler(void)
{
  //todo try to send frame again
}

void cube_Init(void)
{
  strncpy(cubeAckHandler.topic, CUBE_TOPIC, sizeof(cubeAckHandler.topic));
  cubeAckHandler.timeoutHandler = cubeAckTimeoutHandler;
  ackRegisterHandler(&cubeAckHandler);
}
