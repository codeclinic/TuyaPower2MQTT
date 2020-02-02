#from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'tuyapower2mqtt',         # How you named your package folder (MyLib)
  packages = ['tuyapower2mqtt'],   # Chose the same as "name"
  version = '1.1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Reports all the power stats & on/off state from a Tuya / SmartLife / Jinvoo WiFI smart devices such as a socket or switch including newer v3.3 protocol devices, then sends them as JSON via MQTT',   # Give a short description about your library
  author = 'Phill Healey',                   # Type in your name
  author_email = 'phill@codeclinic.de',      # Type in your E-Mail
  url = 'https://github.com/codeclinic/TuyaPower2MQTT',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/codeclinic/TuyaPower2MQTT/archive/1.1.3.tar.gz',    # I explain this later on
  long_description=long_description,
  long_description_content_type='text/markdown',
  keywords = ['TUYA', 'POWER', 'STATS', 'DATA', 'REPORTING', 'SWITCH', 'SOCKET', 'OUTLET', 'SMARTLIFE', 'JINVOO', 'WIFI', 'SMARTDEVICE', 'SMART', 'HOME','AUTOMATION'],   # Keywords that define your package best
  install_requires=[            # dependencies
          'pycryptodome',
          'pytuya',
          'paho-mqtt',
          'datetime',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)