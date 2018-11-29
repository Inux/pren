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

void VL53L0x_Main()
{
  static uint32_t count = 0;
  count++;
  if (count >= TOFS_MS(1000))
  {
    char buf[128];
    buf[0] = '\0';
    utilStrcat(buf, sizeof(buf), "dist: ");
    utilStrcatNum32u(buf, sizeof(buf), (uint32_t) VL53L0X_readRangeContinuousMillimeters());
    utilStrcat(buf, sizeof(buf), "mm;");
    termWriteLine(buf);
    termWriteChar('\n');
    termWriteNum32s(millis());
    termWriteChar('\n');
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

  ftm1Init();                         // init flex timer 1
  termInit(57600);                    // init terminal with a baudrate of 57600
  hcsr04Init();
  driveInit();
  motorInit();
//  quadInit();
  i2cInit();
  VL53L0X_Constructor();
  VL53L0X_init(true);
  //VL53L0X_setTimeout(500);
  VL53L0X_io_timeout = 5; //todo correct
  VL53L0X_startContinuous(0);


  GPIOC_PDDR |= 1 << 2; // Set port direction of the blue Led on tinyK22 as output
  PORTC_PCR2 = PORT_PCR_MUX(1);    // configure port mux of the blue led to GPIO

  while (TRUE)
  {
    if (FTM1_SC & FTM_SC_TOF_MASK)    // check for timer overflow
    {
      FTM1_SC &= ~FTM_SC_TOF_MASK;    // overflow occurred => clear TOF flag

      //hcsr04();
      VL53L0x_Main();
      //drive();
      term();

    }
  }
}
