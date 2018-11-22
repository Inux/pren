/**
 *--------------------------------------------------------------------\n
 *          HSLU T&A Hochschule Luzern Technik+Architektur            \n
 *--------------------------------------------------------------------\n
 *
 * \brief         quadrature decoder
 * \file
 * \author        Christian Jost, christian.jost@hslu.ch
 * \date          03.04.20018
 *
 * $Id: quad.c 116 2018-05-11 14:30:59Z zajost $
 *
 *--------------------------------------------------------------------
 */

#include <string.h>
#include "platform.h"
#include "quad.h"
#include "util.h"
#include "term.h"

#define ERR 5

#define FTM_CLOCK                 250000    // 250 kHz
#define FTM_PRESCALE              1         // div 1
#define WHEEL_DIAMETER            19.2      // 19.2 mm
#define TICKS_PER_REVOLUTION      142       // 142 ticks per wheel revolution

#define PERIODS_PER_REVOLUTION    (TICKS_PER_REVOLUTION / 4.0)                                      // 35.50 periods/revolution
#define WHEEL_CIRCUMFERENCE       (WHEEL_DIAMETER * 3.141593)                                       // 60.32 mm
#define UM_PER_TICK               (((10000.0 * WHEEL_CIRCUMFERENCE / TICKS_PER_REVOLUTION)+5)/10)   // 424.788 => 425 Micrometer/Ticks

// velocity  = (19.2mm * PI * 250'000 * 4) / (142 * Ticks) = (19.2mm * PI * 250'000) / (35.5 * Ticks) = 424779/Ticks
#define VELOCITY_PER_PERIOD       ((((uint32_t)(10 * WHEEL_CIRCUMFERENCE * FTM_CLOCK)) / (PERIODS_PER_REVOLUTION * FTM_PRESCALE)+5)/10) // =424779 430847

#define QuadLeftA                 ((GPIOA_PDIR & (1<<13)) != 0) // FTM1_CH1
#define QuadLeftB                 ((GPIOA_PDIR & (1<<12)) != 0) // FTM1_CH0
#define QuadRightA                ((GPIOB_PDIR & (1<<18)) != 0) // FTM2_CH1
#define QuadRightB                ((GPIOB_PDIR & (1<<19)) != 0) // FTM2_CH0
//#define QuadLeftA               (BITBAND_REG8(GPIOA_PDIR, 13))
//#define QuadLeftB               (BITBAND_REG8(GPIOA_PDIR, 12))


static const int8_t quadTable[16] =
{       // prev  new
        //  AB -> AB+
  ERR,  //  00    00
  -1,   //  00    01
  +1,   //  00    10
  ERR,  //  00    11

  +1,   //  01    00
  ERR,  //  01    01
  ERR,  //  01    10
  -1,   //  01    11

  -1,   //  10    00
  ERR,  //  10    01
  ERR,  //  10    10
  +1,   //  10    11

  ERR,  //  11    00
  +1,   //  11    01
  -1,   //  11    10
  ERR,  //  11    11
};


static int32_t ticksLeft;
static uint8_t errorLeft;

static int32_t ticksRight;
static uint8_t errorRight;
static int32_t timeRight;

static tCommandLineHandler clh;                       // terminal command line handler


//uint16_t times[256];
//uint8_t index;
//
//int32_t speed[256];
//uint8_t i;

/**
 * Interrupt service routine handles the
 * right quadrature decoder
 */
void FTM2_IRQHandler(void)
{
  static uint8_t bits = 0;
  static bool risingOkB = FALSE, fallingOkB = FALSE;
  static bool risingOkA = FALSE, fallingOkA = FALSE;
  static uint32_t risingB, fallingB;
  static uint32_t risingA, fallingA;
  static bool init = TRUE;
  int8_t quadValue;
  uint16_t chValue;
  uint32_t time=0;
  OnEnterQuadRightISR();

  if (FTM2_SC & FTM_SC_TOF_MASK) {
    FTM2_SC &= ~FTM_SC_TOF_MASK;
    risingOkB = fallingOkB = FALSE;
    risingOkA = fallingOkA = FALSE;
  }
  else {
    bits <<= 1;
    bits |= QuadRightA;
    bits <<= 1;
    bits |= QuadRightB;

    if (init) init = FALSE;
    else {
      quadValue = quadTable[bits & 0x0F];
      if (quadValue != ERR) ticksRight -= quadValue;
      else if (errorRight < 255) errorRight++;
    }
  }

  if (FTM2_C0SC & FTM_CnSC_CHF_MASK) chValue = FTM2_C0V;
  if (FTM2_C1SC & FTM_CnSC_CHF_MASK) chValue = FTM2_C1V;

  risingB += chValue;
  fallingB += chValue;
  risingA += chValue;
  fallingA += chValue;

  if (FTM2_C0SC & FTM_CnSC_CHF_MASK) {
    FTM2_C0SC &= ~FTM_CnSC_CHF_MASK;
    if (QuadRightB) {
      if (risingOkB) time = risingB;
      risingB = 0;
      risingOkB = TRUE;
    }
    else {
      if (fallingOkB) time = fallingB;
      fallingB = 0;
      fallingOkB = TRUE;
    }
  }

  if (FTM2_C1SC & FTM_CnSC_CHF_MASK) {
    FTM2_C1SC &= ~FTM_CnSC_CHF_MASK;
    if (QuadRightA) {
      if (risingOkA) time = risingA;
      risingA = 0;
      risingOkA = TRUE;
    }
    else {
      if (fallingOkA) time = fallingA;
      fallingA = 0;
      fallingOkA = TRUE;
    }
  }
  timeRight = (quadValue > 0) ? -time : time;
  OnExitQuadRightISR();
}

