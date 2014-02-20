#!/bin/bash
# Current Version 1.05
# Written by: Thomas Tillman and Daniel Baena-Urbano
# Maintained by: Thomas Tillman

#Revision History:
# 1.0	05/02/2012	First Release
# 1.01	05/29/2012	Updated for Humax 1.4 HW initialization
# 1.02  07/03/2012	Updated to reduce Beacon timing issue in txMode
# 1.03  07/21/2012	Added setAntenna function
# 1.04  07/23/2012	Added antenna selection inside rxMode, rxPER and txMode functions
# 1.05  08/20/2012	Added scraminit to txMode to make fixed payloads & added sleeps to rxPER

########################################################################
#
# This script is as an interface to the wireless configuration utilities.
#
# NOTE: As currently written can only be used for Broadcom interfaces
# 	that use the WL commands
########################################################################

#List of Functions:
#wifiInit
#wifiTerm
#wifiList
#wifiAPInfo [SSID]
#wifiConnect [SSID][Password]
#wifiConnectIP [SSID] [Password] [IP Address]
#wifiConnected
#wifiStatus
#wifiDisconnect
#wifiMCSindex [index]
#wifiSetChannel [channel] [band] [bandwidth] [ctl sideband]
#wifiIperf2way [Server IP] [timeSecs]
#wifiIperfSend [Server IP] [timeSecs]
#wifiIperfReceive
#wifiCWWave [channel]
#wifiCWWaveStop
#wifiRxMode [channel][bandwidth][ctl sideband][antenna #][protocol][mcs index]
#wifiRxModeStop
#wifiRxMeasure
#wifiRxPER [channel] [bandwidth] [ctl sideband] [protocol] [mcs index/data rate]
#wifiTxMode [channel] [bandwidth] [ctl sideband] [power] [protocol] [mcs index/data rate]
#wifiTxModeStop
#wifiSetPower [power]
#wifiReset
#wifiLogCheck [iperf log filename]
#wifiSetAntenna [antenna #]
#wifiIperfSilentReceive 
#wifiVersion
#wifiFunction


WIFI_TOOL_PATH="/opt/wifi"
WIFI_DRV_PATH="/opt/wifi/"
IPERF="/opt/wifi/iperf"

IWCONFIG_TOOL="$WIFI_TOOL_PATH/iwconfig"
IWLIST_TOOL="$WIFI_TOOL_PATH/iwlist"
IWPRIV_TOOL="$WIFI_TOOL_PATH/iwpriv"
WLANCONFIG_TOOL="$WIFI_TOOL_PATH/wlanconfig"
ACFG_TOOL="$WIFI_TOOL_PATH/acfg_tool"
TX99_TOOL="$WIFI_TOOL_PATH/tx99tool"
ATHTST_TOOL="$WIFI_TOOL_PATH/athtst"
ATD_SUPPBR_TOOL="$WIFI_TOOL_PATH/atd_wsupp_bridge"
WPA_CLI_TOOL="$WIFI_TOOL_PATH/wpa_cli"
WIFI_DRV_ADF_NAME="adf"
WIFI_DRV_ADF="$WIFI_DRV_PATH/adf.ko"
WIFI_DRV_USB_NAME="hif_usb"
WIFI_DRV_USB="$WIFI_DRV_PATH/hif_usb.ko"
WIFI_DRV_FWD_NAME="fwd"
WIFI_DRV_FWD="$WIFI_DRV_PATH/fwd.ko"
WIFI_DRV_ATD_NAME="atd"
WIFI_DRV_ATD="$WIFI_DRV_PATH/atd.ko"
WIFI_IF_PHY="wifi0"
#WIFI_IF_VAP="if2"
WIFI_IF_VAP="wln0"
#mooa ath0
SCAN_RES_FILE="/tmp/scanresults"
WIFI_POWER=/tmp/wifi_power.log
WIFI_CHANNEL="/tmp/wifi_channel.log"



######### mooa samsung add
export LD_LIBRARY_PATH=$WIFI_TOOL_PATH
##################

# To store the info for the SSID in use
WIFI_INFO=/tmp/wifi_info.log

# Time in seconds to wait for the scan to finish
WIFI_SCAN_RETRIES=5

# Time in seconds for the join to finish
WIFI_JOIN_RETRIES=5

# Errors
WIFI_OK=0
WIFI_ERR_BAD_PARAM=1
WIFI_ERR_NOT_NETWORKS=88
WIFI_ERR_NOT_CONNECTED=89
WIFI_ERR_INIT=90
WIFI_ERR_CMD=91
WIFI_ERR_JOIN=92
WIFI_ERR_IP=93
WIFI_ERR_DISCONNECT=94
WIFI_ERR_NOT_FOUND=95

########################################################################
#                              Utilities                               #
########################################################################

#=======================================================================
# Syntax: printInfo [message]
#
# Prints the information message given
#=======================================================================
printInfo()
{
   echo -e "[INFO]  $@"
}

#=======================================================================
# Syntax: printError [message]
#
# Prints the error message given
#=======================================================================
printError()
{
   echo -e "[ERROR] $@"
}

