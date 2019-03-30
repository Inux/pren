/*
 * driveCom.c
 *
 *  Created on: 29.03.2019
 *      Author: andre
 */

#include "drive.h"
#include "pi.h"
#include "comAck.h"
#include "comLog.h"
#include "com.h"
#include "McuUtility.h"
#include "McuLib.h"
#include "quad.h"

static tframeLineHandler flh;
static tframeLineHandler flh_ki;
static tframeLineHandler flh_kp;
static tAckHandler ackH;

tError driveHandleKpFrame(const unsigned char *frameValue)
{
  int32_t kp = 0;
  uint8_t error = McuUtility_ScanDecimal32sNumber(&frameValue, &kp);
  if (error == ERR_OK)
  {
    driveSetKp(kp);
  }
  else
  {
    LOG_ERROR("Invalid Kp received");
    return EC_INVALID_ARG;
  }

  return EC_SUCCESS;
}

tError driveHandleKiFrame(const unsigned char *frameValue)
{
  int32_t ki = 0;
  uint8_t error = McuUtility_ScanDecimal32sNumber(&frameValue, &ki);
  if (error == ERR_OK)
  {
    driveSetKi(ki);
  }
  else
  {
    LOG_ERROR("Invalid Ki received");
    return EC_INVALID_ARG;
  }

  return EC_SUCCESS;
}

tError driveHandleSpeedFrame(const unsigned char *frameValue)
{
  int32_t speed = 0;
  uint8_t error = McuUtility_ScanDecimal32sNumber(&frameValue, &speed);
  if (error == ERR_OK)
  {
    driveSetSpeed(speed);
    ackSend(&ackH);
  }
  else
  {
    LOG_ERROR("Invalid Speed received");
    return EC_INVALID_ARG;
  }

  return EC_SUCCESS;
}

void driveSendSpeedUpdate(int32_t isSpeed)
{
  // todo make sure direction is in there
  piWriteNum32s(IS_SPEED_TOPIC, isSpeed, NULL); //todo add ack for this
}

void driveCom_Init()
{
  strncpy(ackH.topic, SPEED_TOPIC, sizeof(ackH.topic));
  ackH.timeoutHandler = NULL;
  piRegisterFrameLineHandler(&flh, SPEED_TOPIC, "sets the speed", driveHandleSpeedFrame, &ackH);

  piRegisterFrameLineHandler(&flh_kp, "kp", "sets the kp", driveHandleKpFrame, NULL);
  piRegisterFrameLineHandler(&flh_ki, "ki", "sets the ki", driveHandleKiFrame, NULL);
}
