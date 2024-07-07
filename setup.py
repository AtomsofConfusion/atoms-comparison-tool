from setuptools import setup, find_packages

setup(
    name='AtomsComparsionTool',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'compare = src.__main__:main',
        ],
    },
)