#=======================================================================
# Syntax: exitError [errcode] [message]
#
# Internal function to print an error and exit with the given error code
#=======================================================================
exitError()
{
   errorcode=$1
   shift
   message="$@"
   errorhex=`printf 0x%02X $errorcode`

   if [ ${#message} -gt 0 ]; then
      printError "($errorhex): $message"
   else
      printError "($errorhex)"
   fi
   exit $errorcode
}

#=======================================================================
# Syntax: exitifError [value] [errcode] [message]
#
# If value is not 0, it exits with the error given
#=======================================================================
exitifError()
{
   if [ $1 -ne 0 ]; then
      shift
      exitError $@
   fi
}

#=======================================================================
# Syntax: checkNumParams [expected] [numparams] [functionname]
#
# Validates the input params to a function
#=======================================================================
checkNumParams()
{
   expected=$1
   numparams=$2
   function=$3
   
   if [ $numparams -ne $expected ]; then
      exitError $WIFI_ERR_BAD_PARAM "$function needs $expected, given $numparams"
   fi
}

########################################################################
#                               Functions                              #
########################################################################

#=======================================================================
# Syntax: wifiInit
#
# Makes sure that the drivers are installed and the module is in station
# mode.
#
# This function must succeed if the WiFi driver is already up and ready
#=======================================================================
wifiInit()
{

   # Install drivers if necessary
   #if ! lsmod | grep $WIFI_DRV_ADF_NAME &> /dev/null; then
   #   insmod $WIFI_DRV_ADF
   #   insmod $WIFI_DRV_USB
   #   insmod $WIFI_DRV_FWD
   #   insmod $WIFI_DRV_ATD
   #   exitifError $? $WIFI_ERR_INIT "Failed to install $WIFI_DRV_USB_NAME driver"
   #fi

   # mooa samsung semco start
   if ! lsmod | grep $WIFI_DRV_ADF_NAME &> /dev/null; then
      insmod $WIFI_DRV_ADF
      exitifError $? $WIFI_ERR_INIT "Failed to install $WIFI_DRV_ADF_NAME driver"
   fi
   if ! lsmod | grep $WIFI_DRV_USB_NAME &> /dev/null; then
      insmod $WIFI_DRV_USB
      exitifError $? $WIFI_ERR_INIT "Failed to install $WIFI_DRV_USB_NAME driver"
   fi
   if ! lsmod | grep $WIFI_DRV_FWD_NAME &> /dev/null; then
      insmod $WIFI_DRV_FWD
      exitifError $? $WIFI_ERR_INIT "Failed to install $WIFI_DRV_FWD_NAME driver"
   fi
   if ! lsmod | grep $WIFI_DRV_ATD_NAME &> /dev/null; then
      insmod $WIFI_DRV_ATD
      exitifError $? $WIFI_ERR_INIT "Failed to install $WIFI_DRV_ATD_NAME driver"
   fi
   # mooa samsung semco end

   #if ! lsmod | grep $WIFI_DRV_NAME &> /dev/null; then
   #   insmod $WIFI_DRV
   #   exitifError $? $WIFI_ERR_INIT "Failed to install $WIFI_DRV_NAME driver"
   #fi
   sleep 10
   # Set to station mode
   $WLANCONFIG_TOOL $WIFI_IF_VAP create wlandev $WIFI_IF_PHY wlanmode sta nosbeacon
   exitifError $? $WIFI_ERR_CMD "Command '$WIFI_TOOL ap 0' failed"

   # Make sure interface is down during configuration
   ifconfig $WIFI_IF_VAP down
	 sleep 1
   
   # Reinitialize with new settings
   ifconfig $WIFI_IF_VAP up
   exitifError $? $WIFI_ERR_CMD "Command '$WIFI_TOOL up' failed"

   # Set maximum transmit power
   $IWCONFIG_TOOL $WIFI_IF_VAP txpower 21
   
   printInfo "Wifi initialized successfully"

   return $WIFI_OK

}

#=======================================================================
# Syntax: wifiTerm
#
# Reset and mark adapter down (disabled)
#=======================================================================
wifiTerm()
{
   SUPPLIST=$(ps | grep atd_wsupp_bridg | cut -b 1-5)
   if [ -n $SUPPLIST ]; then
       for i in $SUPPLIST ; do
           printInfo "killing $i"
           kill -9 $i
       done
       sleep 4
   fi

   ifconfig $WIFI_IF_VAP down
   $WLANCONFIG_TOOL $WIFI_IF_VAP destroy
   rmmod $WIFI_DRV_ATD
   rmmod $WIFI_DRV_FWD
   rmmod $WIFI_DRV_USB
   rmmod $WIFI_DRV_ADF
	 printInfo "Adapters down. Drivers Uninstalled"
}


#=======================================================================
# Syntax: wifiList
#
# Prints the list of the SSIDs found
# This command shall only print the SSID names.
# The command wifiAPInfo can be used to retrieve more details about each SSID
#=======================================================================
wifiList()
{
   rm -f $SCAN_RES_FILE
   
   printInfo "Scanning..."
   $IWLIST_TOOL $WIFI_IF_VAP scan | grep ESSID: > $SCAN_RES_FILE
   exitifError $? $WIFI_ERR_CMD "Command '$WIFI_TOOL scan' failed"

   grep ESSID: $SCAN_RES_FILE > /dev/null 2>&1
   es=$?
   if [ $es -eq 0 ]; then  
        printInfo "Networks found:"
        cat $SCAN_RES_FILE
   else
        exitifError $es $WIFI_ERR_NOT_NETWORKS "No WiFi networks found"
   fi
   rm -f $SCAN_RES_FILE

}

#=======================================================================
# Syntax: wifiAPInfo [SSID]
#
# Prints the details for the given SSID
#
# Inputs:
# - SSID: SSID string of the network to retrieve details for
#
# This command shall display the following information for the given SSID:
# - SSID
# - RSSI
# - SNR
# - Noise
# - Channel
# - BSSID
# - Bandwidth
# - Encryption type
#=======================================================================
wifiAPInfo()
{
   checkNumParams 1 ${#@} $FUNCNAME

   SSID=$1
   
   printInfo "Scanning for $SSID..."
   $IWLIST_TOOL $WIFI_IF_VAP scan essid $SSID > $SCAN_RES_FILE
   exitifError $? $WIFI_ERR_CMD "Command '$IWLIST_TOOL $WIFI_IF_VAP scan essid $SSID' failed"
      
   retries=0
   while [ $retries -lt $WIFI_SCAN_RETRIES ]; do

      grep ESSID: $SCAN_RES_FILE > /dev/null 2>&1
      es=$?
      if [ $es -eq 0 ]; then
         break
      else
         let retries=$retries+1

         # Wait for scan to finish
         sleep 3
         $IWLIST_TOOL $WIFI_IF_VAP scan essid $SSID > $SCAN_RES_FILE
      fi
   done

   grep SSID: $SCAN_RES_FILE > /dev/null 2>&1
   if [ "$es" != "0" ]; then  
        exitifError $es $WIFI_ERR_NOT_FOUND "SSID $SSID not found"
   fi
   
   # Get info
   BSSID=$(grep "Address" $SCAN_RES_FILE | sed 's/^.*Cell //g' | cut -d " " -f4)
   RSSI=$(grep "Signal level" $SCAN_RES_FILE | sed 's/^.*Signal //g' | cut -d '=' -f2 | cut -d ' ' -f1)
   Noise=$(grep "Noise" $SCAN_RES_FILE | sed 's/^.*Signal //g' | cut -d '=' -f3 | cut -d ' ' -f1)
   let SNR=$RSSI+-1*$Noise
   #Channel=$( grep "Channel" $SCAN_RES_FILE | sed 's/^.*Channel //g' | cut -d ')' -f1 )
   Freq=$( grep "Frequency" $SCAN_RES_FILE | sed 's/^.*Frequency://g' | cut -d '(' -f1 | cut -d ' ' -f1 )
   PRIBAND=$(echo $Freq | cut -d '.' -f1)
   SUBBAND=$(echo $Freq | cut -d '.' -f2)
   if [ "$PRIBAND" = "2" ]; then
      let Channel=$SUBBAND-412
      let Channel=$Channel/5
      let Channel=$Channel+1   
   elif [ "$PRIBAND" = "5" ]; then
      if [ "${#SUBBAND}" = "1" ]; then
      		Comp=100
      elif [ "${#SUBBAND}" = "2" ];	then
         Comp=10	
      elif [ "${#SUBBAND}" = "3" ];	then
         Comp=1
      else
         Comp=0
      fi      
      let SUBBAND=$SUBBAND*$Comp   
      let Channel=$SUBBAND/5
   fi   
   # Get channel and control channel if available
   controlChannel=$Channel
   # Bandwidth is 40Mhz if indicated, otherwise 20MHz
   if grep "bandwidth" $SCAN_RES_FILE > /dev/null 2>&1; then
      Bandwidth=$(grep "bandwidth" $SCAN_RES_FILE | sed 's/^.*Extra://g' | cut -d '=' -f2)
   else
      Bandwidth="20MHz"
   fi
   # Encryption is open if WEP not found
   # Encryption is WPA2 if "RSN:" found
   # Encryption is WEP if WEP found but not RSN
   if grep "WPA2" $SCAN_RES_FILE > /dev/null 2>&1; then
      Encryption="WPA2"
   elif grep "WPA" $SCAN_RES_FILE > /dev/null 2>&1; then
      Encryption="WPA"
   elif grep "Encryption key:on" $SCAN_RES_FILE > /dev/null 2>&1; then
      Encryption="WEP"
   else
      Encryption="open"
   fi
   rm -f $WIFI_INFO
   
   echo "SSID:$SSID" >> $WIFI_INFO
   echo "BSSID:$BSSID" >> $WIFI_INFO
   echo "RSSI:$RSSI" >> $WIFI_INFO
   echo "SNR:$SNR" >> $WIFI_INFO
   echo "Noise:$Noise" >> $WIFI_INFO
   echo "Channel:$Channel" >> $WIFI_INFO
   #echo "ControlChannel:$controlChannel" >> $WIFI_INFO
   echo "Bandwidth:$Bandwidth" >> $WIFI_INFO
   echo "Encryption:$Encryption" >> $WIFI_INFO
   
   cat $WIFI_INFO	
}

#=======================================================================
# Syntax: wifiConnect [SSID] [Password]
#
# Joins the given SSID. open, WEP, WPA and WPA2 required
# This command must be able to detect the encryption system for the SSID
# provided and connect to it.
#
# Inputs:
# - SSID: SSID string of the network to join
# - Password: Password, if required, to join the network
#=======================================================================
wifiConnect()
{
   checkNumParams 2 ${#@} $FUNCNAME

   SSID=$1
   PASSWORD=$2
   
   wifiDisconnect
       
   # Get SSID info to know the band and encryption type
   if [ ! -e $WIFI_INFO ] || ! grep ESSID $WIFI_INFO | grep $SSID &> /dev/null; then
      # Get info
      wifiAPInfo $SSID
   fi

	 ifconfig $WIFI_IF_VAP down

   # Get encryption type
   encryption=$(grep Encryption $WIFI_INFO | sed 's/Encryption://g')
			
   # Now join
   $IWPRIV_TOOL $WIFI_IF_VAP autoassoc 1
   exitifError $? $WIFI_ERR_CMD "Command '$WIFI_TOOL join $SSID' failed"

   ifconfig $WIFI_IF_VAP up
				
   # Set encryption   
   case $encryption in
      WEP)
         [ -z "PASSWORD" ] && exitError $WIFI_ERR_BAD_PARAM "PASSWORD not given"
         # Add password to WEP key index 0
				 
				 $IWCONFIG_TOOL $WIFI_IF_VAP enc $PASSWORD
         $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID
      ;;         
      WPA)
         [ -z "PASSWORD" ] && exitError $WIFI_ERR_BAD_PARAM "PASSWORD not given"
        $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID
				CONFIG=/tmp/config.wpa
				echo -e "ap_scan=1" > $CONFIG
				echo -e "network={" >> $CONFIG
				echo -e "\tssid=\"${SSID}\"" >> $CONFIG
			  echo -e "\tproto=WPA" >> $CONFIG
				echo -e "\tkey_mgmt=WPA-PSK" >> $CONFIG
				echo -e "\tpairwise=CCMP TKIP" >> $CONFIG
				echo -e "\tpsk=\"${PASSWORD}\"" >> $CONFIG
				echo -e "}" >> $CONFIG
				$ATD_SUPPBR_TOOL -i $WIFI_IF_VAP -c $CONFIG &
				sleep 10
      ;;
      WPA2)
         [ -z "PASSWORD" ] && exitError $WIFI_ERR_BAD_PARAM "PASSWORD not given"
        $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID
				CONFIG=/tmp/config.wpa
				echo -e "ap_scan=1" > $CONFIG
				echo -e "network={" >> $CONFIG
				echo -e "\tssid=\"${SSID}\"" >> $CONFIG
			  echo -e "\tproto=WPA2" >> $CONFIG
				echo -e "\tkey_mgmt=WPA-PSK" >> $CONFIG
				echo -e "\tpairwise=CCMP TKIP" >> $CONFIG
				echo -e "\tpsk=\"${PASSWORD}\"" >> $CONFIG
				echo -e "}" >> $CONFIG
				$ATD_SUPPBR_TOOL -i $WIFI_IF_VAP -c $CONFIG &
				sleep 10
      ;;
      *)
         # Assume not encrypted
         $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID
      ;;
   esac

   # Verify association
   $IWCONFIG_TOOL $WIFI_IF_VAP | grep ESSID:\"$SSID\" > /dev/null 2>&1
   exitifError $? $WIFI_ERR_JOIN "Failed to join SSID $SSID"
   
   sleep 6
   # Finally up the device and start dhcp to get an IP
   ifconfig $WIFI_IF_VAP 0.0.0.0
   /sbin/udhcpc --quit --now --retries=3 --interface=$WIFI_IF_VAP &> /dev/null
   exitifError $? $WIFI_ERR_IP "Failed to get a DHCP IP"
   sleep 2
   printInfo "Connection established"
   # Print status
   wifiStatus
}
#=======================================================================
# Syntax: wifiConnectIP [SSID] [Password] [IP Address]
#
# Joins the given SSID with a specified static IP address. 
# open, WEP, WPA and WPA2 security required
# This command must be able to detect the encryption system for the SSID
# provided and connect to it.
#
# Inputs:
# - SSID: SSID string of the network to join
# - Password: Password to join the network
# - IP Address: Static IP address of device on the network
#=======================================================================
wifiConnectIP()
{
   checkNumParams 3 ${#@} $FUNCNAME

   SSID=$1
   PASSWORD=$2
   IPAddr=$3

   wifiDisconnect

      # Get SSID info to know the band and encryption type
   if [ ! -e $WIFI_INFO ] || ! grep ESSID $WIFI_INFO | grep $SSID &> /dev/null; then
      # Get info
      wifiAPInfo $SSID
   fi

	 ifconfig $WIFI_IF_VAP down

   # Get encryption type
   encryption=$(grep Encryption $WIFI_INFO | sed 's/Encryption://g')
				
   # Now join
   $IWPRIV_TOOL $WIFI_IF_VAP autoassoc 1
   exitifError $? $WIFI_ERR_CMD "Command '$WIFI_TOOL join $SSID' failed"

   ifconfig $WIFI_IF_VAP up
				
   # Set encryption   
   case $encryption in
      WEP)
         [ -z "PASSWORD" ] && exitError $WIFI_ERR_BAD_PARAM "PASSWORD not given"
         # Add password to WEP key index 0
				 
				 $IWCONFIG_TOOL $WIFI_IF_VAP enc $PASSWORD
				 $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID 
      ;;
      WPA)
         [ -z "PASSWORD" ] && exitError $WIFI_ERR_BAD_PARAM "PASSWORD not given"
        $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID 
				CONFIG=/tmp/config.wpa
				echo -e "ap_scan=1" > $CONFIG
				echo -e "network={" >> $CONFIG
				echo -e "\tssid=\"${SSID}\"" >> $CONFIG
			  echo -e "\tproto=WPA" >> $CONFIG
				echo -e "\tkey_mgmt=WPA-PSK" >> $CONFIG
				echo -e "\tpairwise=CCMP TKIP" >> $CONFIG
				echo -e "\tpsk=\"${PASSWORD}\"" >> $CONFIG
				echo -e "}" >> $CONFIG
				$ATD_SUPPBR_TOOL -i $WIFI_IF_VAP -c $CONFIG &
				sleep 10
      ;;
      WPA2)
         [ -z "PASSWORD" ] && exitError $WIFI_ERR_BAD_PARAM "PASSWORD not given"
        $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID 
				CONFIG=/tmp/config.wpa
				echo -e "ap_scan=1" > $CONFIG
				echo -e "network={" >> $CONFIG
				echo -e "\tssid=\"${SSID}\"" >> $CONFIG
			  echo -e "\tproto=WPA2" >> $CONFIG
				echo -e "\tkey_mgmt=WPA-PSK" >> $CONFIG
				echo -e "\tpairwise=CCMP TKIP" >> $CONFIG
				echo -e "\tpsk=\"${PASSWORD}\"" >> $CONFIG
				echo -e "}" >> $CONFIG
				$ATD_SUPPBR_TOOL -i $WIFI_IF_VAP -c $CONFIG &
				sleep 10
      ;;
      *)
         # Assume not encrypted
         $IWCONFIG_TOOL $WIFI_IF_VAP essid $SSID
      ;;
   esac

   # Verify association
   $IWCONFIG_TOOL $WIFI_IF_VAP | grep ESSID:\"$SSID\" > /dev/null 2>&1
   exitifError $? $WIFI_ERR_JOIN "Failed to join SSID $SSID"
   
   # Finally up the device and start dhcp to get an IP
   ifconfig $WIFI_IF_VAP $IPAddr
   sleep 2
   printInfo "Connection established"
   # Print status
   wifiStatus
}

