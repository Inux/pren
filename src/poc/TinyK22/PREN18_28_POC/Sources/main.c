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

#include "platform.h"
#include "ftm0.h"
#include "ftm3.h"
#include "term.h"
#include "i2c.h"
#include "adc.h"
#include "util.h"
#include "HCSR04.h"

// calulates the nr of TOF count for a given number of milliseconds
#define TOFS_MS(x)   ((uint16_t)(((FTM3_CLOCK / 1000) * x) / (FTM3_MODULO + 1)))

/**
 * The main function
 */
void main(void)
{
  uint32_t count = 0;
  char buf[128];

  ftm3Init();                         // init flex timer 3
  termInit(57600);                    // init terminal with a baudrate of 57600
  hcsr04Init();

  GPIOC_PDDR |= 1 << 2; // Set port direction of the blue Led on tinyK22 as output
  PORTC_PCR2 = PORT_PCR_MUX(1);    // configure port mux of the blue led to GPIO

  while (TRUE)
  {
    if (FTM3_SC & FTM_SC_TOF_MASK)    // check for timer overflow
    {
      FTM3_SC &= ~FTM_SC_TOF_MASK;    // overflow occurred => clear TOF flag

      count++;                        // count the number of TOF's
      if (count >= TOFS_MS(1000)) // check if number of TOF's is equal or greater 250ms
      {
        count = 0;
        hcsr04PrintCurrentStatus();
      }
    }
  }
}
