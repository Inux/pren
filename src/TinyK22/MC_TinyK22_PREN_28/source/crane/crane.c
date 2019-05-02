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
#include "fsl_ftm.h"
#include "pin_mux.h"
#include "peripherals.h"
#include "crane.h"
#include "quad.h"

#define MOTOR_S_MAX_VALUE   (100000/4)

#define TICK_PER_REV        (512*21)
#define ANGLE_TO_DRIVE      (180)
#define TICKS_TO_DRIVE      (5435-25)
                            //(TICK_PER_REV*ANGLE_TO_DRIVE/360)

static tAckHandler craneAckHandler;
static tframeLineHandler craneFrameHandler;

static uint32_t targetPos;
static uint16_t kp, ki, kd;
static uint32_t val;


static void motor_A_UpdatePwmDutyCycle(uint32_t value)
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
  //todo check for timeout and let it be if timeout expires
  truePos = Encoder_S_GetNbrOfTicks();

  if (truePos >= targetPos)
  {
    //destination reached
    //reset controler to original state
    motor_A_UpdatePwmDutyCycle(0);
    targetPos = 0;
    setPos = 0;
    oldError = 0;
    intError = 0;
    ctrl_i = 0;
    return; //todo this is not nice
  }

  if (targetPos > setPos)
  {
    setPos += 40;
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
    currentError = (setPos-truePos);
  }

  // calculate Controller
  ctrl_p = kp*currentError;
  intError += currentError;
  ctrl_i = ki*intError;
  ctrl_d = kd*(currentError - oldError);
  oldError = currentError;

  val = ctrl_p + ctrl_i + ctrl_d;

  val /= 1; //scaling done by widening range of SetPwm

  if (val > MOTOR_S_MAX_VALUE)
  {
    val = MOTOR_S_MAX_VALUE;
    intError -= currentError;
  }
  else if  (val < 0)
  {
    val = 0;
    intError += currentError;
  }


  motor_A_UpdatePwmDutyCycle(val);

#if TEST
  piWriteNum32s("motor_S_SetValue", val, NULL); //todo clean
#endif
}

tError craneFrameLineHandler(unsigned char *value)
{
  // todo implement some stuff here
  // todo implement the correct stuff here
  uint32_t motVal = 0;
  McuUtility_ScanDecimal32uNumber(&value, &motVal);

  if (motVal > MOTOR_S_MAX_VALUE) motVal = MOTOR_S_MAX_VALUE;

  //motor_A_UpdatePwmDutyCycle(motVal);
  Encoder_S_StartCountingTicks();
  targetPos = TICKS_TO_DRIVE;


  ackSend(&craneAckHandler);

  return EC_SUCCESS;
}

void crane_Init(void)
{
  kp = 15;
  ki = 1;
  kd = 0;
  targetPos = 0;

  Motor_S_InitPins();
  motor_A_UpdatePwmDutyCycle(0);
  Encoder_S_StartCountingTicks();


  strncpy(craneAckHandler.topic, CRANE_TOPIC, sizeof(craneAckHandler.topic));
  craneAckHandler.timeoutHandler = NULL;
  piRegisterFrameLineHandler(&craneFrameHandler, CRANE_TOPIC, "", craneFrameLineHandler, &craneAckHandler);
}
