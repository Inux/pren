/* ###################################################################
**     This component module is generated by Processor Expert. Do not modify it.
**     Filename    : LEDpin2.h
**     Project     : FRDM-K64F_Generator
**     Processor   : MK64FN1M0VLL12
**     Component   : SDK_BitIO
**     Version     : Component 01.025, Driver 01.00, CPU db: 3.00.000
**     Compiler    : GNU C Compiler
**     Date/Time   : 2019-02-16, 17:45, # CodeGen: 426
**     Abstract    :
**          GPIO component usable with NXP SDK
**     Settings    :
**          Component name                                 : LEDpin2
**          SDK                                            : McuLib
**          GPIO Name                                      : GPIOA
**          PORT Name                                      : PORTA
**          Pin Number                                     : 0
**          Pin Symbol                                     : LED2
**          Do Pin Muxing                                  : no
**          Init Direction                                 : Output
**          Pull Resistor                                  : no pull resistor
**          Init Value                                     : 0
**     Contents    :
**         GetDir    - bool LEDpin2_GetDir(void);
**         SetDir    - void LEDpin2_SetDir(bool Dir);
**         SetInput  - void LEDpin2_SetInput(void);
**         SetOutput - void LEDpin2_SetOutput(void);
**         GetVal    - bool LEDpin2_GetVal(void);
**         PutVal    - void LEDpin2_PutVal(bool Val);
**         ClrVal    - void LEDpin2_ClrVal(void);
**         SetVal    - void LEDpin2_SetVal(void);
**         NegVal    - void LEDpin2_NegVal(void);
**         Init      - void LEDpin2_Init(void);
**         Deinit    - void LEDpin2_Deinit(void);
**
** * Copyright (c) 2015-2019, Erich Styger
**  * Web:         https://mcuoneclipse.com
**  * SourceForge: https://sourceforge.net/projects/mcuoneclipse
**  * Git:         https://github.com/ErichStyger/McuOnEclipse_PEx
**  * All rights reserved.
**  *
**  * Redistribution and use in source and binary forms, with or without modification,
**  * are permitted provided that the following conditions are met:
**  *
**  * - Redistributions of source code must retain the above copyright notice, this list
**  *   of conditions and the following disclaimer.
**  *
**  * - Redistributions in binary form must reproduce the above copyright notice, this
**  *   list of conditions and the following disclaimer in the documentation and/or
**  *   other materials provided with the distribution.
**  *
**  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
**  * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
**  * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
**  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
**  * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
**  * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
**  * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
**  * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
**  * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
**  * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
** ###################################################################*/
/*!
** @file LEDpin2.h
** @version 01.00
** @brief
**          GPIO component usable with NXP SDK
*/         
/*!
**  @addtogroup LEDpin2_module LEDpin2 module documentation
**  @{
*/         

/* MODULE LEDpin2. */

#include "LEDpin2.h"
#if McuLib_CONFIG_NXP_SDK_2_0_USED
  #if LEDpin2_CONFIG_DO_PIN_MUXING
  #include "fsl_port.h" /* include SDK header file for port muxing */
  #endif
  #include "fsl_gpio.h" /* include SDK header file for GPIO */
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  #include "fsl_gpio_driver.h" /* include SDK header file for GPIO */
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  #include "pins_gpio_hw_access.h"
  #include "pins_driver.h" /* include SDK header file for GPIO */
#else
  #error "Unsupported SDK!"
#endif

