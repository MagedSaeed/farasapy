import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="farasapy",
    version="0.0.10",
    author="MagedSaeed",
    author_email="mageedsaeed1@gmail.com",
    description="A Python Wrapper for the well Farasa toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MagedSaeed/farasapy",
    packages=["farasa"],
    package_dir={"farasa": "farasa"},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Text Processing :: Linguistic",
        "Natural Language :: Arabic",
        "Intended Audience :: Science/Research",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
    install_requires=["requests", "tqdm",],
)

# scripts=['farasa/__init__.py','farasa/farasa_bin/*','farasa/farasa_bin/lib/*','farasa/tmp/*'],