#=======================================================================
# Syntax: wifiConnected
#
# Returns OK if connected, error if not
#=======================================================================
wifiConnected()
{

   # Verify if connected
   SSID=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep ESSID | sed 's/^.*ESSID://g' | sed 's/"//g' | sed 's/ //g')
   BSSID=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Access Point:" | sed 's/^.*Access Point: //g' | sed 's/ Tx-Power=.*$//g' | sed 's/ //g')
   if [ "$BSSID" = "Not-Associated" ]; then
      exitError $WIFI_ERR_NOT_CONNECTED "Not connected"
   fi
   
   printInfo "WiFi connected to $SSID"

   return $WIFI_OK
}

#=======================================================================
# Syntax: wifiStatus
#
# Prints the following details for the current connection:
# - SSID
# - BSSID
# - IP
# - RSSI global
# - RSSI antenna 0
# - RSSI antenna 1
# - Noise level
# - MCS index
# - TX power level
#=======================================================================
wifiStatus()
{
   # Get connection details
   SSID=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep ESSID | sed 's/^.*ESSID://g' | sed 's/"//g' | sed 's/ //g')
   BSSID=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Access Point:" | sed 's/^.*Access Point: //g' | sed 's/ Tx-Power=.*$//g' | sed 's/ //g')
   IP=$(ifconfig $WIFI_IF_VAP | grep "inet" | xargs | sed 's/ /:/g' | cut -d':' -f3)

   # Get RSSI global and for each antena
   RSSI=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Signal level=" | sed 's/^.*Signal //g' | cut -d '=' -f2 | cut -d ' ' -f1)
   RSSI_ANT0=$($ACFG_TOOL acfg_get_ath_stats wifi0 | grep 'ack\[ctl, ch0\]' | cut -d ' ' -f6)
   RSSI_ANT1=$($ACFG_TOOL acfg_get_ath_stats wifi0 | grep 'ack\[ctl, ch1\]' | cut -d ' ' -f6)
   
   # Get noise
   NOISE=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Noise" | sed 's/^.*Signal //g' | cut -d '=' -f3 | cut -d ' ' -f1)
   let RSSI_ANT0=$RSSI_ANT0+$NOISE
   let RSSI_ANT1=$RSSI_ANT1+$NOISE
   # Get tx power
   TXPOWER=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Tx-Power=" | sed 's/^.*Tx-Power=//g')
   
   # Get MCS index
   #MCSINDEX=
   BITRATE=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Bit Rate=" | sed 's/^.*Bit Rate=//g' | sed 's/ Tx-Power=.*$//g' | sed 's/ //g')

   printInfo "SSID:    $SSID"
   printInfo "BSSID:   $BSSID"
   printInfo "IP:      $IP"
   printInfo "RSSI:    $RSSI dBm"
   printInfo "RSSI[0]: $RSSI_ANT0 dBm"
   printInfo "RSSI[1]: $RSSI_ANT1 dBm"
   printInfo "Noise:   $NOISE dBm"
   #printInfo "MCS:     $MCSINDEX"
   printInfo "BitRate: $BITRATE"
   printInfo "TX pwr:  $TXPOWER"
}

