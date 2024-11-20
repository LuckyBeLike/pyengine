from setuptools import setup, find_packages

setup(
    name='pyengine',
    version='1.0.0',
    description='A Python library for game development',
    author='LuckyBeLike',
    author_email=thebeezzzzzz@gmail.com',
    url='https://github.com/LuckyBeLike/pyengine',
    packages=find_packages(),
    install_requires=[
        'pygame',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