/**
 * Returns the velocity of the right wheel
 * @return
 *   the distance in mm
 */
int16_t quadGetSpeedRight(void)
{
  if (timeRight) return (int16_t)(((int32_t)VELOCITY_PER_PERIOD) / timeRight);
  else return 0;
}

/**
 * Returns the distance the right wheel has covered
 * @return
 *   the distance in mm
 */
int16_t quadGetDistanceRight(void)
{
   return (int16_t)((ticksRight * UM_PER_TICK) / 1000);
}


/**
 * Command line parser for this file.
 * This code is complete and works.
 *
 * @param[in] cmd
 *   the command to parse
 */
tError quadParseCommand(const unsigned char *cmd)
{
  tError result = EC_INVALID_ARG;
  if (strcmp(cmd, "help") == 0)
  {
    termWriteLine("q (quad) commands:");
    termWriteLine("  help");
    termWriteLine("  status");
    termWriteLine("  reset");
    result = EC_SUCCESS;
  }
  else if (strncmp(cmd, "status", sizeof("status")-1) == 0)
  {
    termWriteLine("quad status:");
    termWrite("L:");
    termWriteNum32s(ticksLeft);
    termWrite(" ");
    termWriteNum16s(quadGetDistanceLeft());
    termWrite(" ");
    termWriteNum16s(quadGetSpeedLeft());
    termWriteLine("");

    termWrite("R:");
    termWriteNum32s(ticksRight);
    termWrite(" ");
    termWriteNum16s(quadGetDistanceRight());
    termWrite(" ");
    termWriteNum16s(quadGetSpeedRight());
    termWrite("\n");
    result = EC_SUCCESS;
  }
  else if (strncmp(cmd, "reset", sizeof("reset")-1) == 0)
  {
    cmd += sizeof("reset");
    ticksLeft = ticksRight = errorLeft = errorRight = 0;
    termWriteLine("OK");
    result = EC_SUCCESS;
  }
  return result;
}


/**
 * Initializes the quadrature signal decoder:
 * - Hallsensor motor left
 *   A: PTA13, FTM1_QD_PHB Mux:3 (7)
 *   B: PTA12, FTM1_QD_PHA Mux:3 (7)
 *
 * - Hallsensor motor right
 *   A: PTB18, FTM2_QD_PHA Mux:3 (6)
 *   B: PTB19, FTM2_QD_PHB Mux:3 (6)
 */
void quadInit(void)
{
  PORTB_PCR18 = PORT_PCR_MUX(3) | PORT_PCR_PE(1) | PORT_PCR_PS(1);
  PORTB_PCR19 = PORT_PCR_MUX(3) | PORT_PCR_PE(1) | PORT_PCR_PS(1);

  // set clockgating for FTM2
  SIM_SCGC6 |= SIM_SCGC6_FTM2_MASK;

  // configure the timer with "Fixed frequency clock" as clocksource and with a "Prescaler" of 0 => 250'000 kHz
  FTM2_SC = FTM_SC_CLKS(2) |  FTM_SC_PS(0) | FTM_SC_TOIE(1);

  // Enable FTM2 interrupt on NVIC with Prio: PRIO_FTM2 (defined in platform.h)

  NVIC_SetPriority(FTM2_IRQn, PRIO_FTM2);       // set interrupt priority
  NVIC_EnableIRQ(FTM2_IRQn);                    // enable interrupt

  // configure channels as input capture
  FTM2_C0SC = FTM_CnSC_CHIE(1) | FTM_CnSC_MSx(0) | FTM_CnSC_ELSx(3) | FTM_CnSC_ICRST(1);
  FTM2_C1SC = FTM_CnSC_CHIE(1) | FTM_CnSC_MSx(0) | FTM_CnSC_ELSx(3) | FTM_CnSC_ICRST(1);

  // register terminal command line handler
  termRegisterCommandLineHandler(&clh, "q", "(quad)", quadParseCommand);
}