#=======================================================================
# Syntax: wifiDisconnect
#
# Disconnects from the current connection
#=======================================================================
wifiDisconnect()
{
   # Disconnect
   SUPPLIST=$(ps | grep atd_wsupp_bridg | cut -b 1-5)
   if [ "$SUPPLIST" != "" ]; then
		   $WPA_CLI_TOOL -i $WIFI_IF_VAP terminate
		   #sleep 10
   fi
   if [ -n $SUPPLIST ]; then
       for i in $SUPPLIST ; do
           printInfo "killing $i"
           kill -9 $i
       done
       #sleep 4
   fi
        
   # Verify if connected
   #SSID=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep ESSID | sed 's/^.*ESSID://g' | sed 's/"//g' | sed 's/ //g')
   #BSSID=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Access Point:" | sed 's/^.*Access Point: //g' | sed 's/ Tx-Power=.*$//g' | sed 's/ //g')
   #if [ "$BSSID" = "Not-Associated" ]; then
   #   printInfo "Not connected"
   #   return $WIFI_OK
   #fi
   
   # Wait for disconnection
   $WLANCONFIG_TOOL $WIFI_IF_VAP destroy
   sleep 1
   $WLANCONFIG_TOOL $WIFI_IF_VAP create wlandev $WIFI_IF_PHY wlanmode sta nosbeacon
	 $IWPRIV_TOOL $WIFI_IF_VAP autoassoc 1
	 ifconfig $WIFI_IF_VAP up

   # Verify
   BSSID=$($IWCONFIG_TOOL $WIFI_IF_VAP | grep "Access Point:" | sed 's/^.*Access Point: //g' | sed 's/ Tx-Power=.*$//g' | sed 's/ //g')
   if [ "$BSSID" = "Not-Associated" ]; then
      printInfo "Disconnected from $SSID successfully"
   else   
      exitError $WIFI_ERR_DISCONNECT "Failed to disconnect"
   fi   
}

