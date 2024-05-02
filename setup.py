from setuptools import find_packages, setup


def parse_requirements(filename):
  """load requirements from a pip requirements file."""
  with open(filename) as f:
    lineiter = (line.strip() for line in f)
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    name="RFEM Matlab Exchange",
    version="0.1.0",
    description=(
        "Exchange interface between dlubal rfem and matlab"
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Technische Hochschule Ostwestfalen-Lippe",
    url="https://github.com/pak9819/RFEM-Matlab-Exchange",
    packages=find_packages(exclude="benchmarks"),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: Windows",
    ],
    python_requires=">=3.10",
    install_requires=parse_requirements("requirements.in"),
)