/*
 * cube.c
 *
 *  Created on: 04.04.2019
 *      Author: andre
 */


#include <stdbool.h>
#include "com.h"
#include "comLog.h"
#include "pi.h"
#include "comAck.h"
#include "McuUtility.h"
#include "string.h"
#include "pin_mux.h"
#include "fsl_ftm.h"
#include "ms_counter.h"
#include "VL53L0X.h"
#include "i2c.h"

/**
 * if range is smaller then this value, cube is detected
 */
#define CUBE_DISTANCE_THREASHOLD (10000)

static tAckHandler cubeAckHandler;
static tframeLineHandler cubeFrameHandler;

typedef enum {
  notFound,
  finding,
  found
} cubeState_t;

static cubeState_t cubeState = notFound;

/**
 * resends the frame for "cube detected"
 */
void cubeAckTimeoutHandler(void)
{
  //try to send frame again
  piWriteNum32s(CUBE_TOPIC, 1, &cubeAckHandler);
}

/**
 * tries to find the cube and performs a verification of 20 measurements after the fist detection
 */
void cubeDoWork(void)
{
  static int nbrOfPosVerifications = 0;
  static int nbrOfNegVerifications = 0;
  static int nbrOfVerifications = 0;

  uint16_t range_mm = VL53L0X_readRangeContinuousMillimeters();
#if TEST
  static int i_test = 0;
  i_test++;
  if (i_test > 10)
  {
    i_test = 0;
    piWriteNum32u("Tof distance", range_mm, NULL);

    switch (cubeState)
    {
      case notFound:
        LOG_INFO("CubeState: notFound");
        break;

      case finding:
        LOG_INFO("CubeState: finding");
        break;

      case found:
        LOG_INFO("CubeState: found");
        break;
    }
  }
#endif

  switch (cubeState)
  {
    case notFound:
      if (range_mm < CUBE_DISTANCE_THREASHOLD)
      {
        cubeState = finding;
        LOG_INFO("Cube fist time detected, starting verification");
      }
      break;

    case finding:

      nbrOfVerifications++;
      if (range_mm < CUBE_DISTANCE_THREASHOLD) nbrOfPosVerifications++;
      else nbrOfNegVerifications++;

      if (nbrOfVerifications > 20)
      {
        if (nbrOfPosVerifications > 15)
        {
          cubeState = found;
          piWriteNum32s(CUBE_TOPIC, 1, &cubeAckHandler);
        }
        else
        {
          if (nbrOfPosVerifications < nbrOfNegVerifications)
          {
            cubeState = notFound;
            LOG_CRITICAL("verification negative --> aborting finding, back to not found");
          }
          else
          {
            LOG_CRITICAL("verification ambiguous --> restart verification");
          }

          nbrOfVerifications = 0;
          nbrOfPosVerifications = 0;
          nbrOfNegVerifications = 0;
        }
      }

      break;

    case found:
      /* nothing to do */
    break;
  }
}

/**
 * Handles frames to manipulate the cube module
 * send 42 to reset the state to notFound
 */
tError cubeFrameHander (const unsigned char *value)
{
  uint32_t iVal = 0;
  McuUtility_ScanDecimal32uNumber(&value, &iVal);

  if (iVal = 42)
  {
    cubeState = notFound;
    LOG_INFO("Resetting cube state to not found");
  }

  ackSend(&cubeAckHandler);
}


void cubeReset(void)
{
  cubeFrameHander("42");
}


/**
 * Initializes the cube module and the i2c necessary for it.
 */
void cube_Init(void)
{
  i2cInit();
  ms_Counter_Init();

  VL53L0X_Constructor();
  VL53L0X_init(true);
  VL53L0X_setTimeout(5*20);
  VL53L0X_startContinuous(0);

  strncpy(cubeAckHandler.topic, CUBE_TOPIC, sizeof(cubeAckHandler.topic));
  cubeAckHandler.timeoutHandler = cubeAckTimeoutHandler;

  piRegisterFrameLineHandler(&cubeFrameHandler, CUBE_TOPIC, "frames to manipulate the cube detection", cubeFrameHander, &cubeAckHandler);
}