#=======================================================================
# Syntax: wifiMCSindex [index]
#
# Sets the MCS index and then prints the new value
#
# Inputs:
# - index: new MCS index
#=======================================================================
wifiMCSindex()
{
   checkNumParams 1 ${#@} $FUNCNAME
	 declare -r HEX_DIGITS="0123456789abcdef" 
	  
   index=$1
   mcsidx=8${HEX_DIGITS:$index:1}
   mcsidx=$mcsidx$mcsidx$mcsidx$mcsidx
   
   $IWPRIV_TOOL $WIFI_IF_VAP set11NRetries 0x04040404
   $IWPRIV_TOOL $WIFI_IF_VAP set11NRates 0x$mcsidx
   exitifError $? $WIFI_ERR_CMD "Command '$IWPRIV_TOOL $WIFI_IF_VAP set11NRates 0x$mcsidx' failed"
   
   # Print MCS current index
   printInfo "fix MCS index to $index"
}

#=======================================================================
# Syntax: wifiSetChannel [channel][band][bandwidth][sideband]
#
# Sets the channel and channel details
#
# Inputs:
# - channel:   0 - 224
# - band:      5 (a), 2 (b/g)
# - bandwidth: 20, 40
# - sideband:  -1 (lower), 0 (none), 1 (upper)
#=======================================================================
wifiSetChannel()
{
   checkNumParams 4 ${#@} $FUNCNAME
   
   channel=$1
   band=$2
   bandwidth=$3
   sideband=$4
  
   rm -f $WIFI_CHANNEL
   echo "CHANNEL:$channel" >> $WIFI_CHANNEL
   echo "BAND:$band" >> $WIFI_CHANNEL
   echo "WIDTH:$bandwidth" >> $WIFI_CHANNEL
   echo "SIDE:$sideband" >> $WIFI_CHANNEL

   printInfo "set channel: $channel, band: $band, bandwidth: $bandwidth, sideband: $sideband"
}


#=======================================================================
# Syntax: wifiIperf2way [Server IP][timeSecs]
#
# Sends AND receives data through the WiFi port for the specified time
# This command must run in the background
# This command saves a log file of the iperf output to a file in /tmp with the name:
#	iPerfLog_2way_YYYY-M-D_HH-MM-SS.txt
#
# Inputs:
# - Server IP: IP of the PC that will be receiving the data
# - timeSecs: time in seconds for this test
#=======================================================================
wifiIperf2way()
{
   checkNumParams 2 ${#@} $FUNCNAME
   
   serverIP=$1
   timeSecs=$2
   
   if [ ! -e $IPERF ]; then
      exitError $WIFI_ERR_NOT_FOUND "iperf utility not available"
   fi
   
   mount -t tmptfs -o remount -o size=10M tmpfs /tmp
   printInfo -n "Please start iperf utility in the server PC with the following command and press a key to continue: ./iperf -s -w 256K -i 1"; read key
   
   # Start client side from box, which is the TX side
   DATE_STRING=$(/bin/date +%Y-%m-%d_%H-%M-%S)
   $IPERF -c $serverIP  -i 1 -t $timeSecs -d -f m | tee /tmp/iPerfLog_2way_$DATE_STRING.txt
   exitifError $? $WIFI_ERR_CMD "Command: $IPERF -c <serverip>  -i 1 -t $timeSecs -d -w 256K | tee /tmp/iPerfLog_$DATE_STRING.txt"
   
   #printInfo "Sending data"
}

#=======================================================================
# Syntax: wifiIperfSend [Server IP][timeSecs]
#
# Sends data through the WiFi port for the specified time
# This command must run in the background
# This command saves a log file of the iperf output to a file in /tmp with the name:
#	iPerfLog_Send_YYYY-M-D_HH-MM-SS.txt
#
# Inputs:
# - Server IP: IP of the PC that will be receiving the data
# - timeSecs: time in seconds for this test
#=======================================================================
wifiIperfSend()
{
   checkNumParams 2 ${#@} $FUNCNAME
   
   serverIP=$1
   timeSecs=$2
   
   if [ ! -e $IPERF ]; then
      exitError $WIFI_ERR_NOT_FOUND "iperf utility not available"
   fi
   
   mount -t tmptfs -o remount -o size=10M tmpfs /tmp
   printInfo -n "Please start iperf utility in the server PC with the following command and press a key to continue: ./iperf -s -w 256K -i 1"; read key
   
   # Start client side from box, which is the TX side
   DATE_STRING=$(/bin/date +%Y-%m-%d_%H-%M-%S)
   $IPERF -c $serverIP  -i 1 -t $timeSecs -f m | tee /tmp/iPerfLog_Send_$DATE_STRING.txt &
   exitifError $? $WIFI_ERR_CMD "Command: $IPERF -c <serverip>  -i 1 -t $timeSecs | tee /tmp/iPerfLog_$DATE_STRING.txt"
   
   #printInfo "Sending data"
}

#=======================================================================
# Syntax: wifiIperfReceive 
#
# Receives data from the WiFi port for the specified time
# This command must run in the background
# This command saves a log file of the iperf output to a file in /tmp with the name:
#	iPerfLog_Receive_YYYY-M-D_HH-MM-SS.txt
#
# Inputs:
# - none
#=======================================================================
wifiIperfReceive()
{
   
   if [ ! -e $IPERF ]; then
      exitError $WIFI_ERR_NOT_FOUND "iperf utility not available"
   fi
   
   # Start server side in box, which is the RX side
   DATE_STRING=$(/bin/date +%Y-%m-%d_%H-%M-%S)
   $IPERF -s -i 1 -f m | tee /tmp/iPerfLog_Receive_$DATE_STRING.txt &
   exitifError $? $WIFI_ERR_CMD "Command: $IPERF -s -i 1 -f m"
   
   
   #BOX_IP=$(ifconfig $WIFI_IF | grep inet | xargs | sed 's/ /:/g' | cut -d':' -f3)
   BOX_IP=$(ifconfig $WIFI_IF_VAP | grep "inet" | xargs | sed 's/ /:/g' | cut -d':' -f3)
   printInfo -n "Ready to receive data. Please start iperf utility in the client PC with the following command and press a key to continue: ./iperf -c $BOX_IP -w 256K -i 1 -t $timeSecs"; read key
}

#=======================================================================
# Syntax: wifiIperfSilentReceive 
#
# Receives data from the WiFi port for the specified time
# This command must run in the background
# This command does NOT display link information, so it can be used with coexistence testing
#
# Inputs:
# - none
#=======================================================================
wifiIperfSilentReceive()
{
   
   if [ ! -e $IPERF ]; then
      exitError $WIFI_ERR_NOT_FOUND "iperf utility not available"
   fi
   
   # Start server side in box, which is the RX side
   DATE_STRING=$(/bin/date +%Y-%m-%d_%H-%M-%S)
   $IPERF -s -i 1 -f m > /dev/null &
   exitifError $? $WIFI_ERR_CMD "Command: $IPERF -s -i 1 -f m"
   
   
   #BOX_IP=$(ifconfig $WIFI_IF | grep "inet" | xargs | sed 's/ /:/g' | cut -d':' -f3)
   BOX_IP=$(ifconfig $WIFI_IF_VAP | grep "inet" | xargs | sed 's/ /:/g' | cut -d':' -f3)   
   printInfo -n "Ready to receive data. Please start iperf utility in the client PC with the following command and press a key to continue: ./iperf -c $BOX_IP -w 256K -i 1 -t $timeSecs"; read key
}

#=======================================================================
# Syntax: wifiCWWave [channel]
#
# Transmits a CW waveform on the selected channel
#
# Inputs:
# - channel: channel to use to transmit the CW wave
#=======================================================================
wifiCWWave()
{
   checkNumParams 1 ${#@} $FUNCNAME
   
   channel=$1
   
   if [ -e $WIFI_POWER ] && grep POWER: $WIFI_POWER &> /dev/null; then
      # Get power
      txpwr=$(grep POWER: $WIFI_POWER | sed 's/POWER://g')
   else
      txpwr="30"
   fi

   if [ -e $WIFI_CHANNEL ] && grep CHANNEL: $WIFI_CHANNEL &> /dev/null; then
      # Get htmode
      width=$(grep WIDTH: $WIFI_CHANNEL | sed 's/WIDTH://g')
      side=$(grep SIDE: $WIFI_CHANNEL | sed 's/SIDE://g')
      if [ "$side" = "0" ]; then  
           mode=0
           extchan=0
      elif [ "$width" = "20" ]; then  
           mode=0
           extchan=0
      elif [ "$side" = "-1" ]; then  
           extchan=2
           mode=2
           let channel=$channel+side*2
      else
           extchan=1
           mode=2
           let channel=$channel+side*2
      fi
   else
      mode=0
      extchan=0
   fi   
   
   $TX99_TOOL $WIFI_IF_PHY set freq $channel $mode $extchan
   $TX99_TOOL $WIFI_IF_PHY set rate 54000
   $TX99_TOOL $WIFI_IF_PHY set txchain 3
   $TX99_TOOL $WIFI_IF_PHY set type 1
   $TX99_TOOL $WIFI_IF_PHY set pwr $txpwr
   $TX99_TOOL $WIFI_IF_PHY start
   exitifError $? $WIFI_ERR_CMD "Command: $WIFI_TOOL fqacurcy $channel"
   
   printInfo "CW test started on channel $channel"
}

#=======================================================================
# Syntax: wifiRxMeasure 
#
# Sets chip to measure RSSI on current channel
#
# Inputs:
# - none
#=======================================================================
wifiRxMeasure()
{
   
  echo "wifiRxMeasure" 
	rxmode=$($ATHTST_TOOL $WIFI_IF_VAP testmode get rx | cut -d '=' f2)
	
	if [ "$rxmode"="1" ]; then
	  sleep 2
		RSSI=$($ATHTST_TOOL $WIFI_IF_VAP testmode get result | grep rssi | cut -d '=' -f2 | cut -d ',' -f1)
	else
	  RSSI=$($ACFG_TOOL acfg_get_rssi $WIFI_IF_VAP | grep "Beacon RSSIavg" | sed 's/^.*Beacon RSSIavg=//g')
	fi  
  
  let RSSI=$RSSI-95
  
	#Print RSSI of current channel
  printInfo "RSSI of current channel is $RSSI"
}

#=======================================================================
# Syntax: wifiSetAntenna [antenna #]
#
# Sets IRD to use either a specific single antenna or all antennas
#
# Inputs:
# - antenna #: sets antennas to use, 0 for ANT0, 1 for ANT1, 2 for ANT2, 3 for ANT3, and 4 for all antennas
#=======================================================================
wifiSetAntenna()
{
   checkNumParams 1 ${#@} $FUNCNAME
   antennas=$1

######## QCA tx99 ################
# antenna # : 0 : NONE
#             1 : ant 0
#             2 : ant 1
#             3 : ant 0 and ant 1 (both)
######## QCA tx99 ################
	   case $antennas in
			0)
				$TX99_TOOL $WIFI_IF_PHY set txchain 1
				exitifError $? $WIFI_ERR_CMD "Command: $TX99_TOOL fail"
				printInfo "Antennas set to ANT0 ONLY"
				;;
			1)
				$TX99_TOOL $WIFI_IF_PHY set txchain 2
				exitifError $? $WIFI_ERR_CMD "Command: $TX99_TOOL fail"
				printInfo "Antennas set to ANT1 ONLY"
				;;
			2|3|4)
				$TX99_TOOL $WIFI_IF_PHY set txchain 3
				exitifError $? $WIFI_ERR_CMD "Command: $TX99_TOOL fail"
				printInfo "Antennas set to ANT0 and ANT1"
				;;
			*)
				printError "Invalid antenna selection, all antennas selected" 
				$TX99_TOOL $WIFI_IF_PHY set txchain 3
				exitifError $? $WIFI_ERR_CMD "Command: $TX99_TOOL fail"
				printInfo "Antennas set to ANT0 and ANT1"
				;;
	   esac


}


#=======================================================================
# Syntax: wifiRxMode [channel][bandwidth][ctl sideband][antenna #][protocol][mcs index]
#
# Sets chip to receive a modulated signal on the selected channel
#	Note: MAC address of wifi module for testing purposes is set to 00:11:22:33:44:55
#
# Inputs:
# - channel: channel to use to receive (for 40 MHz channels this is the center)
# - bandwidth: bandwidth to use, 20 or 40 MHz
# - ctl sideband: upper or lower control channel, 1 for upper, -1 for lower, 0 for 20 MHz channels
# - antenna #: sets antennas to use, 0 for ANT0, 1 for ANT1, 2 for ANT2, 3 for ANT3, and 4 for all antennas
# - protocol: 802.11 flavor:  a b g or n
# - mcs index: If 802.11n, which index (0-15), if not 802.11n, enter data rate in Mbps
#=======================================================================
wifiRxMode()
{
   checkNumParams 6 ${#@} $FUNCNAME
   
   
   channel=$1
   bandwidth=$2
   ctlband=$3
   antparm=$4
   protocol=$5
   mcsi=$6
   
   case $channel in
      1|2|3|4|5|6|7|8|9|10|11|12|13)
         #$WIFI_TOOL band b 
		 band=g
		 ;;
      *)
         #$WIFI_TOOL band a 
		 band=a
		 ;;
   esac
      
   if [ "$ctlband" = "-1" ]; then
      let channel=$channel+$ctlband*2
   		extchan="plus"
   elif [ "$ctlband" = "1" ]; then
      let channel=$channel+$ctlband*2
   	  extchan="minus"
   else
   		extchan=""
   fi			  		
   
   if [ "$protocol" = "n" ]; then
   			modestr="11n"$band"ht"$bandwidth$extchan
   else
   			modestr="11"$protocol		
   fi		
   
   case $antparm in
		0|1)
		  let ant=$antparm+1
			printInfo "Antennas set to ANT$antparm ONLY"
			;;
		2|3|4)
			ant=0
			printInfo "Antennas set to ANT0 and ANT1"
			;;
		*)
			printError "Invalid antenna selection, all antennas selected" 
			ant=0
			printInfo "Antennas set to ANT0 and ANT1"
			;;
   esac
   
   
   ifconfig $WIFI_IF_VAP down
   $WLANCONFIG_TOOL $WIFI_IF_VAP destroy
   $WLANCONFIG_TOOL $WIFI_IF_VAP create wlandev $WIFI_IF_PHY wlanmode monitor
   ifconfig $WIFI_IF_VAP up   
   $IWPRIV_TOOL $WIFI_IF_VAP mode $modestr
   $ATHTST_TOOL $WIFI_IF_VAP testmode set chan $channel
   #$ATHTST_TOOL $WIFI_IF_VAP testmode set bssid ff:ff:ff:ff:ff:ff
   $ATHTST_TOOL $WIFI_IF_VAP testmode set bssid 00:11:22:33:44:55
   $ATHTST_TOOL $WIFI_IF_VAP testmode set ant $ant
   $ATHTST_TOOL $WIFI_IF_VAP testmode set rx  1
   
   printInfo "RX Mode started on channel $channel with $bandwidth MHz BW"
}


