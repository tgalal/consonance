# -*- coding: utf-8 -*-
import consonance
from setuptools import find_packages, setup

setup(
    name='consonance',
    version=consonance.__version__,
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=['dissononce>=0.34.3', 'python-axolotl-curve25519', 'transitions', 'protobuf'],
    license='GPL-3+',
    author='Tarek Galal',
    author_email='tare2.galal@gmail.com',
    description="WhatsApp's handshake implementation using Noise Protocol",
    long_description="This library implements WhatsApp's handshake process which makes use of "
                     "Noise Pipes with Curve25519, AES-GCM, and SHA256 from Noise Protocol",
    platforms='any',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Topic :: Security :: Cryptography',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
