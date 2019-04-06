/*
 * phase.c
 *
 *  Created on: 04.04.2019
 *      Author: andre
 */


#include "com.h"
#include "pi.h"
#include "comAck.h"
#include "McuUtility.h"
#include "string.h"

static tAckHandler phaseAckHandler;
static tframeLineHandler phaseFrameHandler;

tError phaseFrameLineHandler(const unsigned char *value)
{
  // todo implement some stuff here
  ackSend(&phaseAckHandler);

  return EC_SUCCESS;
}

void phase_Init(void)
{
  strncpy(phaseAckHandler.topic, PHASE_TOPIC, sizeof(phaseAckHandler.topic));
  phaseAckHandler.timeoutHandler = NULL;
  piRegisterFrameLineHandler(&phaseFrameHandler, PHASE_TOPIC, "", phaseFrameLineHandler, &phaseAckHandler);
}

