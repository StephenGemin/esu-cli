from setuptools import setup, find_packages

setup(
    name="esu_cli",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Everyday script utilities CLI; simplify tedious tasks with automation",
    author="Stephen Gemin",
    author_email="s.gemin88@gmail.com",
    url="https://github.com/StephenGemin/esu-cli",
    packages=find_packages(include=["esu_cli"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "click",
        "click_log",
        "click_spinner",
        "gitpython",
        "pygithub",
        "pyyaml",
        "colorama; platform_system == 'Windows'",
        "importlib_metadata; python_version < '3.8'",
    ],
    entry_points={"console_scripts": ["esu=esu_cli.cli:main"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
