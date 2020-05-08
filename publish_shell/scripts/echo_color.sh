#!/bin/bash

function yellow_echo () 
{
        local what=$*
        echo -e "\e[1;33m-- Info: ${what} \e[0m"
}

function green_echo () 
{
        local what=$*
        echo -e "\e[1;32m-- Info: ${what} \e[0m"
}

function red_echo () 
{
        local what=$*
        echo -e "\e[1;31m-- Error: ${what} \e[0m"
}
