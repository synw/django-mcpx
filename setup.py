import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-mcpx",
    version="0.1.1",
    author="synw",
    author_email="synwe@yahoo.com",
    description="A Django package for MCP authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/synw/django-mcpx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    python_requires=">=3.6",
    install_requires=["fastmcp"],
)
