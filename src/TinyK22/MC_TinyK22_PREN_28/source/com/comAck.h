/*
 * comAck.h
 *
 *  Created on: 21.03.2019
 *      Author: andre
 */

#ifndef COM_COMACK_H_
#define COM_COMACK_H_

#include "pi.h"
#include <stdbool.h>

typedef void (*AckTimeoutHandler)(void);


typedef struct ackHandler
{
  char topic[PI_TOPIC_MAX_LENGTH];
  AckTimeoutHandler timeoutHandler;
  bool outstanding;
  uint8_t nbrOfRetries;
  bool new; //if the handler was set outsanding since the last check
  struct ackHandler *next;
} tAckHandler;

void ack_init(void);

void ackCheckQueue(void);

void ackSend(tAckHandler *ackHandler);

void ackRegisterHandler(tAckHandler *ackHandler);
void ackRegisterOutstanding(tAckHandler *ackHandler);

#endif /* COM_COMACK_H_ */
