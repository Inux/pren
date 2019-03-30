/*
 * drive.c
 *
 *  Created on: 28.03.2019
 *      Author: andre
 */

#include "drive.h"
#include "quad.h"
#include "motor_A.h"
#include "driveCom.h"

static int32_t targetSpeed;
static int8_t targetDir = 1;
static uint8_t kp, ki, kd;
static int32_t val;

#define DELAT_T             25

/**
 * Sets the speed
 * @param[in] speed
 *   the speed in mm/sec
 */
void driveSetSpeed(int32_t speed)
{
  targetSpeed = speed;

  if (speed >= 0)
  {
    targetDir = 1;
  }
  else
  {
    targetDir = -1;
  }
}

void driveSetParameters(uint8_t KpR, uint8_t KiR)
{
  kp = KpR;
  ki = KiR;
}

void driveSetKp(uint8_t KpR)
{
  kp = KpR;
}

void driveSetKi(uint8_t KiR)
{
  ki = KiR;
}


/**
 * This function contains the PID closed loop controller
 * should be called every {delat_T} ms
 * accelerate and decelerate on average 1 (mm/s) per ms
 */
void driveToWork(void)
{
  static int16_t trueSpeed = 0;
  static int16_t setSpeed = 0;
  static int oldError;
  static int intError;
  int ctrl_p;
  int ctrl_i = 0;
  int ctrl_d;
  int currentError;

  trueSpeed = Encoder_A_GetAbsSpeed() *targetDir;

  if (targetSpeed > setSpeed)
  {                                        // accelerate
    setSpeed += DELAT_T;
    if (targetSpeed < setSpeed)
      setSpeed = targetSpeed;
  }
  if (targetSpeed < setSpeed)
  {                                        // decelerate
    setSpeed -= DELAT_T;
    if (targetSpeed > setSpeed)
      setSpeed = targetSpeed;
  }

  //dynamic parameters
  if (abs(setSpeed) < 1000)
  {
    kp = 13;
  }
  else
  {
    kp = 22;
  }


  currentError = (setSpeed-trueSpeed);
  // calculate Controller
  ctrl_p = kp*currentError;
  intError += currentError;
  ctrl_i = ki*intError;
  ctrl_d = kd*(currentError - oldError);
  oldError = currentError;

  val = ctrl_p + ctrl_i + ctrl_d;

  val /= 1; //scaling done by widening range of SetPwm

  if (val > MOTOR_MAX_VALUE && targetDir == 1)
  {
    val = MOTOR_MAX_VALUE;
    intError -= currentError;
  }
  else if  (val < -MOTOR_MAX_VALUE && targetDir == -1)
  {
    val = -MOTOR_MAX_VALUE;
    intError += currentError;
  }
  else if ((val < 0 && targetDir == 1) || (val > 0 && targetDir == -1)) //breaking
  {
    val = 0;
    intError = 0;
  }
  else if (targetSpeed == 0 && trueSpeed == 0)
  {
    val = 0;
    intError = 0;
  }

  motor_A_SetPwm(val);

  piWriteNum32s("motorSetValue", val, NULL); //todo clean

  static int updateCounter = 0;
  updateCounter++;
  if (updateCounter > 4)
  {
    driveSendSpeedUpdate(trueSpeed);
  }
}

/**
 * Initializes the drive components
 */
void driveInit(void)
{
  kp = 22;
  ki = 5;
  kd = 0;
  targetSpeed = 0;

  motor_A_init();
  Encoder_Init();
  driveCom_Init();
}

