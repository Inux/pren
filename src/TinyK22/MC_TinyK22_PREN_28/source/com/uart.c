/*
 * uart.c
 *
 *  Created on: 14.03.2019
 *      Author: andre
 */

#include <stdbool.h>

#include "com.h"
#include "fsl_uart.h"
#include "peripherals.h"
#include "pin_mux.h"
#include "board.h"

#define UART_CLK_FREQ CLOCK_GetFreq(SYS_CLK)


/**
 * the receive queue of this driver, implemented as ring buffer
 */
static char rxBuf[COM_RX_BUF_SIZE];
static volatile uint16_t rxBufCount;
static uint16_t rxBufWritePos;
static uint16_t rxBufReadPos;

/**
 * the transmit queue of this driver, implemented as ring buffer
 */
static char txBuf[COM_TX_BUF_SIZE];
static volatile uint16_t txBufCount;
static uint16_t txBufWritePos;
static uint16_t txBufReadPos;

/**
 * @brief UART Interrupt Service Routine
 * - Received bytes are stored in the queue rxBuf
 * - Bytes in the queue txBuf are sent
 */
void COM_UART_IRQHandler(void)
{
  //OnEnterUart1RxTxISR();
  uint8_t status = UART_GetStatusFlags(COM_UART);
  if (status & UART_S1_RDRF_MASK)
  {
    uint8_t data = UART_ReadByte(COM_UART);
    // store the received byte into receiver Queue (rxBuf)
    // ignore string terminating characters
    if (rxBufCount < COM_RX_BUF_SIZE && data != '\0')
    {
      if (data == '\r') data = '\n'; //todo ugly hack test with actual raspi software
      rxBuf[rxBufWritePos++] = data;
      rxBufCount++;
      if (rxBufWritePos == COM_RX_BUF_SIZE)
        rxBufWritePos = 0;
    }
  }

  if (status & UART_S1_TDRE_MASK)
  {
    if (txBufCount > 0)
    {
      // store bytes to send in tx buffer
      UART_WriteByte(COM_UART, txBuf[txBufReadPos++]);
      txBufCount--;
      if (txBufReadPos == COM_TX_BUF_SIZE)
        txBufReadPos = 0;
    }
    else
    {
      UART_DisableInterrupts(COM_UART, kUART_TxDataRegEmptyInterruptEnable);
    }
  }
  __DSB();
  //OnExitUart1RxTxISR();
}

/**
 * Writes one Byte in the transmit buffer.
 *
 * @details
 *   Switching on the TIE interrupt causes an interrupt to be
 *   triggered immediately. The function blocks until there is
 *   space in the txBuf queue.
 *
 * @param[in] ch
 *   the byte to send
 */
void uartWriteChar(char ch)
{
  while (txBufCount >= COM_TX_BUF_SIZE)
    ;
  txBuf[txBufWritePos++] = ch;
  if (txBufWritePos == COM_TX_BUF_SIZE)
    txBufWritePos = 0;
  NVIC_DisableIRQ(COM_UART_IRQn);
  txBufCount++;
  NVIC_EnableIRQ(COM_UART_IRQn);
  UART_EnableInterrupts(COM_UART, kUART_TxDataRegEmptyInterruptEnable);
}

/**
 * Writes a null terminated string in the send buffer. If the
 * string is null, the function returns immediately.
 *
 * @param[in] str
 *   the null terminated string to send
 */
void uartWrite(const char *str)
{
  if (str == NULL)
    return;
  while (*str != '\0')
    uartWriteChar(*str++);
}

/**
 * Writes a null terminated string in the send buffer. If the
 * string is null, only a new new line character is sent.
 *
 * @param[in] str
 *   the null terminated string to send
 */
void uartWriteLine(const char *str)
{
  uartWrite(str);
  uartWriteChar(NEW_LINE);
}

/**
 * Reads one char out of the rxBuf queue. The function blocks
 * until there is at least one byte in the queue.
 *
 * @return
 *   the received byte
 */
char uartReadChar(void)
{
  char ch;
  while (rxBufCount == 0)
    ;
  ch = rxBuf[rxBufReadPos++];
  if (rxBufReadPos == COM_RX_BUF_SIZE)
    rxBufReadPos = 0;
  NVIC_DisableIRQ(COM_UART_IRQn);
  rxBufCount--;
  NVIC_EnableIRQ(COM_UART_IRQn);
  return ch;
}

/**
 * Reads a null terminated string out of the rxBuf queue. The
 * function blocks until a new Line character has been received
 * or the length has been exceeded.
 *
 * @details
 *   the new line character will be replaced with a '\0' to
 *   terminate the string.
 *
 * @param[out] *str
 *   pointer to a char array to store the received string
 * @param[in] length
 *   the length of the str char array.
 * @returns
 *   the length of the received string.
 */
uint16_t uartReadLine(char *str, uint16_t length)
{
  uint16_t i;
  for (i = 1; i < length; i++)
  {
    *str = uartReadChar();
    if (*str == NEW_LINE)
    {
      *str = '\0';
      break;
    }
    str++;
  }
  return i;
}

/**
 * This functions checks, if there is a new line character
 * in the rxBuf queue.
 *
 * @returns
 *   TRUE, if there is a new line character, otherweise FALSE.
 */
bool uartHasLineReceived(void)
{
  uint16_t i;
  uint16_t index = rxBufReadPos;

  for (i = 0; i < rxBufCount; i++)
  {
    if (rxBuf[index++] == NEW_LINE)
      return true;
    if (index == COM_RX_BUF_SIZE)
      index = 0;
  }
  return false;
}

/**
 * \fn uint16_t uart1RxBufCount(void)
 * Returns the number of bytes in the receiver queue.
 *
 * @returns
 *   the number of bytes in the receiver queue.
 */
uint16_t uartRxBufCount(void)
{
  return rxBufCount;
}

/**
 * Error Interrupt Service Routine
 * Clears the error flags.
 */
/**
 * For DEBUG_UART
 */
void UART1_ERR_IRQHandler(void)
{
  (void) ((UART1)->S1);
  (void) ((UART1)->D);
}
/**
 * For PI_UART
 */
void UART0_ERR_IRQHandler(void)
{
  (void) ((UART0)->S1);
  (void) ((UART0)->D);
}

static void initPeriphery(UART_Type *base)
{
  uart_config_t config;

  /*
   * config.baudRate_Bps = 115200U;
   * config.parityMode = kUART_ParityDisabled;
   * config.stopBitCount = kUART_OneStopBit;
   * config.txFifoWatermark = 0;
   * config.rxFifoWatermark = 1;
   * config.enableTx = false;
   * config.enableRx = false;
   */
  UART_GetDefaultConfig(&config);
  config.baudRate_Bps = COM_UART_BAUDRATE;
  config.enableTx = true;
  config.enableRx = true;

  UART_Init(base, &config, UART_CLK_FREQ);
}

void uart_inti(void)
{
  txBufReadPos = txBufWritePos = txBufCount = 0;
  rxBufReadPos = rxBufWritePos = rxBufCount = 0;

  initPeriphery(COM_UART);
  UART_EnableInterrupts(COM_UART,
      kUART_RxDataRegFullInterruptEnable);// | kUART_RxOverrunInterruptEnable);
  EnableIRQ(COM_UART_IRQn);

#if USE_DEBUG_UART
    BOARD_InitDEBUG_UARTPins();
#else
    Pi_Init_UARTPins();
#endif
}
