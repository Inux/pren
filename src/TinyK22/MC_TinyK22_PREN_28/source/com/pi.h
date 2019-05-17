/*
 * pi.h
 *
 *  Created on: 17.03.2019
 *      Author: andre
 */

#ifndef COM_PI_H_
#define COM_PI_H_

#include "com.h" /*all definitions in this file */
#include "app.h"
#include "comAck.h"


typedef tError (*frameHandler)(const unsigned char *cmd);

typedef struct frameLineHandler
{
  char topic[COM_PI_TOPIC_MAX_LENGTH];
  char frameDesc[32];
  frameHandler frameHandler;
  struct frameLineHandler *next;
} tframeLineHandler;

void pi_Init(void);

void piRegisterFrameLineHandler(tframeLineHandler *clh,
    unsigned char* cmd, unsigned char *cmdDesc, frameHandler h, tAckHandler *ackHandler);

void piWriteNum32s(const char *topic, int32_t value, tAckHandler* ackHandler);
void piWriteNum32u(const char *topic, uint32_t value, tAckHandler* ackHandler);
void piWriteString(const char *topic, const char *str, tAckHandler* ackHandler);

void piDoWork(void);

#endif /* COM_PI_H_ */
