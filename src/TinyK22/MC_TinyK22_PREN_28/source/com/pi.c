/*
 * pi.c
 *
 *  Created on: 17.03.2019
 *      Author: andre
 */

#include "com.h"
#include "uart.h"
#include "app.h"
#include "pi.h"
#include "McuUtility.h"

static tframeLineHandler *head = NULL;

/**
 * registers a new Frame line handler
 */
void piRegisterFrameLineHandler(tframeLineHandler *flh, unsigned char* topic,
    unsigned char *frameDesc, frameHandler h)
{
  flh->next = head;
  head = flh;

  strncpy(flh->topic, topic, sizeof(flh->topic));
  strcat(flh->topic, SEP_TOKEN);
  strncpy(flh->frameDesc, frameDesc, sizeof(flh->frameDesc));
  flh->frameHandler = h;
}

void piWriteNum32s(const char *topic, int32_t value)
{
  char str[sizeof("-2147483648")];
  McuUtility_Num32sToStr(str, sizeof(str), value);
  piWriteString(topic, str);
}

void piWriteString(const char *topic, const char *str)
{
  uartWrite(topic);
  uartWrite(SEP_TOKEN);
  uartWriteLine(str);
}

/**
 * Parses one frame and executes the appropriate command.
 *
 * @param[in] frame
 *   the null terminated string to process
 */
void piParseFrame(char *frame)
{
  uint8_t topicLength = 0;
  tError result = EC_INVALID_CMD;
  tframeLineHandler *clh = head;
  char buf[16];

  while (clh != NULL)
  {
    if (strncmp(frame, clh->topic, strlen(clh->topic)) == 0)
    {
      topicLength = strlen(clh->topic);
      result = clh->frameHandler(frame + strlen(clh->topic));
      break;
    }
    clh = clh->next;
  }

  if (result != EC_SUCCESS)
  {
    //todo: log error
  }
}

/**
 * @brief Pi do work
 *
 * This function reads a line from the uart and calls the
 * piParseFrame function to process the command.
 */
void piDoWork(void)
{
  char frame[256];

  if (uartHasLineReceived())
  {
    uartReadLine(frame, sizeof(frame));
    piParseFrame(frame);
  }
}

void pi_init(void)
{
  McuUtility_Init();
  uart_inti();

}
