/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         Drive with PID
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          04.04.20018
 *
 * $Id: drive.c 116 2018-05-11 14:30:59Z zajost $
 *
 *--------------------------------------------------------------------
 */

#include "platform.h"
#include "drive.h"
#include "quad.h"
#include "motor.h"

static int16_t setValue;
static uint8_t kp, ki, kd;
static int16_t integ, dev, devOld;
static int32_t val;


#define MAX_SPEED           50

//int16_t sl[256];
//int16_t sr[256];
//uint8_t sli, sri;




/**
 * Sets the speed
 * @param[in] speedL
 *   the speed of the left wheel in mm/sec
 * @param[in] speedR
 *   the speed of the right wheel in mm/sec
 */
void driveSetSpeed(int16_t speed)
{
  setValue = speed;
}


/**
 * This function sets the control parameters
 * @param[in] pKpR Kp 0..255
 * @param[in] pKiR Ki 0..255
 */
void driveSetParameters(uint8_t KpR, uint8_t KiR)
{
  kp = KpR;
  ki = KiR;
}

#define a 2000
/**
 * This function contains the PID closed loop controller
 */
void driveToWork(void)
{
  static int16_t speedRight = 0;
  static int16_t setValueR = 0;

  motorSetPwm(0);

  speedRight = ((speedRight * 1) + quadGetSpeedRight())/2;

  if (setValue > setValueR) {                                        // accelerate right wheel
    setValueR += (a/40);
    if (setValue < setValueR) setValueR = setValue;
  }
  if (setValue < setValueR) {                                        // decelerate right wheel
    setValueR -= (a/40);
    if (setValue > setValueR) setValueR = setValue;
  }
#if USE_PID
  motorSetPwm(setValueR);
#else
  if (setValueR)
  {
    dev = (setValueR - speedRight);      // calc deviation
    val = (kp * dev);                  // P-Part: (max kpX = 2000 * 255 = 510'000)
    if (ki) integ += dev;              // I-Part: with anti-windup below
    val += (ki * integ);
    val += (kd*(setValueR-devOld));    // D-Part
    devOld = setValueR;
    val /= 1000;                         // scaling

    // pre control
    // y=m*x+n => preControl = setValue*m + n | m=0.055, n=7
    val += (67 * setValueR) / 1000 + (setValueR > 0 ? 10 : -10);

    if (val > MOTOR_MAX_VALUE) {
      val = MOTOR_MAX_VALUE;
      integ -= dev;                     // anti wind-up
    }
    else if (val < -MOTOR_MAX_VALUE) {
      val = -MOTOR_MAX_VALUE;
      integ += dev;                     // anti wind-up
    }
  }
  else {
    val = integ = 0;
  }

//  sl[sli] = (uint8_t)valL;     // 100=18    500=45     11.25   0.0675
//  sr[sli++] = (uint8_t)valR;   // 100=16    500=42    9.5 0.065

  motorSetPwm((int8_t)val+0);
#endif
}



void driveInit(void)
{
  kp = 70;//80;
  ki = 20;//30;
  kd = 0;
  setValue = 00;  //30... 7sec 30m = 4cm/sec
}
