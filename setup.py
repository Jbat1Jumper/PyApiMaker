from distutils.core import setup

setup(
    name='PyApiMaker',
    version='0.1.0',
    author='Nikita Zdanovitch',
    author_email='nzdanovitch@dc.uba.ar',
    packages=['pyapimaker'],
    url=None,
    license='LICENSE.txt',
    description='Provides utilities to manage and interact with your code.',
    long_description=open('README.rst').read(),
    install_requires=["flask"
    ],
)