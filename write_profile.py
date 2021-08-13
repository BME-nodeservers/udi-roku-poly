#!/usr/bin/env python3

import collections
import re
import os
import json

pfx = "write_profile:"

VERSION_FILE = "profile/version.txt"

# Create a dynamic NLS file with the mapping between application ID and
# application names.

def write_nls(logger, roku_list):
    logger.info("{0} Writing profile/nls/en_us.txt".format(pfx))
    if not os.path.exists("profile/nls"):
        try:
            os.makedirs("profile/nls")
        except:
            logger.error('unable to create node NLS directory.')

    try:
        nls = open("profile/nls/en_us.txt", "w")

        # Write out the standard node, command, and status entries

        #nls.write("# controller\n")
        #nls.write("ND-Roku-NAME = Roku Media Player\n")
        #nls.write("ND-Roku-ICON = Output\n")
        nls.write("ST-ctl-ST-NAME = Online\n")
        #nls.write("ST-ctl-GV0-NAME = Log Level\n")
        nls.write("ST-ctl-GV1-NAME = Active Application Name\n")
        nls.write("ST-ctl-GV2-NAME = Active Application ID\n")
        nls.write("CMD-ctl-HOME-NAME = Home\n")
        nls.write("CMD-ctl-REV-NAME = Reverse\n")
        nls.write("CMD-ctl-FWD-NAME = Forward\n")
        nls.write("CMD-ctl-PLAY-NAME = Play\n")
        nls.write("CMD-ctl-SELECT-NAME = Select\n")
        nls.write("CMD-ctl-LEFT-NAME = Left\n")
        nls.write("CMD-ctl-RIGHT-NAME = Right\n")
        nls.write("CMD-ctl-DOWN-NAME = Down\n")
        nls.write("CMD-ctl-UP-NAME = Up\n")
        nls.write("CMD-ctl-BACK-NAME = Back\n")
        nls.write("CMD-ctl-REPLAY-NAME = InstantReplay\n")
        nls.write("CMD-ctl-INFO-NAME = Info\n")
        nls.write("CMD-ctl-BACKSPACE-NAME = Backspace\n")
        nls.write("CMD-ctl-SEARCH-NAME = Search\n")
        nls.write("CMD-ctl-ENTER-NAME = Enter\n")
        nls.write("CMD-ctl-LAUNCH-NAME = Launch\n")
        nls.write("CMD-ctl-VOLUP-NAME = Volume Up\n")
        nls.write("CMD-ctl-VOLDOWN-NAME = Volume Down\n")
        nls.write("CMD-ctl-MUTE-NAME = Volume Mute\n")
        nls.write("CMD-ctl-CHNLUP-NAME = Channel Up\n")
        nls.write("CMD-ctl-CHNLDOWN-NAME = Channel Down\n")
        nls.write("CMD-ctl-OFF-NAME = Power Off\n")
        nls.write("CMD-ctl-TUNER-NAME = Tuner Input\n")
        nls.write("CMD-ctl-HDMI1-NAME = HDMI 1 Input\n")
        nls.write("CMD-ctl-HDMI2-NAME = HDMI 2 Input\n")
        nls.write("CMD-ctl-HDMI3-NAME = HDMI 3 Input\n")
        nls.write("CMD-ctl-HDMI4-NAME = HDMI 4 Input\n")
        nls.write("CMD-ctl-AV-NAME = AV Input\n")
        nls.write("\n")

        for rk in roku_list:
            node_id = roku_list[rk]['node_id']
            nls.write('ND-{}-NAME = {}\n'.format(node_id, roku_list[rk]['name']))
            nls.write('ND-{}-ICON = Output\n'.format(node_id))
            for app in roku_list[rk]['apps']:
                logger.debug(roku_list[rk]['apps'][app])
                (name, cnt) = roku_list[rk]['apps'][app]
                nls.write('{}-{} = {}\n'.format(node_id, cnt, name))
            nls.write("\n")

        nls.close()
    except Exception as e:
        logger.error('Failed to write node NLS file: {}'.format(e))
        nls.close()

    logger.info(pfx + " done.")


