#!/usr/bin/env python
#########################################################################
# Copyright 2014 Marcel Tiews marcel.tiews@gmail.com
#########################################################################
# Helios-Plugin for SmartHome.py. http://mknx.github.io/smarthome/
#
# This plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this plugin. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import sys
import logging
import http.client
import xml.etree.cElementTree

logger = logging.getLogger("")


class PoweroneException(Exception):
    pass

class PoweroneBase():
    def __init__(self, host='localhost'):
        self._host = host
        
    def _readvalues(self):
        values = {}
        content = self._get_plantxml()
        if content is None:
            return None
        
        contentXML = xml.etree.cElementTree.fromstring(content)
        
        self._pushvaluefromxml(values, 'sun', contentXML, '.','sun')  
        self._pushvaluefromxml(values, 'alarmstate', contentXML, 'eth/inv','alarmstate')  
        self._pushvaluefromxml(values, 'status', contentXML, 'eth/inv','status')  
        
        self._pushvaluefromxml(values, 'vgrid', contentXML, 'eth/inv','vgrid')  
        self._pushvaluefromxml(values, 'igrid', contentXML, 'eth/inv','igrid')  
        self._pushvaluefromxml(values, 'fgrid', contentXML, 'eth/inv','fgrid')  
        self._pushvaluefromxml(values, 'pout_KW', contentXML, 'eth/inv','pout_KW')  
        
        self._pushvaluefromxml(values, 'vin1', contentXML, 'eth/inv','vin1')  
        self._pushvaluefromxml(values, 'iin1', contentXML, 'eth/inv','iin1')  
        self._pushvaluefromxml(values, 'pin1', contentXML, 'eth/inv','pin1')  
        
        self._pushvaluefromxml(values, 'vin2', contentXML, 'eth/inv','vin2')  
        self._pushvaluefromxml(values, 'iin2', contentXML, 'eth/inv','iin2')  
        self._pushvaluefromxml(values, 'pin2', contentXML, 'eth/inv','pin2')  
        
        self._pushvaluefromxml(values, 'eday_KWh', contentXML, 'eth/inv','eday_KWh')  
        self._pushvaluefromxml(values, 'eweek_KWh', contentXML, 'eth/inv','eweek_KWh')  
        self._pushvaluefromxml(values, 'emonth_KWh', contentXML, 'eth/inv','emonth_KWh')  
        self._pushvaluefromxml(values, 'eyear_KWh', contentXML, 'eth/inv','eyear_KWh')  
        self._pushvaluefromxml(values, 'etot_KWh', contentXML, 'eth/inv','etot_KWh')  
        
        return values
	
    def _pushvaluefromxml(self, values, valuename, xml, elementpath, attribute = None):
        element = xml.find(elementpath)
        if element is not None:
            if attribute is None:
                values[valuename] = element.text
            else:
                aval = element.get(attribute)
                if aval is not None:
                    values[valuename] = element.get(attribute)
                
    
    def _get_plantxml(self):
        connection = http.client.HTTPConnection(self._host, timeout=2)
        try:
            connection.request("GET", '/plant.xml')
        except Exception as e:
            logger.warning("Error fetching plant xml: {0}".format(e))
            connection.close()
            return None
        response = connection.getresponse()
        if response.status == 200:
            content = response.read()
        else:
            logger.warning("Error fetching plant xml: {0} {1}".format(response.status, response.reason))
            content = None
        connection.close()
        return content
    
class Powerone(PoweroneBase): 
    _items = {}
    
    def __init__(self, smarthome, host, cycle=300):
        PoweroneBase.__init__(self, host)
        self._sh = smarthome
        self._cycle = int(cycle)
        self._alive = False
        
    def run(self):
        self._alive = True
        self._sh.scheduler.add('Powerone', self._update, cycle=self._cycle)

    def stop(self):
        self._alive = False

    def parse_item(self, item):
        if 'powerone_var' in item.conf:
            self._items[item.conf['powerone_var']] = item
                
    def _update(self):
        logger.debug("Powerone: Updating values")
        values = self._readvalues()
        for valname in values.keys():
            if valname in self._items.keys():
                self._items[valname](values[valname],"Powerone")
   
def main():
    import argparse 
    
    parser = argparse.ArgumentParser(
    description="Helios ventilation system commandline interface.",
    epilog="Without arguments all readable values using default ip will be retrieved.",
    argument_default=argparse.SUPPRESS)
    parser.add_argument("-s", "--host", dest="host", default="127.0.0.1", help="Host to use")
    parser.add_argument("-d", "--debug", dest="enable_debug", action="store_true", help="Prints debug statements.")
    args = vars(parser.parse_args())
 
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    if "enable_debug" in args.keys():
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    try:
        powerone = PoweroneBase(args["host"])
        values = powerone._readvalues()
        if values != None:
            print("Inverter values:")
            for var in values.keys():
                print("   {0}: {1}".format(var,values[var]))
    except Exception as e:
        print("Exception: {0}".format(e))

        return 1

if __name__ == "__main__":
    sys.exit(main())        
