import setuptools

setuptools.setup(
    name="ursadb",
    version="1.0",
    author="msm",
    author_email="msm@tailcall.net",
    description="ursadb",
    url="https://github.com/CERT-Polska/ursadb-cli",
    packages=["ursadb"],
    scripts=['bin/ursaclient'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyzmq",
        "tabulate"
    ]
)