#=======================================================================
# Syntax: wifiRxPER [channel][bandwidth][ctl sideband][antenna #][protocol][mcs index]
#
# Sets chip to receive a modulated signal on the selected channel
#	Note: MAC address of wifi module for testing purposes is set to 00:11:22:33:44:55
#	Reports PER based on 10000 Packet input
#
# Inputs:
# - channel: channel to use to receive (for 40 MHz channels this is the center)
# - bandwidth: bandwidth to use, 20 or 40 MHz
# - ctl sideband: upper or lower control channel, 1 for upper, -1 for lower, 0 for 20 MHz channels
# - antenna #: sets antennas to use, 0 for ANT0, 1 for ANT1, 2 for ANT2, 3 for ANT3, and 4 for all antennas
# - protocol: 802.11 flavor:  a b g or n
# - mcs index: If 802.11n, which index (0-15), if not 802.11n, enter data rate in Mbps
#=======================================================================
wifiRxPER()
{
    checkNumParams 6 ${#@} $FUNCNAME
   
   channel=$1
   bandwidth=$2
   ctlband=$3
   antparm=$4
   protocol=$5
   mcsi=$6
   
   case $channel in
      1|2|3|4|5|6|7|8|9|10|11|12|13)
         #$WIFI_TOOL band b 
		 band=g
		 ;;
      *)
         #$WIFI_TOOL band a 
		 band=a
		 ;;
   esac
      
   if [ "$ctlband" = "-1" ]; then
      let channel=$channel+$ctlband*2
   		extchan="plus"
   elif [ "$ctlband" = "1" ]; then
      let channel=$channel+$ctlband*2
   	  extchan="minus"
   else
   		extchan=""
   fi			  		
   
   if [ "$protocol" = "n" ]; then
   			modestr="11n"$band"ht"$bandwidth$extchan
   else
   			modestr="11"$protocol		
   fi		

   case $antparm in
		0|1)
		  let ant=$antparm+1
			printInfo "Antennas set to ANT$antparm ONLY"
			;;
		2|3|4)
			ant=0
			printInfo "Antennas set to ANT0 and ANT1"
			;;
		*)
			printError "Invalid antenna selection, all antennas selected" 
			ant=0
			printInfo "Antennas set to ANT0 and ANT1"
			;;
   esac

   ifconfig $WIFI_IF_VAP down
   $WLANCONFIG_TOOL $WIFI_IF_VAP destroy
   $WLANCONFIG_TOOL $WIFI_IF_VAP create wlandev $WIFI_IF_PHY wlanmode monitor
   ifconfig $WIFI_IF_VAP up   
   $IWPRIV_TOOL $WIFI_IF_VAP mode $modestr
   $ATHTST_TOOL $WIFI_IF_VAP testmode set chan $channel
   #$ATHTST_TOOL $WIFI_IF_VAP testmode set bssid ff:ff:ff:ff:ff:ff
   $ATHTST_TOOL $WIFI_IF_VAP testmode set bssid 00:11:22:33:44:55
   $ATHTST_TOOL $WIFI_IF_VAP testmode set ant $ant
   $ATHTST_TOOL $WIFI_IF_VAP testmode set rx  1
   
   #exitifError $? $WIFI_ERR_CMD "Command: $WIFI_TOOL pkteng_start 00:11:22:33:44:55 rx"
      
    printInfo "RX PER test started on channel $channel with $bandwidth MHz BW"
   
    printInfo "When test transmission is complete hit Enter"
    read input
    printInfo "RX PER test stopped."
    $ATHTST_TOOL $WIFI_IF_VAP testmode set rx 0

    #Calculation of PER goes here
	  #PER based on Sequence of 10,000 packets sent

		perPct=0	  
	  RXCNT=$($ATHTST_TOOL $WIFI_IF_VAP testmode get result | grep rxpkt | cut -d '=' -f2)
	  ERRCNT=$($ATHTST_TOOL $WIFI_IF_VAP testmode get result | grep errpkt | cut -d '=' -f2)
	  perPct=$($ATHTST_TOOL $WIFI_IF_VAP testmode get result | grep per | cut -d '=' -f2)
