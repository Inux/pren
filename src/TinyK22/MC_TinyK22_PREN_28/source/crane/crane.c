/*
 * crane.c
 *
 *  Created on: 04.04.2019
 *      Author: andre
 */

#include "com.h"
#include "pi.h"
#include "comLog.h"
#include "comAck.h"
#include "McuUtility.h"
#include "string.h"
#include "fsl_ftm.h"
#include "pin_mux.h"
#include "peripherals.h"
#include "crane.h"
#include "quad.h"
#include <stdbool.h>
#include "cubeDetection.h"

#define MOTOR_S_MAX_VALUE   (100000/2)

#define TICK_PER_REV        (512*21)
#define ANGLE_TO_DRIVE      (180)
#define TICKS_TO_DRIVE      (5435+50)
                            //(TICK_PER_REV*ANGLE_TO_DRIVE/360)

#define TIMEOUT_VALUE       (10000/25)

static tAckHandler isCraneAckHandler;
static tAckHandler craneAckHandler;
static tframeLineHandler craneFrameHandler;

static uint32_t targetPos;
static uint16_t kp, ki, kd;
static uint32_t val;

static bool craneRetracting = false;
static bool craneDoneRetracted = false;
static int timeoutCounter = 0;

static void motor_S_UpdatePwmDutyCycle(uint32_t value)
{
  uint32_t mod = FTM_1_MOTOR_PWM_PERIPHERAL->MOD;
  uint32_t cnv = (mod * value) / MOTOR_S_MAX_VALUE;
  /* For 100% duty cycle */
  if (cnv >= mod)
  {
      cnv = mod + 1;
  }
  FTM_1_MOTOR_PWM_PERIPHERAL->CONTROLS[1].CnV = cnv;

//  FTM_UpdatePwmDutycycle(FTM_1_MOTOR_PWM_PERIPHERAL, 0, kFTM_EdgeAlignedPwm, value);
  FTM_SetSoftwareTrigger(FTM_1_MOTOR_PWM_PERIPHERAL, true);
}

static void doneRetractCrane(void)
{
  craneRetracting = false;
  craneDoneRetracted = true;

  piWriteNum32u(IS_CRANE_TOPIC, 1, &isCraneAckHandler);
}


void craneDoWork(void)
{
  static int16_t truePos = 0;
  static int16_t setPos = 0;
  static int oldError;
  static int intError;
  int ctrl_p;
  int ctrl_i = 0;
  int ctrl_d;
  int currentError;

  if (craneRetracting && timeoutCounter < TIMEOUT_VALUE)
  {
    timeoutCounter++;
    if (timeoutCounter >= TIMEOUT_VALUE)
    {
      //timeout reached
      //reset controler to original state
      motor_S_UpdatePwmDutyCycle(0);
      targetPos = 0;
      setPos = 0;
      oldError = 0;
      intError = 0;
      ctrl_i = 0;
      LOG_WARN("crane timeout occurred");
      doneRetractCrane();
      return; //todo this is not nice
    }

    truePos = Encoder_S_GetNbrOfTicks();

    if (truePos >= targetPos)
    {
      //destination reached
      //reset controler to original state
      motor_S_UpdatePwmDutyCycle(0);
      targetPos = 0;
      setPos = 0;
      oldError = 0;
      intError = 0;
      ctrl_i = 0;
      doneRetractCrane();
      return; //todo this is not nice, again
    }

    if (targetPos > setPos)
    {
      setPos += 50;
      if (targetPos < setPos)
        setPos = targetPos;
    }

    if (setPos < truePos)
    {
      currentError = 0;
      intError = 0;
    }
    else
    {
      currentError = (setPos - truePos);
    }

    // calculate Controller
    ctrl_p = kp * currentError;
    intError += currentError;
    ctrl_i = ki * intError;
    ctrl_d = kd * (currentError - oldError);
    oldError = currentError;

    val = ctrl_p + ctrl_i + ctrl_d;

    val /= 1; //scaling done by widening range of SetPwm

    if (val > MOTOR_S_MAX_VALUE)
    {
      val = MOTOR_S_MAX_VALUE;
      intError -= currentError;
    }
    else if (val < 0)
    {
      val = 0;
      intError += currentError;
    }

    motor_S_UpdatePwmDutyCycle(val);

#if TEST
    piWriteNum32s("motor_S_SetValue", val, NULL); //todo clean
#endif
  }
  else
  {
    motor_S_UpdatePwmDutyCycle(0);
  }
}

tError craneFrameLineHandler(const unsigned char *value)
{
  uint32_t iVal = 0;
  McuUtility_ScanDecimal32uNumber(&value, &iVal);

  if (iVal == 1 && !craneDoneRetracted && !craneRetracting)
  {
    Encoder_S_StartCountingTicks();
    targetPos = TICKS_TO_DRIVE;
    craneRetracting = true;
  }
  else if (iVal == 42)
  {
    cubeReset();

    if (!craneRetracting && craneDoneRetracted)
    {
      craneDoneRetracted = false;
      timeoutCounter = 0;
    }
  }

  ackSend(&craneAckHandler);

  return EC_SUCCESS;
}

void isCraneAckTimeoutHandler(void)
{
  piWriteNum32u(IS_CRANE_TOPIC, 1, &isCraneAckHandler);
}

void crane_Init(void)
{
  kp = 25;
  ki = 3;
  kd = 0;
  targetPos = 0;

  Motor_S_InitPins();
  motor_S_UpdatePwmDutyCycle(0);
  Encoder_S_StartCountingTicks();


  strncpy(craneAckHandler.topic, CRANE_TOPIC, sizeof(craneAckHandler.topic));
  craneAckHandler.timeoutHandler = NULL;
  piRegisterFrameLineHandler(&craneFrameHandler, CRANE_TOPIC, "", craneFrameLineHandler, &craneAckHandler);

  strncpy(isCraneAckHandler.topic, IS_CRANE_TOPIC, sizeof(isCraneAckHandler.topic));
  isCraneAckHandler.timeoutHandler = isCraneAckTimeoutHandler;
  ackRegisterHandler(&isCraneAckHandler);
}
