/*
 * comLog.h
 *
 *  Created on: 22.03.2019
 *      Author: andre
 */

#ifndef COM_COMLOG_H_
#define COM_COMLOG_H_

#include "com.h"
#include "comAck.h"
#include "pi.h"

#define LOG_LEVEL_ALL       (3)
#define LOG_LEVEL_WARN      (2)
#define LOG_LEVEL_CRITICAL  (1)
#define LOG_LEVEL_ERROR     (0)

#define LOG_LEVEL           LOG_LEVEL_ALL

#define LOG_INFO(s)
#define LOG_WARN(s)
#define LOG_CRITICAL(s)
#define LOG_ERROR(s)

#if (LOG_LEVEL >= LOG_LEVEL_ALL)
#define LOG_INFO(s)       piWriteString(LOG_TOPIC, "Info:"s, NULL);
#endif

#if (LOG_LEVEL >= LOG_LEVEL_WARN)
#define LOG_WARN(s)       piWriteString(LOG_TOPIC, "Warn:"s, NULL);
#endif

#if (LOG_LEVEL >= LOG_LEVEL_CRITICAL)
#define LOG_CRITICAL(s)   piWriteString(LOG_TOPIC, "Critical:"s, NULL);
#endif

#if (LOG_LEVEL >= LOG_LEVEL_ERROR)
#define LOG_ERROR(s)      piWriteString(LOG_TOPIC, "Error:"s, NULL);
#endif

#endif /* COM_COMLOG_H_ */
