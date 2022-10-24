#!/usr/bin/env python3
"""
Polyglot v3 node server experimental Roku Media Player control.
Copyright (C) 2019,2021 Robert Paauwe

Control class.  

Using the longPoll interval, do device discovery and update the device
nodes if necessary.
"""
import udi_interface
import sys
import json
import time
import write_profile as profile
from nodes import roku_node
from roku_scanner.scanner import Scanner
from roku_scanner.roku import Roku

LOGGER = udi_interface.LOGGER

class Controller(object):
    def __init__(self, polyglot):
        self.poly = polyglot
        self.roku_list = {}
        self.n_queue = []

        polyglot.subscribe(polyglot.ADDNODEDONE, self.done_queue)
        polyglot.subscribe(polyglot.POLL, self.poll)
        polyglot.setCustomParamsDoc()
        polyglot.ready()

        self.start()


    def start(self):
        LOGGER.info('Starting node server')
        # Do initial device discovery on start
        self.discover()
        LOGGER.info('Node server started')

    def poll(self, pollflag):
        if 'longPoll' in pollflag:
            self.discover()

    def done_queue(self, n_data):
        self.n_queue.append(n_data['address'])

    def wait_for_node_done(self):
        while len(self.n_queue) == 0:
            time.sleep(0.2)
        self.n_queue.pop()


    # Update or create the node associated with device 'dev'
    def updateNode(self, dev, apps, ip):
        address = dev['serial-number']

        # if new device, Create entry for it
        if address not in self.roku_list:
            LOGGER.info('Found new Roku device {}'.format(dev['user-device-name']))
            node_id = 'roku_{}'.format(ip.split('.')[3].split(':')[0])
            name = self.poly.getValidName(dev['user-device-name'])
            self.roku_list[address] = {
                    'name': name,
                    'ip': ip,
                    'configured': False,
                    'apps': None,
                    'node_id': node_id,
                    'count': 0,
                    'isTV': True if dev['is-tv'] == 'true' else False
                    }

        # Update the NLS map for device
        nls_map = {}
        cnt = 1
        for app in apps['app']:
            if app['@type'] == 'appl' or app['@type'] == 'tvin':
                name = app['#text'].replace('&', 'and')
                nls_map[app['@id']] = (name, cnt)
                cnt += 1
        nls_map['0'] = ('Screensaver', 0)
        self.roku_list[address]['apps'] = nls_map
        self.roku_list[address]['count'] = cnt

        # write profile files to ISY
        profile.write_nls(LOGGER, self.roku_list)
        profile.write_nodedef(LOGGER, self.roku_list)
        self.poly.updateProfile()

        for rk in self.roku_list:
            rd = self.roku_list[rk]
            addr = rk[-6:-1:1].lower()
            if not rd['configured']:
                LOGGER.error('Is TV = {}'.format(rd['isTV']))
                if rd['isTV']:
                    LOGGER.error('Adding Roku TV node {}'.format(addr))
                    node = roku_node.RokuNodeTV(self.poly, addr, addr, rd['name'], rd['ip'], rd['apps'], rd['node_id'])
                else:
                    LOGGER.error('Adding Roku node {}'.format(addr))
                    node = roku_node.RokuNode(self.poly, addr, addr, rd['name'], rd['ip'], rd['apps'], rd['node_id'])

                self.poly.addNode(node)
                self.wait_for_node_done()
                rd['configured'] = True

            # refresh the node's application list 
            node = self.poly.getNode(addr)
            node.refresh(rd['apps'])


    # Create the nodes for each device configured and query
    # to get the list of installed applications.  
    def discover(self):
        LOGGER.info("In Discovery...")

        scanner = Scanner(discovery_timeout=3)
        scanner.discover()
        for roku_dev in scanner.discovered_devices:
            roku_location = roku_dev.get('LOCATION')
            roku = Roku(location=roku_location, discovery_data=roku_dev)
            roku.fetch_data()
            r = roku.data['device_info']['data']['device-info']
            apps = roku.data['apps']['data']['apps']

            LOGGER.info('Discovered {} - {}'.format(r['user-device-name'], r['user-device-location']))

            # Have we already configured this device?
            sn = r['serial-number']
            if sn in self.roku_list:
                # Has the number of apps changed?
                if len(apps['app']) != self.roku_list[sn]['count']:
                    self.updateNode(r, apps, roku_location)
            else:
                self.updateNode(r, apps, roku_location)

        LOGGER.info("Discovery finished")

    # Delete the node server from Polyglot
    def delete(self):
        LOGGER.info('Removing node server')

    def stop(self):
        LOGGER.info('Stopping node server')

