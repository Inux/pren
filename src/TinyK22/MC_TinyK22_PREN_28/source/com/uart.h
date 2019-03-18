/*
 * uart.h
 *
 *  Created on: 17.03.2019
 *      Author: andre
 */

#ifndef COM_UART_H_
#define COM_UART_H_


void uart_inti(void);
void uartWriteChar(char ch);
void uartWrite(const char *str);
void uartWriteLine(const char *str);
char uartReadChar(void);
uint16_t uartReadLine(char *str, uint16_t length);
bool uartHasLineReceived(void);
uint16_t uartRxBufCount(void);

#endif /* COM_UART_H_ */
