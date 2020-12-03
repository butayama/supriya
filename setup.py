#!/usr/bin/env python
import pathlib
from distutils.version import LooseVersion
from setuptools import setup, Extension

package_name = "supriya"


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / package_name / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


version = read_version()

with open("README.rst", "r") as file_pointer:
    long_description = file_pointer.read()


if __name__ == "__main__":
    setup(
        author="Josiah Wolf Oberholtzer",
        author_email="josiah.oberholtzer@gmail.com",
        classifiers=[
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: MacOS",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Artistic Software",
            "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        ],
        description="A Python API for SuperCollider",
        extras_require={
            "ipython": [
                "jupyter",
                "jupyter_contrib_nbextensions",
                "jupyter_nbextensions_configurator",
                "rise",
            ],
            "test": [
                "black == 19.10b0",  # Trailing comma behavior in 20.x needs work
                "flake8",
                "isort",
                "mypy >= 0.720",
                "pytest >= 5.4.0",
                "pytest-asyncio >= 0.14.0",
                "pytest-cov >= 2.10.0",
                "pytest-helpers-namespace >= 2019.1.8",
                "pytest-mock",
                "pytest-rerunfailures >= 9.0",
                "pytest-timeout >= 1.4.0",
            ],
        },
        ext_modules=[
            Extension(
                'supriya.realtime.shm.server_shm',
                language="c++",
                sources=['supriya/realtime/shm/server_shm.pyx'],
            )
        ],
        include_package_data=True,
        install_requires=[
            "PyYAML",
            "setuptools>=18.0",
            "appdirs",
            "cython",
            "tqdm",
            "uqbar >= 0.5.2",
        ],
        keywords=[
            "audio",
            "dsp",
            "music composition",
            "scsynth",
            "supercollider",
            "synthesis",
        ],
        license="MIT",
        long_description=long_description,
        name=package_name,
        packages=[package_name],
        url=f"https://github.com/josiah-wolf-oberholtzer/{package_name}",
        version=version,
        zip_safe=False,
    )
