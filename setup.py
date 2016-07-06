"""
justbackoff
----------------

Simple backoff algorithm in Python
"""
from setuptools import setup


setup(
    name='justbackoff',
    version='0.3.0',
    url='https://github.com/admiralobvious/justbackoff',
    license='MIT',
    author='Alexandre Ferland',
    author_email='aferlandqc@gmail.com',
    description='Simple backoff algorithm in Python',
    long_description=__doc__,
    packages=['justbackoff'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
