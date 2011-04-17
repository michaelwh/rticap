from setuptools import setup, find_packages
setup(
    name = "rticap",
    version = "0.1",
    packages = find_packages(),
    install_requires=[
        'setuptools',
        'PySide',
        'pyusb'
      ],
)