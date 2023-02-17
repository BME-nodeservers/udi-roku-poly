import udi_interface
import requests
from xml.etree import ElementTree

LOGGER = udi_interface.LOGGER

class RokuNode(udi_interface.Node):
    # class variables

    def __init__(self, polyglot, primary, address, name, ip, apps, node_id):
        self.id = node_id
        self.poly = polyglot
        self.ip = ip
        self.apps = apps

        # call the default init
        super(RokuNode, self).__init__(polyglot, primary, address, name)

        polyglot.subscribe(polyglot.POLL, self.poll)
        polyglot.subscribe(polyglot.START, self.start, address)
        polyglot.subscribe(polyglot.STOP, self.stop)

    def start(self):
        self.active = self.active_app()
        self.update_status(self.active)
        self.setDriver('ST', 1, True, True)

    def poll(self, pollflag):
        if 'shortPoll' in pollflag:
            self.active = self.active_app()
            self.update_status(self.active)

    def stop(self):
        self.setDriver('ST', 0, True, True)

    def refresh(self, app_list):
        self.apps = app_list

    def update_status(self, app_id):
        self.active = app_id
        self.setDriver('GV2', app_id, report=True, force=True)
        if app_id in self.apps:
            self.setDriver('GV1', self.apps[app_id][1], report=True, force=True)
        elif app_id == '562859':
            # new screen saver app id
            self.setDriver('GV1', self.apps['0'][1], report=True, force=True)
        else:
            LOGGER.error('App id {} is not mapped to an appliction.'.format(app_id))

    # Find the current active application, return it's address or ''
    def active_app(self):
        url = self.ip + 'query/active-app'
        try:
            r = requests.get(url)
        except Exception as e:
            LOGGER.error(str(e))
            LOGGER.error(e)
            return 0

        tree = ElementTree.fromstring(r.content)
        for child in tree.iter('*'):
            if child.tag == 'app':
                if child.text == 'Roku':
                    return '0'
                elif 'id' in child.attrib:
                    return child.attrib['id']
                else:
                    return '0'
        return '0'

    def launch(self, command):
        LOGGER.debug('Launch app ' + self.name + "/" + command['value'])
        LOGGER.debug(command)
        # need to convert value (count) into app ID.  self.apps[appid] = (name, count)
        for appid in self.apps:
            if self.apps[appid][1] == int(command['value']):
                LOGGER.info('Launching ' + self.apps[appid][0])
                url = self.ip + 'launch/' + str(appid)
                r = requests.post(url);
                self.update_status(appid)
                return

    def remote(self, command):
        LOGGER.info('Send Remote button ' + command['address'])
        url = self.ip + 'keypress/' + command['cmd']
        r = requests.post(url);
        LOGGER.debug ('requests: ' + r.reason);

        if command['cmd'] == 'HOME':
            self.update_status('0')


    commands = {
            'HOME': remote,
            'REV': remote,
            'FWD': remote,
            'PLAY': remote,
            'SELECT': remote,
            'LEFT': remote,
            'RIGHT': remote,
            'DOWN': remote,
            'UP': remote,
            'BACK': remote,
            'REPLAY': remote,
            'INFO': remote,
            'BACKSPACE': remote,
            'SEARCH': remote,
            'ENTER': remote,
            'LAUNCH': launch
            }
    drivers = [
            {'driver': 'ST', 'value': 0, 'uom': 2},    # Active or not
            {'driver': 'GV1', 'value': 0, 'uom': 25},  # Current  application
            {'driver': 'GV2', 'value': 1, 'uom': 56},  # Current application id
            ]

    
class RokuNodeTV(RokuNode):
    def __init__(self, polyglot, primary, address, name, ip, apps, node_id):
        self.id = node_id
        self.poly = polyglot
        self.ip = ip
        self.apps = apps

        super(RokuNode, self).__init__(polyglot, primary, address, name)

        polyglot.subscribe(polyglot.POLL, self.poll)
        polyglot.subscribe(polyglot.START, self.start, address)
        polyglot.subscribe(polyglot.STOP, self.stop)

    def remote(self, command):
        LOGGER.info('TV:: Send Remote button ' + command['address'])
        url = self.ip + 'keypress/' + command['cmd']
        r = requests.post(url);
        LOGGER.debug ('requests: ' + r.reason);

        if command['cmd'] == 'HOME':
            self.update_status('0')
        #RokuNode.remote(command)

    def launch(self, command):
        LOGGER.debug('Launch app ' + self.name + "/" + command['value'])
        LOGGER.debug(command)
        # need to convert value (count) into app ID.  self.apps[appid] = (name, count)
        for appid in self.apps:
            if self.apps[appid][1] == int(command['value']):
                LOGGER.info('Launching ' + self.apps[appid][0])
                url = self.ip + 'launch/' + str(appid)
                r = requests.post(url);
                self.update_status(appid)
                return

    commands = {
            'HOME': remote,
            'REV': remote,
            'FWD': remote,
            'PLAY': remote,
            'SELECT': remote,
            'LEFT': remote,
            'RIGHT': remote,
            'DOWN': remote,
            'UP': remote,
            'BACK': remote,
            'REPLAY': remote,
            'INFO': remote,
            'BACKSPACE': remote,
            'SEARCH': remote,
            'ENTER': remote,
            'VOLUP': remote,
            'VOLDOWN': remote,
            'CHNLUP': remote,
            'CHNLDOWN': remote,
            'MUTE': remote,
            'OFF': remote,
            'TUNER': remote,
            'HDMI1': remote,
            'HDMI2': remote,
            'HDMI3': remote,
            'HDMI4': remote,
            'AV': remote,
            'LAUNCH': launch
            }
    drivers = [
            {'driver': 'ST', 'value': 0, 'uom': 2},    # Active or not
            {'driver': 'GV1', 'value': 0, 'uom': 25},  # Current  application
            {'driver': 'GV2', 'value': 1, 'uom': 56},  # Current application id
            ]
