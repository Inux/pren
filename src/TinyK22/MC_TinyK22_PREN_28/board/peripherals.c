/***********************************************************************************************************************
 * This file was generated by the MCUXpresso Config Tools. Any manual edits made to this file
 * will be overwritten if the respective MCUXpresso Config Tools is used to update this file.
 **********************************************************************************************************************/

/* clang-format off */
/* TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
!!GlobalInfo
product: Peripherals v5.0
processor: MK22FN512xxx12
package_id: MK22FN512VLH12
mcu_data: ksdk2_0
processor_version: 5.0.0
board: FRDM-K22F
functionalGroups:
- name: BOARD_InitPeripherals
  called_from_default_init: true
  selectedCore: core0
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS **********/

/* TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
component:
- type: 'system'
- type_id: 'system'
- global_system_definitions: []
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS **********/
/* clang-format on */

/***********************************************************************************************************************
 * Included files
 **********************************************************************************************************************/
#include "peripherals.h"

/***********************************************************************************************************************
 * BOARD_InitPeripherals functional group
 **********************************************************************************************************************/
/***********************************************************************************************************************
 * FTM_1_Motor_PWM initialization code
 **********************************************************************************************************************/
/* clang-format off */
/* TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
instance:
- name: 'FTM_1_Motor_PWM'
- type: 'ftm'
- mode: 'EdgeAligned'
- type_id: 'ftm_04a15ae4af2b404bf2ae403c3dbe98b3'
- functional_group: 'BOARD_InitPeripherals'
- peripheral: 'FTM1'
- config_sets:
  - ftm_main_config:
    - ftm_config:
      - clockSource: 'kFTM_SystemClock'
      - clockSourceFreq: 'GetFreq'
      - prescale: 'kFTM_Prescale_Divide_1'
      - timerFrequency: '20000'
      - bdmMode: 'kFTM_BdmMode_0'
      - pwmSyncMode: 'kFTM_SoftwareTrigger'
      - reloadPoints: ''
      - faultMode: 'kFTM_Fault_Disable'
      - faultFilterValue: '0'
      - deadTimePrescale: 'kFTM_Deadtime_Prescale_1'
      - deadTimeValue: '0'
      - extTriggers: ''
      - chnlInitState: ''
      - chnlPolarity: ''
      - useGlobalTimeBase: 'false'
    - timer_interrupts: ''
    - enable_irq: 'false'
    - ftm_interrupt:
      - IRQn: 'FTM1_IRQn'
      - enable_priority: 'false'
      - enable_custom_name: 'false'
    - EnableTimerInInit: 'true'
  - ftm_edge_aligned_mode:
    - ftm_edge_aligned_channels_config:
      - 0:
        - edge_aligned_mode: 'kFTM_EdgeAlignedPwm'
        - edge_aligned_pwm:
          - chnlNumber: 'kFTM_Chnl_0'
          - level: 'kFTM_HighTrue'
          - dutyCyclePercent: '0'
          - enable_chan_irq: 'false'
      - 1:
        - edge_aligned_mode: 'kFTM_EdgeAlignedPwm'
        - edge_aligned_pwm:
          - chnlNumber: 'kFTM_Chnl_1'
          - level: 'kFTM_LowTrue'
          - dutyCyclePercent: '0'
          - enable_chan_irq: 'false'
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS **********/
/* clang-format on */
const ftm_config_t FTM_1_Motor_PWM_config = {
  .prescale = kFTM_Prescale_Divide_1,
  .bdmMode = kFTM_BdmMode_0,
  .pwmSyncMode = kFTM_SoftwareTrigger,
  .reloadPoints = 0,
  .faultMode = kFTM_Fault_Disable,
  .faultFilterValue = 0,
  .deadTimePrescale = kFTM_Deadtime_Prescale_1,
  .deadTimeValue = 0,
  .extTriggers = 0,
  .chnlInitState = 0,
  .chnlPolarity = 0,
  .useGlobalTimeBase = false
};

const ftm_chnl_pwm_signal_param_t FTM_1_Motor_PWM_pwmSignalParams[] = { 
  {
    .chnlNumber = kFTM_Chnl_0,
    .level = kFTM_HighTrue,
    .dutyCyclePercent = 0
  },
  {
    .chnlNumber = kFTM_Chnl_1,
    .level = kFTM_LowTrue,
    .dutyCyclePercent = 0
  }
};

