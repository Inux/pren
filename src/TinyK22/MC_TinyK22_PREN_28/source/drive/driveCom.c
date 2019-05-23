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
static tAckHandler isSpeedAckH;
static tAckHandler setSpeedAckH;

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
    ackSend(&setSpeedAckH);
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
#if SEND_IS_SPEED
  piWriteNum32s(IS_SPEED_TOPIC, isSpeed, &isSpeedAckH);
#endif
}

void driveComAckTimeoutHandler(void)
{
 if (isSpeedAckH.nbrOfRetries < 10)
 {
   //It'll be alright, just be patient
   isSpeedAckH.nbrOfRetries++;
 }
 else
 {
   //driveSetSpeed(0); todo add this back in
   LOG_CRITICAL("no speed ack afer 500ms. stop the train");
   isSpeedAckH.nbrOfRetries=0;

 }
}

void driveCom_Init()
{
  strncpy(setSpeedAckH.topic, SPEED_TOPIC, sizeof(setSpeedAckH.topic));
  isSpeedAckH.timeoutHandler = NULL;
  piRegisterFrameLineHandler(&flh, SPEED_TOPIC, "sets the speed", driveHandleSpeedFrame, &setSpeedAckH);

  strncpy(isSpeedAckH.topic, IS_SPEED_TOPIC, sizeof(isSpeedAckH.topic));
  isSpeedAckH.timeoutHandler = driveComAckTimeoutHandler;
  ackRegisterHandler(&isSpeedAckH);

#if TEST
  piRegisterFrameLineHandler(&flh_kp, "kp", "sets the kp", driveHandleKpFrame, NULL);
  piRegisterFrameLineHandler(&flh_ki, "ki", "sets the ki", driveHandleKiFrame, NULL);
#endif
}
