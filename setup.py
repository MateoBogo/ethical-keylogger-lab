from setuptools import setup, find_packages

setup(
    name='ethical-keylogger',
    version='1.0.0',
    description='Un keylogger éthique multiplateforme pour des fins éducatives et de tests de sécurité.',
    author='mateo',
    packages=find_packages(),
    py_modules=['EthicalKeylogger', 'test_logger'],
    install_requires=[
        'pynput==1.4',
        'clipboard==0.0.4',
        'PyAutoGUI==0.9.44',
        'requests==2.21.0'
    ],
    entry_points={
        'console_scripts': [
            'ethical-keylogger = EthicalKeylogger:main'
        ]
    },
)
