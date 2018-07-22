****************************
Mopidy-serialRFID
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-serialRFID.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-serialRFID/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/tulip85/modpiy-serialRFID/master.svg?style=flat
    :target: https://travis-ci.org/tulip85/modpiy-serialRFID
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/tulip85/modpiy-serialRFID/master.svg?style=flat
   :target: https://coveralls.io/r/tulip85/modpiy-serialRFID
   :alt: Test coverage

Mopidy extension for Foobar mechanics


Installation
============

Install by running::

    pip install Mopidy-serialRFID

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-serialRFID to your Mopidy configuration file::

    [serialRFID]
    enabled = true
	device = /dev/ttyAMA0
	rate = 9600
	button = 40
	oled_enabled = true
	oled_bus = 1
	oled_address = 0x3c
	oled_driver = ssd1306


Project resources
=================

- `Source code <https://github.com/tulip85/mopidy-serialrfid>`_
- `Issue tracker <https://github.com/tulip85/mopidy-serialrfid/issues>`_


Credits
=======

- Original author: `tulip <https://github.com/tulip85`__
- Current maintainer: `tulip <https://github.com/tulip85`__
- `Contributors <https://github.com/tulip85/mopidy-serialrfid/graphs/contributors>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.