#if McuLib_CONFIG_NXP_SDK_2_0_USED
  static const gpio_pin_config_t LEDpin2_configOutput = {
    kGPIO_DigitalOutput,  /* use as output pin */
    LEDpin2_CONFIG_INIT_PIN_VALUE,  /* initial value */
  };

  static const gpio_pin_config_t LEDpin2_configInput = {
    kGPIO_DigitalInput,  /* use as input pin */
    LEDpin2_CONFIG_INIT_PIN_VALUE,  /* initial value */
  };
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  const gpio_output_pin_user_config_t LEDpin2_OutputConfig[] = {
    {
      .pinName = LEDpin2_CONFIG_PIN_SYMBOL,
      .config.outputLogic = LEDpin2_CONFIG_INIT_PIN_VALUE,
    #if FSL_FEATURE_PORT_HAS_SLEW_RATE
      .config.slewRate = kPortSlowSlewRate,
    #endif
    #if FSL_FEATURE_PORT_HAS_OPEN_DRAIN
      .config.isOpenDrainEnabled = true,
    #endif
    #if FSL_FEATURE_PORT_HAS_DRIVE_STRENGTH
      .config.driveStrength = kPortLowDriveStrength,
    #endif
    },
    {
      .pinName = GPIO_PINS_OUT_OF_RANGE,
    }
  };

  const gpio_input_pin_user_config_t LEDpin2_InputConfig[] = {
    {
      .pinName = LEDpin2_CONFIG_PIN_SYMBOL,
    #if FSL_FEATURE_PORT_HAS_PULL_ENABLE
      #if LEDpin2_CONFIG_PULL_RESISTOR==0 /* 0: no pull resistor, 1: pull-up, 2: pull-down, 3: pull-up or no pull, 4: pull-down or no pull: 4: autoselect-pull */
      .config.isPullEnable = false,
      #else
      .config.isPullEnable = true,
      #endif
    #endif
    #if FSL_FEATURE_PORT_HAS_PULL_SELECTION
      #if LEDpin2_CONFIG_PULL_RESISTOR==1
      .config.pullSelect = kPortPullUp,
      #else
      .config.pullSelect = kPortPullDown,
      #endif
    #endif
    #if FSL_FEATURE_PORT_HAS_PASSIVE_FILTER
      .config.isPassiveFilterEnabled = true,
    #endif
    #if FSL_FEATURE_PORT_HAS_DIGITAL_FILTER
      .config.isDigitalFilterEnabled = true,
    #endif
    #if FSL_FEATURE_GPIO_HAS_INTERRUPT_VECTOR
      .config.interrupt = kPortIntDisabled
    #endif
    },
    {
      .pinName = GPIO_PINS_OUT_OF_RANGE,
    }
  };
#endif

