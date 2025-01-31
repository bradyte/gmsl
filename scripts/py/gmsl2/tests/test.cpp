/*
# Name: TBrady2
# Date: 12/16/2024
# Version: 1.6.0
#
# I2C Address(0x), Register Address(0x), Register Value(0x), Read Modify Write(0x)
#
# THIS DATA FILE, AND ALL INFORMATION CONTAINED THEREIN,
# IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL ANALOG DEVICES, INC. BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE DATA FILE,
# THE INFORMATION CONTAINED THEREIN, OR ITS USE FOR ANY PURPOSE.
# BEFORE USING THIS DATA FILE IN ANY APPLICATION FOR PRODUCTION OR DEPLOYMENT,
# THE CUSTOMER IS SOLELY RESPONSIBLE FOR TESTING AND VERIFYING
# THE CONTENT OF THIS DATA FILE IN CONNECTION WITH THEIR PRODUCTS AND SYSTEM(S).
# ---------------------------------------------------------------------------------
#
#            _____ _____  
#      /\   |  __ \_   _| 
#     /  \  | |  | || |   
#    / /\ \ | |  | || |   
#   / ____ \| |__| || |_  
#  /_/    \_\_____/_____| 
#
# ---------------------------------------------------------------------------------
*/
/*
# This script is validated on: 
# MAX96717
# MAX96716A
# Please refer to the Errata sheet for each device.
# ---------------------------------------------------------------------------------
*/
//  
// CSIConfigurationTool
//  
// GMSL-A / Serializer: MAX96717 (Pixel Mode) / Mode: 1x4 / Device Address: 0x80 / Multiple-VC Case: Single VC / Pipe Sharing: Separate Pipes
// PipeZ:
// Input Stream: VC0 RAW10 PortB (D-PHY) (Doubled)

// Deserializer: MAX96716A / Mode: 2 (1x4) / Device Address: 0x50
// PipeY:
// GMSL-A Input Stream: VC0 RAW10 PortB - Output Stream: VC0 RAW10 PortA (D-PHY)

