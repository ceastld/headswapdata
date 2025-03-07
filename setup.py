from setuptools import setup

setup(
    name='headswapdata',
    version='0.1',
    packages=['expdataloader'],
    package_dir={'expdataloader': 'expdataloader'},
    install_requires=[
        'natsort',
        'Pillow',
        'opencv-python'
    ]
)