void FTM_1_Motor_PWM_init(void) {
  FTM_Init(FTM_1_MOTOR_PWM_PERIPHERAL, &FTM_1_Motor_PWM_config);
  FTM_SetupPwm(FTM_1_MOTOR_PWM_PERIPHERAL, FTM_1_Motor_PWM_pwmSignalParams, sizeof(FTM_1_Motor_PWM_pwmSignalParams) / sizeof(ftm_chnl_pwm_signal_param_t), kFTM_EdgeAlignedPwm, 20000U, FTM_1_MOTOR_PWM_CLOCK_SOURCE);
  FTM_StartTimer(FTM_1_MOTOR_PWM_PERIPHERAL, kFTM_SystemClock);
}

/***********************************************************************************************************************
 * FTM_2_Encoder initialization code
 **********************************************************************************************************************/
/* clang-format off */
/* TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
instance:
- name: 'FTM_2_Encoder'
- type: 'ftm'
- mode: 'EdgeAligned'
- type_id: 'ftm_04a15ae4af2b404bf2ae403c3dbe98b3'
- functional_group: 'BOARD_InitPeripherals'
- peripheral: 'FTM2'
- config_sets:
  - ftm_main_config:
    - ftm_config:
      - clockSource: 'kFTM_SystemClock'
      - clockSourceFreq: 'GetFreq'
      - prescale: 'kFTM_Prescale_Divide_128'
      - timerFrequency: '100'
      - bdmMode: 'kFTM_BdmMode_0'
      - pwmSyncMode: 'kFTM_SoftwareTrigger'
      - reloadPoints: ''
      - faultMode: 'kFTM_Fault_Disable'
      - faultFilterValue: '0'
      - deadTimePrescale: 'kFTM_Deadtime_Prescale_1'
      - deadTimeValue: '0'
      - extTriggers: ''
      - chnlInitState: ''
      - chnlPolarity: ''
      - useGlobalTimeBase: 'false'
    - timer_interrupts: 'kFTM_TimeOverflowInterruptEnable'
    - enable_irq: 'true'
    - ftm_interrupt:
      - IRQn: 'FTM2_IRQn'
      - enable_priority: 'true'
      - priority: '2'
      - enable_custom_name: 'false'
    - EnableTimerInInit: 'true'
  - ftm_edge_aligned_mode:
    - ftm_edge_aligned_channels_config:
      - 0:
        - edge_aligned_mode: 'kFTM_InputCapture'
        - input_capture:
          - chnNumber: 'kFTM_Chnl_0'
          - input_capture_edge: 'kFTM_RisingEdge'
          - filterValue: '0'
          - enable_chan_irq: 'true'
      - 1:
        - edge_aligned_mode: 'kFTM_InputCapture'
        - input_capture:
          - chnNumber: 'kFTM_Chnl_1'
          - input_capture_edge: 'kFTM_RisingEdge'
          - filterValue: '0'
          - enable_chan_irq: 'true'
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS **********/
/* clang-format on */
const ftm_config_t FTM_2_Encoder_config = {
  .prescale = kFTM_Prescale_Divide_128,
  .bdmMode = kFTM_BdmMode_0,
  .pwmSyncMode = kFTM_SoftwareTrigger,
  .reloadPoints = 0,
  .faultMode = kFTM_Fault_Disable,
  .faultFilterValue = 0,
  .deadTimePrescale = kFTM_Deadtime_Prescale_1,
  .deadTimeValue = 0,
  .extTriggers = 0,
  .chnlInitState = 0,
  .chnlPolarity = 0,
  .useGlobalTimeBase = false
};

void FTM_2_Encoder_init(void) {
  FTM_Init(FTM_2_ENCODER_PERIPHERAL, &FTM_2_Encoder_config);
  FTM_SetupInputCapture(FTM_2_ENCODER_PERIPHERAL, kFTM_Chnl_0, kFTM_RisingEdge, 0);
  FTM_SetupInputCapture(FTM_2_ENCODER_PERIPHERAL, kFTM_Chnl_1, kFTM_RisingEdge, 0);
  FTM_SetTimerPeriod(FTM_2_ENCODER_PERIPHERAL, ((FTM_2_ENCODER_CLOCK_SOURCE/ (1U << (FTM_2_ENCODER_PERIPHERAL->SC & FTM_SC_PS_MASK))) / 100) + 1);
  FTM_EnableInterrupts(FTM_2_ENCODER_PERIPHERAL, kFTM_Chnl0InterruptEnable | kFTM_Chnl1InterruptEnable | kFTM_TimeOverflowInterruptEnable);
  /* Interrupt vector FTM2_IRQn priority settings in the NVIC */
  NVIC_SetPriority(FTM_2_ENCODER_IRQN, FTM_2_ENCODER_IRQ_PRIORITY);
  /* Enable interrupt FTM2_IRQn request in the NVIC */
  EnableIRQ(FTM_2_ENCODER_IRQN);
  FTM_StartTimer(FTM_2_ENCODER_PERIPHERAL, kFTM_SystemClock);
}

