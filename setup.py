import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jacow_validator",
    version="0.0.1",
    author="Australian Synchrotron",
    author_email="ascidev@synchrotron.org.au",
    description="Validate JACoW docx proceedings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AustralianSynchrotron/jacow-validator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 3 Clause",
        "Operating System :: OS Independent",
    ],
)
