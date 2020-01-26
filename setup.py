from setuptools import setup, find_packages

setup(
    name='vaultssh',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'hvac',
    ],
    entry_points='''
        [console_scripts]
        vssh=vaultssh.vaultssh:main
    ''',
)