/***********************************************************************************************************************
 * FTM_3_MS_Coutner initialization code
 **********************************************************************************************************************/
/* clang-format off */
/* TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
instance:
- name: 'FTM_3_MS_Coutner'
- type: 'ftm'
- mode: 'EdgeAligned'
- type_id: 'ftm_04a15ae4af2b404bf2ae403c3dbe98b3'
- functional_group: 'BOARD_InitPeripherals'
- peripheral: 'FTM3'
- config_sets:
  - ftm_main_config:
    - ftm_config:
      - clockSource: 'kFTM_SystemClock'
      - clockSourceFreq: 'GetFreq'
      - prescale: 'kFTM_Prescale_Divide_1'
      - timerFrequency: '1000'
      - bdmMode: 'kFTM_BdmMode_0'
      - pwmSyncMode: 'kFTM_SoftwareTrigger'
      - reloadPoints: ''
      - faultMode: 'kFTM_Fault_Disable'
      - faultFilterValue: '0'
      - deadTimePrescale: 'kFTM_Deadtime_Prescale_1'
      - deadTimeValue: '0'
      - extTriggers: ''
      - chnlInitState: ''
      - chnlPolarity: ''
      - useGlobalTimeBase: 'false'
    - timer_interrupts: 'kFTM_TimeOverflowInterruptEnable'
    - enable_irq: 'true'
    - ftm_interrupt:
      - IRQn: 'FTM3_IRQn'
      - enable_priority: 'false'
      - enable_custom_name: 'true'
      - handler_custom_name: 'FTM3_MS_COUNTER_IRQHandler'
    - EnableTimerInInit: 'true'
  - ftm_edge_aligned_mode:
    - ftm_edge_aligned_channels_config: []
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS **********/
/* clang-format on */
const ftm_config_t FTM_3_MS_Coutner_config = {
  .prescale = kFTM_Prescale_Divide_1,
  .bdmMode = kFTM_BdmMode_0,
  .pwmSyncMode = kFTM_SoftwareTrigger,
  .reloadPoints = 0,
  .faultMode = kFTM_Fault_Disable,
  .faultFilterValue = 0,
  .deadTimePrescale = kFTM_Deadtime_Prescale_1,
  .deadTimeValue = 0,
  .extTriggers = 0,
  .chnlInitState = 0,
  .chnlPolarity = 0,
  .useGlobalTimeBase = false
};

void FTM_3_MS_Coutner_init(void) {
  FTM_Init(FTM_3_MS_COUTNER_PERIPHERAL, &FTM_3_MS_Coutner_config);
  FTM_SetTimerPeriod(FTM_3_MS_COUTNER_PERIPHERAL, ((FTM_3_MS_COUTNER_CLOCK_SOURCE/ (1U << (FTM_3_MS_COUTNER_PERIPHERAL->SC & FTM_SC_PS_MASK))) / 1000) + 1);
  FTM_EnableInterrupts(FTM_3_MS_COUTNER_PERIPHERAL, kFTM_TimeOverflowInterruptEnable);
  /* Enable interrupt FTM3_IRQn request in the NVIC */
  EnableIRQ(FTM_3_MS_COUTNER_IRQN);
  FTM_StartTimer(FTM_3_MS_COUTNER_PERIPHERAL, kFTM_SystemClock);
}

/***********************************************************************************************************************
 * Initialization functions
 **********************************************************************************************************************/
void BOARD_InitPeripherals(void)
{
  /* Initialize components */
  FTM_1_Motor_PWM_init();
  FTM_2_Encoder_init();
  FTM_3_MS_Coutner_init();
}

/***********************************************************************************************************************
 * BOARD_InitBootPeripherals function
 **********************************************************************************************************************/
void BOARD_InitBootPeripherals(void)
{
  BOARD_InitPeripherals();
}
