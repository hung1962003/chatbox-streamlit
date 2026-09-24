import setuptools
from pathlib import Path


def readme():
    return Path(__file__).parent.absolute().joinpath("README.md").read_text("utf-8")


setuptools.setup(
    name="streamlit-chatbox",
    version="1.1.13.post1",
    author="David Nguyen",
    author_email="315294890+davidnguyen1601@users.noreply.github.com",
    description="A chat box and helpers to build Streamlit chatbot apps",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/davidnguyen1601/streamlit-chatbox",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Streamlit",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.26.0",
        "simplejson",
        "streamlit-feedback",
        "streamlit-markdown>=1.0.9",
    ],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
)