static bool LEDpin2_isOutput = false;
/*
** ===================================================================
**     Method      :  ClrVal (component SDK_BitIO)
**
**     Description :
**         Clears the pin value (sets it to a low level)
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_ClrVal(void)
{
#if McuLib_CONFIG_NXP_SDK_2_0_USED
  #if McuLib_CONFIG_CPU_IS_LPC
  GPIO_PortClear(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #elif McuLib_CONFIG_SDK_VERSION < 250
  GPIO_ClearPinsOutput(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #else
  GPIO_PortClear(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #endif
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  GPIO_DRV_ClearPinOutput(LEDpin2_CONFIG_PIN_SYMBOL);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  PINS_GPIO_WritePin(LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, 0);
#endif
}

/*
** ===================================================================
**     Method      :  SetVal (component SDK_BitIO)
**
**     Description :
**         Sets the pin value to a high value.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_SetVal(void)
{
#if McuLib_CONFIG_NXP_SDK_2_0_USED
  #if McuLib_CONFIG_CPU_IS_LPC
  GPIO_PortSet(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #elif McuLib_CONFIG_SDK_VERSION < 250
  GPIO_SetPinsOutput(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #else
  GPIO_PortSet(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #endif
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  GPIO_DRV_SetPinOutput(LEDpin2_CONFIG_PIN_SYMBOL);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  PINS_GPIO_WritePin(LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, 1);
#endif
}

/*
** ===================================================================
**     Method      :  NegVal (component SDK_BitIO)
**
**     Description :
**         Toggles/negates the pin value
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_NegVal(void)
{
#if McuLib_CONFIG_NXP_SDK_2_0_USED
  #if McuLib_CONFIG_CPU_IS_LPC
  GPIO_PortToggle(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #elif McuLib_CONFIG_SDK_VERSION < 250
  GPIO_TogglePinsOutput(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #else
  GPIO_PortToggle(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  #endif
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  GPIO_DRV_TogglePinOutput(LEDpin2_CONFIG_PIN_SYMBOL);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  pins_channel_type_t val;

  val = PINS_GPIO_GetPinsOutput(LEDpin2_CONFIG_PORT_NAME);
  if (val&(1<<LEDpin2_CONFIG_PIN_NUMBER)) {
    PINS_GPIO_WritePin(LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, 0);
  } else {
    PINS_GPIO_WritePin(LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, 1);
  }
#endif
}

/*
** ===================================================================
**     Method      :  GetVal (component SDK_BitIO)
**
**     Description :
**         Returns the pin value
**     Parameters  : None
**     Returns     :
**         ---             - Returns the value of the pin:
**                           FALSE/logical level '0' or TRUE/logical
**                           level '1'
** ===================================================================
*/
bool LEDpin2_GetVal(void)
{
#if McuLib_CONFIG_CPU_IS_LPC
  return GPIO_PinRead(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER);
#elif McuLib_CONFIG_NXP_SDK_2_0_USED
  #if McuLib_CONFIG_SDK_VERSION < 250
  return GPIO_ReadPinInput(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PIN_NUMBER)!=0;
  #else
  return GPIO_PinRead(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PIN_NUMBER)!=0;
  #endif
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  return GPIO_DRV_ReadPinInput(LEDpin2_CONFIG_PIN_SYMBOL)!=0;
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  return (PINS_DRV_ReadPins(LEDpin2_CONFIG_PORT_NAME)&(1<<LEDpin2_CONFIG_PIN_NUMBER))!=0;
#else
  return FALSE;
#endif
}

/*
** ===================================================================
**     Method      :  GetDir (component SDK_BitIO)
**
**     Description :
**         Return the direction of the pin (input/output)
**     Parameters  : None
**     Returns     :
**         ---             - FALSE if port is input, TRUE if port is
**                           output
** ===================================================================
*/
bool LEDpin2_GetDir(void)
{
  return LEDpin2_isOutput;
}

/*
** ===================================================================
**     Method      :  SetDir (component SDK_BitIO)
**
**     Description :
**         Sets the direction of the pin (input or output)
**     Parameters  :
**         NAME            - DESCRIPTION
**         Dir             - FALSE: input, TRUE: output
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_SetDir(bool Dir)
{
  if (Dir) {
    LEDpin2_SetOutput();
  } else {
    LEDpin2_SetInput();
  }
}

/*
** ===================================================================
**     Method      :  SetInput (component SDK_BitIO)
**
**     Description :
**         Sets the pin as input
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_SetInput(void)
{
#if McuLib_CONFIG_CPU_IS_LPC
  GPIO_PinInit(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, &LEDpin2_configInput);
#elif McuLib_CONFIG_NXP_SDK_2_0_USED
  GPIO_PinInit(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PIN_NUMBER, &LEDpin2_configInput);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  GPIO_DRV_SetPinDir(LEDpin2_CONFIG_PIN_SYMBOL, kGpioDigitalInput);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  pins_channel_type_t val;

  val = PINS_GPIO_GetPinsDirection(LEDpin2_CONFIG_PORT_NAME); /* bit 0: pin is input; 1: pin is output */
  val &= ~(1<<LEDpin2_CONFIG_PIN_NUMBER); /* clear bit ==> input */
  PINS_DRV_SetPinsDirection(LEDpin2_CONFIG_PORT_NAME, val);
#endif
  LEDpin2_isOutput = false;
}

