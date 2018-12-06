/*
 * VL6180X.c
 *
 *  Created on: 30.11.2018
 *      Author: andre
 */


#include "VL6180X.h"
#include "platform.h"
#include "i2c.h"

uint8_t proxSensAddress =  0x29;


tError proxSensInit()
{
  tError result = EC_FAILED;
  uint8_t readBuffer[1];

  result = proxSensReadReg(0x016, readBuffer);
  // check to see has it be Initialised already
  if (1 != *readBuffer && EC_SUCCESS != result)
  {
    result = EC_FAILED;
  }

  // Mandatory : private registers
  //TODO comment configurations
  result = proxSensWriteReg(0x0207, 0x01);

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0208, 0x01);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0096, 0x00);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0097, 0xfd);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00e3, 0x01);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00e4, 0x03);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00e5, 0x02);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00e6, 0x01);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00e7, 0x03);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00f5, 0x02);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00d9, 0x05);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00db, 0xce);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00dc, 0x03);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00dd, 0xf8);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x009f, 0x00);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00a3, 0x3c);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00b7, 0x00);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00bb, 0x3c);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00b2, 0x09);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00ca, 0x09);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0198, 0x01);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x01b0, 0x17);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x01ad, 0x00);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x00ff, 0x05);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0100, 0x05);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0199, 0x05);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x01a6, 0x1b);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x01ac, 0x3e);
  }


  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x01a7, 0x1f);
  }

  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0030, 0x00);
  }

  // Recommended : Public registers - See data sheet for more detail

  // Enables polling for ‘New Sample ready when measurement completes
  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0011, 0x10);
  }
  // Set the averaging sample period (compromise between lower noise and increased execution time)
  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x010a, 0x30);
  }
  // Sets the light and dark gain (upper nibble). Dark gain should not be changed
  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x003f, 0x46);
  }
  // sets the # of range measurements after which auto calibration of system is performed
  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0031, 0xFF);
  }
  // Set ALS integration time to 100ms
  if (result == EC_SUCCESS)
  {
    result = proxSensWriteReg(0x0041, 0x63);
  }

  return result;
}

tError proxSensWriteReg(uint16_t reg, uint8_t data)
{
  tError result = EC_FAILED;

  // send I2C-Address
  result = i2cStart(proxSensAddress, FALSE);

  // send index high byte
  if (result == EC_SUCCESS)
  {
    result = i2cSendData((uint8_t*)(&reg)+1, 1);
  }

  // send index low byte
  if (result == EC_SUCCESS)
  {
    //uint8_t regs = (uint8_t)(reg >> 8);
    result = i2cSendData((uint8_t*)(&reg), 1);
  }

  // send data
  if (result == EC_SUCCESS)
  {
    result = i2cSendData(&data, 1);
  }

  // generate stop condition
  i2cStop();

  return result;
}

tError proxSensReadReg(uint16_t reg, uint8_t* data)
{
  tError result = EC_FAILED;

  // send I2C-Address
  result = i2cStart(proxSensAddress, FALSE);

  // send index high byte
  if (result == EC_SUCCESS)
  {
    result = i2cSendData((uint8_t*)(&reg)+1, 1);
  }

  // send index low byte
  if (result == EC_SUCCESS)
  {
    result = i2cSendData((uint8_t*)(&reg), 1);
  }

  // repeated start to change the direction from write to read
  if (result == EC_SUCCESS)
  {
    result = i2cRepeatedStart(proxSensAddress, TRUE);
  }

  // read the data & generate the stop condition
  if (result == EC_SUCCESS)
  {
    i2cReceiveData(data, 1);
  }

  return result;
}

tError proxSensRange(uint8_t* data)
{
  tError result = EC_FAILED;
  uint8_t status[1];
  status[0] = 0;

  // start single range measurement
  result = proxSensWriteReg(0x018,0x01);

  // poll the VL6180 till new sample ready
  if(EC_FAILED == result)
  {
    // wait for new measurement ready status
    while (*status != 0x04 && EC_SUCCESS == result)
    {
      // check the status
      result = proxSensReadReg(0x04f, status);
      status[0] = status[0] & 0x07;
      //wait_ms(1); // (can be removed)
    }
  }

  // read range result
  if(EC_SUCCESS == result)
  {
    result = proxSensReadReg(0x062, data);
  }

  // clear the interrupt on VL6180
  if(EC_SUCCESS == result)
  {
    result = proxSensWriteReg(0x015,0x07);
  }

  return result;

}

void VL6180X_init()
{
  tError result = EC_I2C_NO_ANSWER;
  proxSensAddress = 0x29;

  result = i2cTest(proxSensAddress);

  if (EC_SUCCESS == result)
  {
    termWriteLine("ProxSens Test ok");
    result = proxSensInit();
  }

  if (EC_SUCCESS == result)
  {
    termWriteLine("ProxSens Init ok");
  }

}




