import setuptools

with open("README.txt", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="Atoms Comparsion Tool CLI",
    version="0.0.1",
    author="Atoms of Confusion team",
    author_email="",
    description=("The command line interface version of the orginal tool"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["pandas", "typer"],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "ATC-Comparsion = src.__main__:main",
        ]
    }   
)