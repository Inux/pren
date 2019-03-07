/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         Exercise 13 - Luxmeter
 * \file
 * \author        Andreas Rebsamen
 * \date          15.11.2018
 *
 *--------------------------------------------------------------------
 */

#include <ftm1.h>
#include "platform.h"
#include "ftm0.h"
#include "term.h"
#include "i2c.h"
#include "adc.h"
#include "util.h"
#include "HCSR04.h"
#include "drive.h"
#include "motor.h"
#include "VL53L0X.h"
#include "VL6180X.h"
#include "ftm2.h"

// calulates the nr of TOF count for a given number of milliseconds
#define TOFS_MS(x)   ((uint16_t)(((FTM1_CLOCK / 1000) * x) / (FTM1_MODULO + 1)))

void hcsr04()
{
  static uint32_t count = 0;
  count++;
  if (count >= TOFS_MS(1000))
  {
    count = 0;
    hcsr04PrintCurrentStatus();
  }
}

void VL6180x_Main()
{
  static int count = 0;

  if (count++ > TOFS_MS(1000))
  {
    count = 0;
    uint8_t range_data[1];
    range_data[0] = 0;
    tError result = proxSensRange(range_data);

    if (result == EC_SUCCESS)
    {
      char buf[128];
      buf[0]='\0';
      utilStrcat(buf, sizeof(buf), "6180_dist: ");
      utilStrcatNum32u(buf, sizeof(buf), (uint32_t) (((float)range_data[0]*600)/255));
      utilStrcat(buf, sizeof(buf), "mm;");
      termWriteLine(buf);
    }
    else
    {
      termWriteLine("Range NOT ok");
    }
  }
}

void VL53L0x_Main()
{
  static uint32_t count = 0;
  count++;
  if (count >= TOFS_MS(1000))
  {
    uint16_t range_mm = VL53L0X_readRangeContinuousMillimeters()/10;

    count = 0;
    char buf[128];
    buf[0] = '\0';
    utilStrcat(buf, sizeof(buf), "53L0_dist: ");
    utilStrcatNum16u(buf, sizeof(buf),  range_mm);
    utilStrcat(buf, sizeof(buf), "mm;");
    termWriteLine(buf);
  }
}

void drive()
{
  static uint32_t count = 0;
  count++;
  if (count >= TOFS_MS(25))
  {
    count = 0;
    driveToWork();
  }
}

void ImpulsCounterMain()
{
  static uint32_t count = 0;
  count++;
  if (count >= TOFS_MS(500))
  {
    count = 0;
    uint32_t impulses = ftm2GetNbrOfImpulses();
    uint32_t revMin = ftm2GetRevMin();
    uint32_t speed = ((float)revMin/60)*22*3.14159;

    char buf[128];
    buf[0] = '\0';
    utilStrcat(buf, sizeof(buf), "Impulses: ");
    utilStrcatNum32u(buf, sizeof(buf),  impulses);
    utilStrcat(buf, sizeof(buf), "   N: ");
    utilStrcatNum32u(buf, sizeof(buf),  revMin);
    utilStrcat(buf, sizeof(buf), "min^(-1)   speed: ");
    utilStrcatNum32u(buf, sizeof(buf),  speed);
    utilStrcat(buf, sizeof(buf), "mm/s");
    termWriteLine(buf);
  }
}

void term()
{
  static uint32_t count = 0;
  count++;
  if (count >= TOFS_MS(10))
  {
    count = 0;
    termDoWork();
  }
}

/**
 * The main function
 */
void main(void)
{
  char buf[128];

  ftm1Init();
  ftm2Init();
  termInit(57600);                    // init terminal with a baudrate of 57600
//  hcsr04Init();
  driveInit();
  motorInit();
//  quadInit();
//  i2cInit();

//  VL53L0X_Constructor();
//  VL53L0X_init(true);
//  VL53L0X_setTimeout(500);
//  VL53L0X_io_timeout = 5; //todo correct
//  VL53L0X_startContinuous(0);

//  VL6180X_init();


  GPIOC_PDDR |= 1 << 2; // Set port direction of the blue Led on tinyK22 as output
  PORTC_PCR2 = PORT_PCR_MUX(1);    // configure port mux of the blue led to GPIO

  GPIOC_PDDR |= 1<<8;                 // Test pin for encoder performace mesurement
  PORTC_PCR8 = PORT_PCR_MUX(1);

  while (TRUE)
  {
    if (FTM1_SC & FTM_SC_TOF_MASK)    // check for timer overflow
    {
      FTM1_SC &= ~FTM_SC_TOF_MASK;    // overflow occurred => clear TOF flag

      //hcsr04();
      //VL53L0x_Main();
      //drive();
      term();
//      VL6180x_Main();

      ImpulsCounterMain();

    }
  }
}
