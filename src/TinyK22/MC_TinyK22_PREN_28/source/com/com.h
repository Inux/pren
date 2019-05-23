/*
 * com.h
 *
 *  Created on: 14.03.2019
 *      Author: andre
 */

#ifndef COM_COM_H_
#define COM_COM_H_

#include "fsl_uart.h"

#define NEW_LINE            '\n'
#define SEP_TOKEN           ","

#define COM_PI_TOPIC_MAX_LENGTH 16

#define SPEED_TOPIC     "speed"
#define CRANE_TOPIC     "crane"
#define IS_CRANE_TOPIC  "is_crane"
#define PHASE_TOPIC     "phase"
#define IS_SPEED_TOPIC  "is_speed"
#define CUBE_TOPIC      "cube"
#define CURRENT_TOPIC   "current"
#define LOG_TOPIC       "log"
#define ACK_TOPIC       "ack"

#define USE_DEBUG_UART      0
#define SEND_IS_SPEED       1

#define DEBUG_UART          UART1
#define PI_UART             UART0

#define DEBUG_UART_IRQn         UART1_RX_TX_IRQn
#define DEBUG_UART_IRQHandler   UART1_RX_TX_IRQHandler

#define PI_UART_IRQn            UART0_RX_TX_IRQn
#define PI_UART_IRQHandler      UART0_RX_TX_IRQHandler

#define COM_UART_BAUDRATE 115200

#define COM_RX_BUF_SIZE   512
#define COM_TX_BUF_SIZE   512

#if USE_DEBUG_UART
  #define COM_UART                DEBUG_UART
  #define COM_UART_IRQn           DEBUG_UART_IRQn
  #define COM_UART_IRQHandler     DEBUG_UART_IRQHandler
#else
  #define COM_UART                PI_UART
  #define COM_UART_IRQn           PI_UART_IRQn
  #define COM_UART_IRQHandler     PI_UART_IRQHandler
#endif


#endif /* COM_COM_H_ */
