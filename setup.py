from setuptools import setup, find_packages

setup(

    name='gwf-torque-backend',
    version='0.1',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.6',

    install_requires=[
        'gwf>=1.7.1',
        # gwf 1.x imports pkg_resources at runtime.
        'setuptools<85',
    ],

    entry_points={
        'gwf.backends': [
            'torque = gwf_torque_backend.torque:TorqueBackend',
        ]
    },

    author='Michael Knudsen',
    author_email='michaelk@clin.au.dk',
    license='MIT'

)
