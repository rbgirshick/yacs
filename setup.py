from setuptools import setup

setup(
    name="yacs",
    version="0.1.5",
    author="Ross Girshick",
    author_email="ross.girshick@gmail.com",
    description="Yet Another Configuration System",
    url="https://github.com/rbgirshick/yacs",
    packages=["yacs"],
    long_description="A simple experiment configuration system for research",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=["PyYAML"],
)