NODEDEF_TMPL = "  <nodeDef id=\"%s\" nodeType=\"139\" nls=\"%s\">\n"
STATUS_TMPL = "      <st id=\"%s\" editor=\"_25_0_R_0_%d_N_%s\" />\n"
LAUNCH_TMPL = "          <p id=\"\" editor=\"_25_0_R_0_%d_N_%s\" init=\"%s\" />\n"
def write_nodedef(logger, roku_list):
    nodedef = open("profile/nodedef/nodedefs.xml", "w")

    nodedef.write("<nodeDefs>\n")
    '''
    # First, write the controller node definition
    nodedef.write(NODEDEF_TMPL % ('Roku', 'ctl'))
    nodedef.write("    <sts>\n")
    nodedef.write("      <st id=\"ST\" editor=\"bool\" />\n")
    nodedef.write("      <st id=\"GV0\" editor=\"DEBUG\" />\n")
    nodedef.write("    </sts>\n")
    nodedef.write("    <cmds>\n")
    nodedef.write("      <sends />\n")
    nodedef.write("      <accepts>\n")
    nodedef.write("        <cmd id=\"DISCOVER\" />\n")
    nodedef.write("        <cmd id=\"REMOVE_NOTICES_ALL\" />\n")
    nodedef.write("        <cmd id=\"UPDATE_PROFILE\" />\n")
    nodedef.write("        <cmd id=\"DEBUG\">\n")
    nodedef.write("          <p id=\"\" editor=\"DEBUG\" init=\"GV0\" />\n")
    nodedef.write("        </cmd>\n")
    nodedef.write("      </accepts>\n")
    nodedef.write("    </cmds>\n")
    nodedef.write("  </nodeDef>\n\n")
    '''

    # Loop through and write the node defs for each device
    for rk in roku_list:
        logger.debug('{} - {}'.format(rk, roku_list[rk]))

        try:
            no_apps = len(roku_list[rk]['apps'])
        except:
            no_apps = 0

        node_id = roku_list[rk]['node_id']

        nodedef.write(NODEDEF_TMPL % (node_id, 'ctl'))
        nodedef.write("    <sts>\n")
        nodedef.write("      <st id=\"ST\" editor=\"bool\" />\n")
        nodedef.write("      <st id=\"GV1\" editor=\"_25_0_R_0_%d_N_%s\" />\n" % (no_apps, node_id))
        nodedef.write("      <st id=\"GV2\" editor=\"app_id\" />\n")
        nodedef.write("    </sts>\n")
        nodedef.write("    <cmds>\n")
        nodedef.write("      <sends />\n")
        nodedef.write("      <accepts>\n")
        nodedef.write("        <cmd id=\"HOME\" />\n")
        nodedef.write("        <cmd id=\"REV\" />\n")
        nodedef.write("        <cmd id=\"FWD\" />\n")
        nodedef.write("        <cmd id=\"PLAY\" />\n")
        nodedef.write("        <cmd id=\"SELECT\" />\n")
        nodedef.write("        <cmd id=\"LEFT\" />\n")
        nodedef.write("        <cmd id=\"RIGHT\" />\n")
        nodedef.write("        <cmd id=\"DOWN\" />\n")
        nodedef.write("        <cmd id=\"UP\" />\n")
        nodedef.write("        <cmd id=\"BACK\" />\n")
        nodedef.write("        <cmd id=\"REPLAY\" />\n")
        nodedef.write("        <cmd id=\"INFO\" />\n")
        nodedef.write("        <cmd id=\"BACKSPACE\" />\n")
        nodedef.write("        <cmd id=\"SEARCH\" />\n")
        nodedef.write("        <cmd id=\"ENTER\" />\n")
        nodedef.write("        <cmd id=\"LAUNCH\">\n")
        nodedef.write(LAUNCH_TMPL % (no_apps, node_id, 'GV1'))
        nodedef.write("        </cmd>\n")
        if roku_list[rk]['isTV']:
            nodedef.write("        <cmd id=\"VOLUP\" />\n")
            nodedef.write("        <cmd id=\"VOLDOWN\" />\n")
            nodedef.write("        <cmd id=\"MUTE\" />\n")
            nodedef.write("        <cmd id=\"CHNLUP\" />\n")
            nodedef.write("        <cmd id=\"CHNLDOWN\" />\n")
            nodedef.write("        <cmd id=\"OFF\" />\n")
            nodedef.write("        <cmd id=\"TUNER\" />\n")
            nodedef.write("        <cmd id=\"HDMI1\" />\n")
            nodedef.write("        <cmd id=\"HDMI2\" />\n")
            nodedef.write("        <cmd id=\"HDMI3\" />\n")
            nodedef.write("        <cmd id=\"HDMI4\" />\n")
            nodedef.write("        <cmd id=\"AV\" />\n")
        nodedef.write("      </accepts>\n")
        nodedef.write("    </cmds>\n")
        nodedef.write("  </nodeDef>\n\n")

    nodedef.write("</nodeDefs>\n")

    nodedef.close()

