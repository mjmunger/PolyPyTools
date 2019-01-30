import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="poly_py_tools",
    version="2.0.2",
    author="Michael Munger",
    author_email="mj@hp.io",
    description="A package for working with Asterisk and Polycom config files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mjmunger/PolyPyTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
        "Environment :: Console"
    ],
)