from setuptools import setup, find_packages

setup(
    name='wiggler-project',
    version='0.0.a1',
    description=("A Wiggler Project"),
    packages=find_packages(),
#    package_data={
#        'wiggler': ['resources/*/*',
#                    'resources/*.yaml'],
#    },
    data_files=[ ("lib/wiggler", ["assets/*"] )],
    entry_points={
        'console_scripts': [
            'wiggler-project=wiggler_project.engine.main:main',
        ],
    },
    include_package_data=True,
)
