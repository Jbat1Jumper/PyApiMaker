from distutils.core import setup

setup(
    name='PyApiMaker',
    version='0.1.1',
    author='Nikita Zdanovitch',
    author_email='nzdanovitch@dc.uba.ar',
    packages=['pyapimaker'],
    url='https://github.com/Jbat1Jumper/PyApiMaker.git',
    license='LICENSE.txt',
    description='Provides utilities to manage and interact with your code.',
    long_description=open('README.rst', 'r').read(),
    install_requires=["flask"
    ],
)
