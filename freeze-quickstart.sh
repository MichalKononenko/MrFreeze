#!/bin/bash

# Display some kickass ASCII art
echo "
     _     _   ____         _____   ____    _____   _____   _____   _____
    | \   / | |    |       |  ___| |    |  |  ___| |  ___| |___  | |  ___|
    |  \ /  | | == |       | |__   | == |  | |___  | |___     / /  | |___ 
    | | v | | | |  |       |  __|  | |  |  |  ___| |  ___|   / /   |  ___|
    | |   | | | |\ \    _  | |     | |\ \  | |___  | |___   / /__  | |___
    |_|   |_| |_| \_\  |_| |_|     |_| \_\ |_____| |_____| |_____| |_____|
    ---   --- ---  ---  -   -       -- --   -----   -----   -----   -----
"

# Parameters for Python Script ###############################################
GAUSSMETER_ADDRESS=/dev/ttyUSB0
LN2_GAUGE_ADDRESS=/dev/ttyUSB1
POWER_SUPPLY_ADDRESS=/dev/ttyUSB2
##############################################################################

# Variables ##################################################################
promptAddress=""
virtualEnvName="MrFreeze"
##############################################################################

# Hard-coded parameters ######################################################
PROGRAM_DIRECTORY=~/git/MrFreeze
PROGRAM_NAME=mr_freeze
RESULT_DIRECTORY=$PROGRAM_DIRECTORY
##############################################################################

read -p "Enter Gaussmeter Address (default /dev/ttyUSB0): " promptAddress

# Ask for required parameters

if [ "$promptAddress" != "" ]; then
    GAUSSMETER_ADDRESS=$promptAddress
    promptAddress=""
fi

read -p "Enter Liquid Nitrogen Address (default /dev/ttyUSB1): " promptAddress

if [ "$promptAddress" != "" ]; then
    LN2_GAUGE_ADDRESS=$promptAddress
    promptAddress=""
fi

read -p "Enter Power Supply Address (default /dev/ttyUSB2): " promptAddress

if [ "$promptAddress" != "" ]; then
    POWER_SUPPLY_ADDRESS=$promptAddress
    promptAddress=""
fi

CONFIRMATION_TEXT="
    Running Mr Freeze with the following parameters
    -----------------------------------------------

    script location:      ${PROGRAM_DIRECTORY}/${PROGRAM_NAME}

    Parameters
    ----------

    gaussmeter address:   $GAUSSMETER_ADDRESS
    LN2 gauge address:    $LN2_GAUGE_ADDRESS
    Power supply address: $POWER_SUPPLY_ADDRESS 

    Results
    -------

    Output Directory:     $RESULT_DIRECTORY

    is this correct (Y/N): "

read -p "${CONFIRMATION_TEXT}" USER_CONFIRM

function run {

    source /usr/local/bin/virtualenvwrapper.sh

    workon ${virtualEnvName}

    cd ${PROGRAM_DIRECTORY}

    python ${PROGRAM_DIRECTORY}/${PROGRAM_NAME} \
        --gaussmeter-address=${GAUSSMETER_ADDRESS} \
        --ln2-gauge-address=${LN2_GAUGE_ADDRESS} \
        --power-supply-address=${POWER_SUPPLY_ADDRESS}
}

case $USER_CONFIRM in
    "n")
        exit 1
        ;;
    "N")
        exit 1
        ;;
    "y")
        run
        ;;
    "Y")
        run
        ;;
esac

