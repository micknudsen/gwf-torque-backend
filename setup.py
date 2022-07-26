from setuptools import setup, find_packages

setup(

    name='gwf-torque-backend',
    version='0.0',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.6',

    install_requires=[
    ],

    entry_points={
        'gwf.backends': [
            'torque = gwf_torque_backend:Torque',
        ]
    },

    author='Michael Knudsen',
    author_email='michaelk@clin.au.dk',
    license='MIT'

)
