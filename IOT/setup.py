from setuptools import setup, find_packages

setup(
    name='iot_app',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'iot_app=iot_app.main:main',
        ],
    },
)
