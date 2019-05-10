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
#include "phase.h"

static tAckHandler phaseAckHandler;
static tframeLineHandler phaseFrameHandler;

static tPhase currentPhase = PH_startup;

tPhase phase_GetPhase(void)
{
  return currentPhase;
}

tError phaseFrameLineHandler(const unsigned char *value)
{
  int32_t iVal = 0;
  McuUtility_ScanDecimal32sNumber(&value, &iVal);
  currentPhase = (tPhase)iVal;

  ackSend(&phaseAckHandler);

  return EC_SUCCESS;
}

void phase_Init(void)
{
  strncpy(phaseAckHandler.topic, PHASE_TOPIC, sizeof(phaseAckHandler.topic));
  phaseAckHandler.timeoutHandler = NULL;
  piRegisterFrameLineHandler(&phaseFrameHandler, PHASE_TOPIC, "", phaseFrameLineHandler, &phaseAckHandler);
}

