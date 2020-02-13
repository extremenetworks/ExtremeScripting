import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

module_list = ['SLX_BitMap', 'SLX_IntfTypeMap', 'SLX_TunnelTypeMap',
               'SLXRSpeedMap', 'SLXSSpeedMap', 'SLX_PortData',
               'SLX_PortMapping', 'IfIndex', 'SLX_IfIndex_Core',
               'Slx9850_IfIndex', 'Slx9640_IfIndex', 'Slx9540_IfIndex',
               'Slx9250_IfIndex', 'Slx9240_IfIndex', 'Slx9150_IfIndex',
               'Slx9140_IfIndex', 'Slx9030_IfIndex', 'Slx_IfIndex']

setuptools.setup(
    name='slx_ifindex_gen',
    version='0.0.3',
    author='any mouse',
    author_email='any.mouse@extremenetworks.com',
    description='Offline SNMP ifindex generator for Extreme SLX devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/extremenetworks/ExtremeScripting',
    scripts=['build/bin/slx_ifindex_gen.py'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Enviroment :: Console'
    ],
    python_requires='>=3.4',
)
