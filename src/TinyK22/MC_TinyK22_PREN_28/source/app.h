/*
 * app.h
 *
 *  Created on: 07.03.2019
 *      Author: andre
 */

#ifndef APP_H_
#define APP_H_

typedef enum
{
  EC_SUCCESS = 0,           // no error
  EC_FAILED,

  EC_INVALID_CMD,           // invalid or unknown command
  EC_INVALID_ARG,           // invalid or unknown argument(s)
  EC_OVERFLOW,              // overflow

  EC_I2C_NO_ANSWER ,        // No answer from the i2c device during address calling
  EC_I2C_NAK,               // i2c device answered but NAK received during the transmission

} tError;

void RunApp(void);

#endif /* APP_H_ */
