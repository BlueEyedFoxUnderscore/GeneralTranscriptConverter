from setuptools import setup, find_packages

setup(
    name="generaltranscriptconverter",
    version="0.1.1",
    description="A python script that translates between RUMBLE VR notations.",
    license="MIT",
    author="Oxity",
    author_email="oxityy@proton.me",
    include_package_data=True,
    package_data={
        "gtc": ["notation_systems/*.json"],
    },
)
