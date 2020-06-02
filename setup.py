"""Setup for the medmentionsreader package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Tom Oberhauser",
    author_email="tom.oberhauser@beuth-hochschule.de",
    name='medmentionsreader',
    license='',
    description='MedMentionsReader is a module for reading the MedMentions dataset',
    version='0.2.0',
    long_description=README,
    url='https://github.com/DATEXIS/MedMentionsReader',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['tqdm'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)