#	  if [ "$RXCNT" != "0" ]; then
#    	perPct=$(awk -v nn=$ERRCNT -v dd=$RXCNT 'BEGIN {printf "%.2f\n", (nn/dd)*100}')
#    fi

    
	  printInfo "PER is $perPct%"   
    ifconfig $WIFI_IF_VAP down
    $WLANCONFIG_TOOL $WIFI_IF_VAP destroy
    $WLANCONFIG_TOOL $WIFI_IF_VAP create wlandev $WIFI_IF_PHY wlanmode sta nosbeacon
		ifconfig $WIFI_IF_VAP up
}

#=======================================================================
# Syntax: wifiTxMode [IPG][bpf][channel][bandwidth][ctl sideband][antenna #][power][protocol][mod index]
#
# Transmits a modulated signal on the selected channel
#
# Inputs:
# - IPG: inter-packet gap, in microseconds
# - bpf: bytes per frame, in bytes
# - channel: channel to use to transmit (for 40 MHz channels this is the center)
# - bandwidth: bandwidth to use, 20 or 40 MHz
# - ctl sideband: upper or lower control channel, 1 for upper, -1 for lower, 0 for 20 MHz channels
# - antenna #: sets antennas to use, 0 for ANT0, 1 for ANT1, 2 for ANT2, 3 for ANT3, and 4 for all antennas
# - power: set Power of TxMode
# - protocol: 802.11 flavor:  a b g or n
# - modulation index: If 802.11n, which MCS index (0-15), if not 802.11n, enter data rate in Mbps
#=======================================================================
wifiTxMode()
{
   checkNumParams 9 ${#@} $FUNCNAME
   
   ipg_us=$1
   bpf_bytes=$2
   channel=$3
   bandwidth=$4
   ctlband=$5
   antenna=$6
   power=$7
   protocol=$8
   mcsi=$9
 
   if [ "$bandwidth" = "20" ]; then  
        mode=0
	 else
	 			let channel=$channel+ctlband*2
	 			mode=2
	 fi			


   if [ "$ctlband" = "0" ]; then  
        extchan=0
   elif [ "$ctlband" = "-1" ]; then
   			#ctlband upper , extband lower  
        extchan=1 
   else
        #ctlband lower , extband upper 
        extchan=2
   fi

	 echo "mode="$mode

   ratecode=0
   txrate=0
   if [ "$protocol" = "n" ]; then  
      if [ $mcsi -gt 15 ]; then  
         # Invalid MCS index
         printInfo "Invalid MCS index"
         return $WIFI_OK
      fi
      let ratecode="$mcsi+128"
   else
			let txrate="$mcsi*1000"
   fi

   $TX99_TOOL $WIFI_IF_PHY set ipg $ipg_us
   $TX99_TOOL $WIFI_IF_PHY set bpf $bpf_bytes
   $TX99_TOOL $WIFI_IF_PHY set freq $channel $mode $extchan
   $TX99_TOOL $WIFI_IF_PHY set rate $txrate
   $TX99_TOOL $WIFI_IF_PHY set ratecode $ratecode
   
   #wifiSetAntenna [antenna #]
   wifiSetAntenna $antenna 
   
   #$TX99_TOOL $WIFI_IF_PHY set txchain 3
   $TX99_TOOL $WIFI_IF_PHY set type 0
   $TX99_TOOL $WIFI_IF_PHY set pwr $power
   $TX99_TOOL $WIFI_IF_PHY start
   exitifError $? $WIFI_ERR_CMD "Command: $TX99_TOOL fail"
  
   printInfo "TX Mode started on channel $channel with $bandwidth MHz BW"
}

#=======================================================================
# Syntax: wifiTxModeStop
#
# Stops transmission of modulated signal
#
# Inputs:
# - none
#=======================================================================
wifiTxModeStop()
{
   
   $TX99_TOOL $WIFI_IF_PHY stop
   exitifError $? $WIFI_ERR_CMD "Command: $TX99_TOOL $WIFI_IF_PHY stop"
   
   printInfo "TX Mode stopped."
}

#=======================================================================
# Syntax: wifiRxModeStop 
#
# Stops reception of modulated signals
#
# Inputs:
# - none
#=======================================================================
wifiRxModeStop()
{
		$ATHTST_TOOL $WIFI_IF_VAP testmode get result 
		$ATHTST_TOOL $WIFI_IF_VAP testmode set rx 0
   ifconfig $WIFI_IF_VAP down
   $WLANCONFIG_TOOL $WIFI_IF_VAP destroy
   $WLANCONFIG_TOOL $WIFI_IF_VAP create wlandev $WIFI_IF_PHY wlanmode sta nosbeacon
   ifconfig $WIFI_IF_VAP up   

    printInfo "RX Mode stopped."
}

#=======================================================================
# Syntax: wifiCWWaveStop
#
# Stops the CW wave test
#=======================================================================
wifiCWWaveStop()
{
   $TX99_TOOL $WIFI_IF_PHY stop
   exitifError $? $WIFI_ERR_CMD "Command: $TX99_TOOL $WIFI_IF_PHY stop"
   
   printInfo "CW test stopped"
}

#=======================================================================
# Syntax: wifiSetPower [power]
#
# Sets the power level in dBm then prints the current power level
#
# Inputs:
# - power: Power level in dBm
#=======================================================================
wifiSetPower()
{
   checkNumParams 1 ${#@} $FUNCNAME
   
   power=$1
   
   rm -f $WIFI_POWER
   echo "POWER:$power" >> $WIFI_POWER

   printInfo "set txpower: $power dBm"
}


#=======================================================================
# Syntax: wifiReset
#
# Resets the wifi Module to default state
#
# Inputs:
# none
#=======================================================================
wifiReset()
{
   wifiTerm
   sleep 1
   wifiInit
}

#=======================================================================
# Syntax: wifiLogCheck [log filename]
#
# Checks the log file created after running iPerf for throughput dropouts
#
# Inputs:
# - log filename: path and filename of the log file
#=======================================================================
wifiLogCheck()
{
   checkNumParams 1 ${#@} $FUNCNAME
   
   logfilename=$1
   
   DROP_EXIST=$(cat $logfilename |grep sec |grep "0\.00")
   
   cat $logfilename |grep sec |grep "0\.00" |while read line; do if echo $line &> /dev/null; then echo "Dropout occurred at $(echo $line |cut -d']' -f2 |cut -c1-5 |xargs) seconds"; fi; done
   #if [ $DROP_EXIST != "" ]; then
	#	SEC=$($DROP_EXIST |cut -d']' -f2 |cut -c1-5 |xargs)
	#	printInfo "Dropouts occurred at $SEC seconds"
   #fi
   
   DOWNLINK_ID=$(cat $logfilename |grep "connected" |grep "port 5001 connected" |cut -d'[' -f2 |cut -d']' -f1 |xargs)
   UPLINK_ID=$(cat $logfilename |grep "connected" |grep -v "port 5001 connected" |cut -d'[' -f2 |cut -d']' -f1 |xargs)
   
   DOWN_LINE=$(cat $logfilename |grep " 0\.0-" |grep -v " 1\.0" |grep "$DOWNLINK_ID]")
   UP_LINE=$(cat $logfilename |grep " 0\.0-" |grep -v " 1\.0" |grep "$UPLINK_ID]")
   
   DOWN_AVG=$(echo $DOWN_LINE |cut -d' ' -f7-8)
   UP_AVG=$(echo $UP_LINE |cut -d' ' -f7-8)
   
   printInfo "Average throughput for Downlink was $DOWN_AVG"
   printInfo "Average throughput for Uplink was $UP_AVG"
   
   
}


wifiFunction()
{
printInfo "wifiInit"
printInfo "wifiTerm"
printInfo "wifiList"
printInfo "wifiAPInfo [SSID]"
printInfo "wifiConnect [SSID][Password]"
printInfo "wifiConnectIP [SSID] [Password] [IP Address]"
printInfo "wifiConnected"
printInfo "wifiStatus"
printInfo "wifiDisconnect"
printInfo "wifiMCSindex [index]"
printInfo "wifiSetChannel [channel] [band] [bandwidth] [ctl sideband]"
printInfo "wifiIperf2way [Server IP] [timeSecs]"
printInfo "wifiIperfSend [Server IP] [timeSecs]"
printInfo "wifiIperfReceive"
printInfo "wifiCWWave [channel]"
printInfo "wifiCWWaveStop"
printInfo "wifiRxMode [channel][bandwidth][ctl sideband][antenna #][protocol][mcs index]"
printInfo "wifiRxModeStop"
printInfo "wifiRxMeasure"
printInfo "wifiRxPER [channel][bandwidth][ctl sideband][antenna #][protocol][mcs index]"
printInfo "wifiTxMode [IPG][bpf][channel][bandwidth][ctl sideband][antenna #][power][protocol][mod index]"
printInfo "wifiTxModeStop"
printInfo "wifiSetPower [power]"
printInfo "wifiReset"
printInfo "wifiLogCheck [iperf log filename]"
printInfo "wifiSetAntenna [antenna #]"
printInfo "wifiIperfSilentReceive"
printInfo "wifiScriptVersion"
printInfo "wifiFunction"
}


wifiVersion()
{
   printInfo "2012.08.24:SetAntena,AP connection [based on 0823DTV script]"
   printInfo "2012.08.25_r06 :RxTest_FF:FF:FF:FF:FF:FF_RxAntSet [based on 0823DTV script]"
   printInfo "2012.09.01_r08 :add Disconnect before connect "
   printInfo "2012.09.10_r09 :RxTest_PER_00:11:22:33:44:55_with DRV_PATCH"
   printInfo "2012.09.26_r10 :tx ipg,bpf,antenna added"   
   printInfo "2012.10.06_r11 :iwlist 3sec delay for 5G upper channel con & channel parsing change & silentrcv WIFI_IF_VAP"   
}

########################################################################
#                             Script Main                              #
########################################################################

	# Param 1 is the function, the rest the params for that function
	func=$1
	shift
	params="$@"

	# Call the function given
	case $func in
	   "init")        		wifiInit $params ;;
	   "term")        		wifiTerm $params ;;
	   "list")        		wifiList $params ;;
	   "connected")   		wifiConnected $params ;;
	   "status")      		wifiStatus $params ;;
	   "apinfo")      		wifiAPInfo $params ;;
	   "connect")     		wifiConnect $params ;;
	   "connectIP")     	wifiConnectIP $params ;;
	   "disconnect")  		wifiDisconnect $params ;;
	   "logCheck")			wifiLogCheck $params ;;
   "setAntenna")		wifiSetAntenna $params ;;
	   "setMCSindex") 		wifiMCSindex $params ;;
	   "setChannel")  		wifiSetChannel $params ;;
	   "iperf2way")			wifiIperf2way $params ;;
	   "iperfSend")    		wifiIperfSend $params ;;
	   "iperfReceive") 		wifiIperfReceive $params ;;
   "iperfSilentReceive")	wifiIperfSilentReceive $params ;;
	   "txMode")    		wifiTxMode $params ;;
	   "txModeStop")		wifiTxModeStop $params ;;
	   "rxPER") 			wifiRxPER $params ;;
	   "rxMode") 			wifiRxMode $params ;;
	   "rxModeStop")		wifiRxModeStop $params ;;
	   "rxMeasure")			wifiRxMeasure $params ;;
	   "cwwave")      		wifiCWWave $params ;;
	   "cwwaveStop")  		wifiCWWaveStop $params ;;
	   "setPower")    		wifiSetPower $params ;;
	   "reset")       		wifiReset $params ;;
     "version")         wifiVersion $params ;;
     "function")         wifiFunction $params ;;     
	   
	   *) ;;
	esac

	# Exit if script not sourced
	[ "$0" != "-sh" ] && exit $WIFI_OK

