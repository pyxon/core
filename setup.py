import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micropy-core",
    version="0.0.1",
    author="Pavel V. Pristupa",
    author_email="pristupa@gmail.com",
    description="Core components of MicroPy framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micropy/core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        'persipy==1.0.0',
        'winter==2.3.1',
    ],
)
