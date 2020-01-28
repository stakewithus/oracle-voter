from setuptools import setup, find_namespace_packages

setup(
    name="oracle_voter",
    version="0.1.5-alpha",
    packages=find_namespace_packages(),
    py_modules=["oracle_voter"],
    entry_points={
        "console_scripts": [
            "oracle_voter=oracle_voter.main:main"
        ]
    },
    zip_safe=True,
)
