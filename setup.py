from setuptools import setup

setup(
    name = "spybatch",
    version = "0.1",
    description = "Python wrapper for resolving dependencies and submitting jobs to a SLURM job scheduler",
    url = "https://github.com/kkchau/spybatch",
    author = "Kevin Chau",
    author_email = "kkhaichau@gmail.com",
    license = "GPLv3+",
    packages = ["spybatch"],
    zip_safe = False,
    entry_points = {
        "console_scripts": 
        ["spybatch = spybatch:main"]
    },
    install_requires = ["pyyaml"]
)