/*
** ===================================================================
**     Method      :  SetOutput (component SDK_BitIO)
**
**     Description :
**         Sets the pin as output
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_SetOutput(void)
{
#if McuLib_CONFIG_CPU_IS_LPC
  GPIO_PinInit(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, &LEDpin2_configOutput);
#elif McuLib_CONFIG_NXP_SDK_2_0_USED
  GPIO_PinInit(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PIN_NUMBER, &LEDpin2_configOutput);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  GPIO_DRV_SetPinDir(LEDpin2_CONFIG_PIN_SYMBOL, kGpioDigitalOutput);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  pins_channel_type_t val;

  val = PINS_GPIO_GetPinsDirection(LEDpin2_CONFIG_PORT_NAME); /* bit 0: pin is input; 1: pin is output */
  val |= (1<<LEDpin2_CONFIG_PIN_NUMBER); /* set bit ==> output */
  PINS_DRV_SetPinsDirection(LEDpin2_CONFIG_PORT_NAME, val);
#endif
  LEDpin2_isOutput = true;
}

/*
** ===================================================================
**     Method      :  PutVal (component SDK_BitIO)
**
**     Description :
**         Sets the pin value
**     Parameters  :
**         NAME            - DESCRIPTION
**         Val             - Value to set. FALSE/logical '0' or
**                           TRUE/logical '1'
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_PutVal(bool Val)
{
#if McuLib_CONFIG_CPU_IS_LPC
  if (Val) {
    GPIO_PortSet(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  } else {
    GPIO_PortClear(LEDpin2_CONFIG_GPIO_NAME, LEDpin2_CONFIG_PORT_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  }
#elif McuLib_CONFIG_NXP_SDK_2_0_USED
  #if McuLib_CONFIG_SDK_VERSION < 250
  if (Val) {
    GPIO_SetPinsOutput(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  } else {
    GPIO_ClearPinsOutput(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  }
  #else
  if (Val) {
    GPIO_PortSet(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  } else {
    GPIO_PortClear(LEDpin2_CONFIG_GPIO_NAME, 1<<LEDpin2_CONFIG_PIN_NUMBER);
  }
  #endif
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  GPIO_DRV_WritePinOutput(LEDpin2_CONFIG_PIN_SYMBOL, Val);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  PINS_DRV_WritePin(LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, Val);
#endif
}

/*
** ===================================================================
**     Method      :  Init (component SDK_BitIO)
**
**     Description :
**         Driver initialization method
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_Init(void)
{
#if McuLib_CONFIG_NXP_SDK_2_0_USED
  #if LEDpin2_CONFIG_DO_PIN_MUXING
  PORT_SetPinMux(LEDpin2_CONFIG_PORT_NAME, LEDpin2_CONFIG_PIN_NUMBER, kPORT_MuxAsGpio); /* mux as GPIO */
  #endif
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_KINETIS_1_3
  /*! \todo Pin Muxing not implemented */
  GPIO_DRV_Init(LEDpin2_InputConfig, LEDpin2_OutputConfig);
#elif McuLib_CONFIG_SDK_VERSION_USED == McuLib_CONFIG_SDK_S32K
  /* the following needs to be called in the application first:
  PINS_DRV_Init(NUM_OF_CONFIGURED_PINS, g_pin_mux_InitConfigArr);
  */
#endif
#if LEDpin2_CONFIG_INIT_PIN_DIRECTION == LEDpin2_CONFIG_INIT_PIN_DIRECTION_INPUT
  LEDpin2_SetInput();
#elif LEDpin2_CONFIG_INIT_PIN_DIRECTION == LEDpin2_CONFIG_INIT_PIN_DIRECTION_OUTPUT
  LEDpin2_SetOutput();
#endif
}

/*
** ===================================================================
**     Method      :  Deinit (component SDK_BitIO)
**
**     Description :
**         Driver de-initialization method
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void LEDpin2_Deinit(void)
{
  /* nothing needed */
}

/* END LEDpin2. */

/*!
** @}
*/
