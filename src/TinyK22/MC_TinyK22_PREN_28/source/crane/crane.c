/*
 * crane.c
 *
 *  Created on: 04.04.2019
 *      Author: andre
 */

#include "com.h"
#include "pi.h"
#include "comAck.h"
#include "McuUtility.h"
#include "string.h"

static tAckHandler craneAckHandler;
static tframeLineHandler craneFrameHandler;

tError craneFrameLineHandler(unsigned char *value)
{
  // todo implement some stuff here
  ackSend(&craneAckHandler);

  return EC_SUCCESS;
}

void crane_Init(void)
{
  strncpy(craneAckHandler.topic, CRANE_TOPIC, sizeof(craneAckHandler.topic));
  craneAckHandler.timeoutHandler = NULL;
  piRegisterFrameLineHandler(&craneFrameHandler, CRANE_TOPIC, "", craneFrameLineHandler, &craneAckHandler);
}