0x04,0x50,0x03,0x13,0x00, // BACKTOP : BACKTOP12 | CSI_OUT_EN (CSI_OUT_EN): CSI output disabled
// Link Initialization for Deserializer
0x04,0x50,0x00,0x10,0x01, // TCTRL : CTRL0 | AUTO_LINK (AUTO_LINK): Disabled | (Default) LINK_CFG (LINK_CFG): 0x1
// Link Initialization for Deserializer
0x04,0x50,0x00,0x01,0x02, // DEV : REG1 | (Default) DIS_REM_CC (GMSL Link A I2C Port 0): Enabled
0x04,0x50,0x00,0x03,0x57, // DEV : REG3 | DIS_REM_CC_B (GMSL Link B I2C Port 0): Disabled
0x00,0x01, // Warning: The actual recommended delay is 5 usec.
// Video Transmit Configuration for Serializer(s)
0x04,0x80,0x00,0x02,0x03, // DEV : REG2 | VID_TX_EN_Z (VID_TX_EN_Z): Disabled
//  
// INSTRUCTIONS FOR GMSL-A SERIALIZER MAX96717
//  
// MIPI D-PHY Configuration
0x04,0x80,0x03,0x30,0x00, // MIPI_RX : MIPI_RX0 | (Default) RSVD (Port Configuration): 1x4
0x04,0x80,0x03,0x83,0x00, // MIPI_RX_EXT : EXT11 | Tun_Mode (Tunnel Mode): Disabled
0x04,0x80,0x03,0x31,0x30, // MIPI_RX : MIPI_RX1 | (Default) ctrl1_num_lanes (Port B - Lane Count): 4
0x04,0x80,0x03,0x32,0xE0, // MIPI_RX : MIPI_RX2 | (Default) phy1_lane_map (Lane Map - PHY1 D0): Lane 2 | (Default) phy1_lane_map (Lane Map - PHY1 D1): Lane 3
0x04,0x80,0x03,0x33,0x04, // MIPI_RX : MIPI_RX3 | (Default) phy2_lane_map (Lane Map - PHY2 D0): Lane 0 | (Default) phy2_lane_map (Lane Map - PHY2 D1): Lane 1
0x04,0x80,0x03,0x34,0x00, // MIPI_RX : MIPI_RX4 | (Default) phy1_pol_map (Polarity - PHY1 Lane 0): Normal | (Default) phy1_pol_map (Polarity - PHY1 Lane 1): Normal
0x04,0x80,0x03,0x35,0x00, // MIPI_RX : MIPI_RX5 | (Default) phy2_pol_map (Polarity - PHY2 Lane 0): Normal | (Default) phy2_pol_map (Polarity - PHY2 Lane 1): Normal | (Default) phy2_pol_map (Polarity - PHY2 Clock Lane): Normal
// Controller to Pipe Mapping Configuration
0x04,0x80,0x03,0x08,0x64, // FRONTTOP : FRONTTOP_0 | (Default) RSVD (CLK_SELZ): Port B | (Default) START_PORTB (START_PORTB): Enabled
0x04,0x80,0x03,0x11,0x40, // FRONTTOP : FRONTTOP_9 | (Default) START_PORTBZ (START_PORTBZ): Start Video
0x04,0x80,0x03,0x18,0x6B, // FRONTTOP : FRONTTOP_16 | mem_dt1_selz (mem_dt1_selz): 0x6B
// Double Mode Configuration
0x04,0x80,0x03,0x13,0x04, // FRONTTOP : FRONTTOP_11 | bpp10dblz (bpp10dblz): Send 10-bit pixels as 20-bit
0x04,0x80,0x03,0x1E,0x34, // FRONTTOP : FRONTTOP_22 | soft_bppz (soft_bppz): 0x14 | soft_bppz_en (soft_bppz_en): Software override enabled
// Pipe Configuration
0x04,0x80,0x00,0x5B,0x00, // CFGV__VIDEO_Z : TX3 | TX_STR_SEL (TX_STR_SEL Pipe Z): 0x0
//  
// INSTRUCTIONS FOR DESERIALIZER MAX96716A
//  
// Video Pipes And Routing Configuration
0x04,0x50,0x01,0x61,0x30, // VIDEO_PIPE_SEL : VIDEO_PIPE_SEL | VIDEO_PIPE_SEL_Y (STR_SELY): Link A Stream Id 0
// Pipe to Controller Mapping Configuration
0x04,0x50,0x04,0x4B,0x07, // MIPI_TX__1 : MIPI_TX11 | MAP_EN_L (MAP_EN_L Pipe Y): 0x7
0x04,0x50,0x04,0x4C,0x00, // MIPI_TX__1 : MIPI_TX12 | (Default) MAP_EN_H (MAP_EN_H Pipe Y): 0x0
0x04,0x50,0x04,0x4D,0x2B, // MIPI_TX__1 : MIPI_TX13 | MAP_SRC_0 (MAP_SRC_0 Pipe Y DT): 0x2B | (Default) MAP_SRC_0 (MAP_SRC_0 Pipe Y VC): 0x0
0x04,0x50,0x04,0x4E,0x2B, // MIPI_TX__1 : MIPI_TX14 | MAP_DST_0 (MAP_DST_0 Pipe Y DT): 0x2B | (Default) MAP_DST_0 (MAP_DST_0 Pipe Y VC): 0x0
0x04,0x50,0x04,0x4F,0x00, // MIPI_TX__1 : MIPI_TX15 | (Default) MAP_SRC_1 (MAP_SRC_1 Pipe Y DT): 0x0 | (Default) MAP_SRC_1 (MAP_SRC_1 Pipe Y VC): 0x0
0x04,0x50,0x04,0x50,0x00, // MIPI_TX__1 : MIPI_TX16 | (Default) MAP_DST_1 (MAP_DST_1 Pipe Y DT): 0x0 | (Default) MAP_DST_1 (MAP_DST_1 Pipe Y VC): 0x0
0x04,0x50,0x04,0x51,0x01, // MIPI_TX__1 : MIPI_TX17 | MAP_SRC_2 (MAP_SRC_2 Pipe Y DT): 0x1 | (Default) MAP_SRC_2 (MAP_SRC_2 Pipe Y VC): 0x0
0x04,0x50,0x04,0x52,0x01, // MIPI_TX__1 : MIPI_TX18 | MAP_DST_2 (MAP_DST_2 Pipe Y DT): 0x1 | (Default) MAP_DST_2 (MAP_DST_2 Pipe Y VC): 0x0
0x04,0x50,0x04,0x6D,0x15, // MIPI_TX__1 : MIPI_TX45 | MAP_DPHY_DEST_0 (MAP_DPHY_DST_0 Pipe Y): 0x1 | MAP_DPHY_DEST_1 (MAP_DPHY_DST_1 Pipe Y): 0x1 | MAP_DPHY_DEST_2 (MAP_DPHY_DST_2 Pipe Y): 0x1
// Double Mode Configuration
0x04,0x50,0x04,0x73,0x04, // MIPI_TX__1 : MIPI_TX51 | ALT_MEM_MAP10 (ALT_MEM_MAP10 CTRL1): Alternate memory map enabled
// MIPI D-PHY Configuration
0x04,0x50,0x03,0x30,0x04, // MIPI_PHY : MIPI_PHY0 | (Default) phy_4x2 (Port Configuration): 2 (1x4)
0x04,0x50,0x04,0x4A,0xD0, // MIPI_TX__1 : MIPI_TX10 | (Default) CSI2_LANE_CNT (Port A - Lane Count): 4
0x04,0x50,0x03,0x33,0x4E, // MIPI_PHY : MIPI_PHY3 | (Default) phy0_lane_map (Lane Map - PHY0 D0): Lane 2 | (Default) phy0_lane_map (Lane Map - PHY0 D1): Lane 3 | (Default) phy1_lane_map (Lane Map - PHY1 D0): Lane 0 | (Default) phy1_lane_map (Lane Map - PHY1 D1): Lane 1
0x04,0x50,0x03,0x35,0x00, // MIPI_PHY : MIPI_PHY5 | (Default) phy0_pol_map (Polarity - PHY0 Lane 0): Normal | (Default) phy0_pol_map (Polarity - PHY0 Lane 1): Normal | (Default) phy1_pol_map (Polarity - PHY1 Lane 0): Normal | (Default) phy1_pol_map (Polarity - PHY1 Lane 1): Normal | (Default) phy1_pol_map (Polarity - PHY1 Clock Lane): Normal
0x04,0x50,0x1D,0x00,0xF4, // DPLL__CSI2 : DPLL_0 | config_soft_rst_n (config_soft_rst_n - PHY1): 0x0
// This is to set predefined (coarse) CSI output frequency
// CSI Phy 1 is 1500 Mbps/lane.
0x04,0x50,0x1D,0x00,0xF4, // DPLL__CSI2 : DPLL_0 | (Default) 
0x04,0x50,0x03,0x20,0x2F, // (Default) 
0x04,0x50,0x1D,0x00,0xF5, // DPLL__CSI2 : DPLL_0 |  | (Default) config_soft_rst_n (config_soft_rst_n - PHY1): 0x1
0x04,0x50,0x03,0x32,0x34, // MIPI_PHY : MIPI_PHY2 | phy_Stdby_n (phy_Stdby_2): Put PHY2 in standby mode | phy_Stdby_n (phy_Stdby_3): Put PHY3 in standby mode
0x04,0x50,0x03,0x13,0x02, // BACKTOP : BACKTOP12 | CSI_OUT_EN (CSI_OUT_EN): CSI output enabled
// Video Transmit Configuration for Serializer(s)
0x04,0x80,0x00,0x02,0x43, // DEV : REG2 | VID_TX_EN_Z (VID_TX_EN_Z): Enabled
