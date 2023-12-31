"""**************************************************************
*   Desciribe:                                                  *
*       The main function of line-bot                           *
*                                                               *
*   Date    : 2023/07/29                                        *
*   Author  : YongHong, Liu                                     *
*                                                               *
**************************************************************"""
#======import part=================================================================================
import os
import server
#==================================================================================================
#======variable declare============================================================================

#==================================================================================================
#======function declare============================================================================

#==================================================================================================
#==================================================================================================
if __name__ == "__main__":
    
    port = 443
    myLinebotServer = server.linebotServer()
    print("Start line-bot server on Port: ", port)
    myLinebotServer.start('0.0.0.0', port, cert=True)