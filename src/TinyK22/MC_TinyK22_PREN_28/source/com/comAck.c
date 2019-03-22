/*
 * comAck.c
 *
 *  Created on: 21.03.2019
 *      Author: andre
 */

#include "comAck.h"
#include "pi.h"
#include "comLog.h"

static tframeLineHandler ack_flh;

static tAckHandler *head = NULL;

/**
 * checks if there are any ack-messages to long outstanding
 */
void ackCheckQueue(void)
{
  tAckHandler *ackHandler = head;

  while (ackHandler != NULL)
  {
    if (ackHandler->outstanding == true)
    {
      if (ackHandler->new == true)
      {
        // is outstanding since last check --> check next time again
        ackHandler->new = false;
      }
      else
      {
        ackHandler->timeoutHandler();
      }
    }

    ackHandler = ackHandler->next;
  }
}

/**
 * sends a ack message for the given topic to the pi
 */
void ackSend(tAckHandler *ackHandler)
{
  if (ackHandler != NULL)
  {
    piWriteString(ACK_TOPIC, ackHandler->topic, NULL);
  }
}

void ackDefaultTimeoutHandler()
{
  LOG_INFO("ack timeout occurred - default handler");
}

/**
 * Registers a new handler for the given topic
 */
void ackRegisterHandler(tAckHandler *ackHandler)
{
  if (ackHandler != NULL)
  {
    ackHandler->next = head;
    head = ackHandler;

    ackHandler->nbrOfRetries = 0;
    ackHandler->outstanding = false;

    if (ackHandler->timeoutHandler == NULL)
    {
      ackHandler->timeoutHandler = ackDefaultTimeoutHandler;
    }
  }
}

/**
 * registers the topic of the given ackHandler
 * to have an ack outstanding
 *
 * if the ack already was outstanding nbrOfRetries is incremented
 */
void ackRegisterOutstanding(tAckHandler *ackHandler)
{
  if (ackHandler != NULL)
  {
    if (ackHandler->outstanding == true)
    {
      ackHandler->nbrOfRetries++;
    }
    else
    {
      ackHandler->nbrOfRetries = 0;
    }

    ackHandler->outstanding = true;
    ackHandler->new = true;
  }
}

/**
 * handles incoming ack messages
 */
tError AckFrameHandler(const unsigned char *topic)
{
  uint8_t topicLength = 0;
  tError result = EC_INVALID_ARG;
  tAckHandler *ackHandler = head;

  while (ackHandler != NULL)
  {
    if (strncmp(topic, ackHandler->topic, strlen(ackHandler->topic)) == 0)
    {
      ackHandler->outstanding = false;
      ackHandler->nbrOfRetries = 0;
      result = EC_SUCCESS;
      break;
    }
    ackHandler = ackHandler->next;
  }

  if (result != EC_SUCCESS)
  {
    LOG_WARN("ack for unknown topic received");
  }
}

/**
 * Initializes the ack manager
 * registers itselfe at the pi-framhandler
 */
void ack_init(void)
{
  piRegisterFrameLineHandler(&ack_flh, ACK_TOPIC, "handles ack messages", AckFrameHandler, NULL);
}
