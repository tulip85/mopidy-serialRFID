from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext
import tornado.web

__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-serialRFID'
    ext_name = 'serialRFID'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['device'] = config.String()
        schema['rate'] = config.Integer()
        schema['button'] = config.Integer()
        schema['oled_bus'] = config.Integer()
        schema['oled_address'] = config.String()
        schema['oled_enabled'] = config.Boolean()
        schema['oled_driver'] = config.String()
        return schema
        

    def setup(self, registry):
        from .frontend import serialRFID
        registry.add('frontend', serialRFID)
        
        registry.add('http:app', {
            'name': self.ext_name,
            'factory': my_app_factory,
        })
        
def my_app_factory(config, core):
    from .webapp import CSVTable, RFIDManager

    path = os.path.join( os.path.dirname(__file__), 'static')
 
    return [
        ('/csvTable', CSVTable, {'config':config,'core': core}),
        ('/getRFIDKey', RFIDManager, {'config':config,'core': core}),
        (r'/(.*)', tornado.web.StaticFileHandler, {
            'path': path,
            'default_filename': 'index.html'
        })
    ]