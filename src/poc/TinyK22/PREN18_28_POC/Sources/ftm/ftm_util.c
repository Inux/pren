/*
 * ftm_util.c
 *
 *  Created on: 16.11.2018
 *      Author: andre
 */

#include "MK22F51212.h"
#include "ftm_util.h"
#include "math.h"

FTM_SC_PS_VALUES FTM_SC_PS_getApproximativeScaler(double devider)
{
  FTM_SC_PS_VALUES ps_value = round(log2(devider));
  if (ps_value > DivideBy128)
  {
    ps_value = DivideBy128;
  }
  if (ps_value < DivideBy1)
  {
    ps_value = DivideBy1;
  }

  return ps_value;
}
