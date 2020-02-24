import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyxon",
    version="0.0.2",
    author="Pavel V. Pristupa",
    author_email="pristupa@gmail.com",
    description="Pyxon framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyxon/core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6, <3.7",
    install_requires=[
        "injector==0.15.0",
        "persipy==1.0.0",
        "winter==2.3.1",
    ],
)
