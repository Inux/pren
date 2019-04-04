/*
 * phase.h
 *
 *  Created on: 04.04.2019
 *      Author: andre
 */

#ifndef PHASE_PHASE_H_
#define PHASE_PHASE_H_

typedef enum
{
  PH_startup = 0,
  PH_find_cube = 1,
  PH_grab_cube = 2,
  PH_round_one = 3,
  PH_round_two = 4,
  PH_find_stop = 5,
  PH_stopping = 6,
  PH_finished = 7,
} tPhase;

void phase_Init(void);


#endif /* PHASE_PHASE_H_ */
