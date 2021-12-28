import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gfs_basic',
    version=attr: gfs_basic.__version__
    author = Lynn Pickering
    author_email = pickerln@mail.uc.edu,
    description='Basic genetic fuzzy systems code',
    long_description=file: README.md
    url='https://github.com/pickerln/GFS_basic',
    license='MIT',
    packages=['gfs_basic'],
    
    [options]
    zip_safe = True
    package_dir=
        =src
    packages = find:
    python_requires = >=3.6

    [options.packages.find]
    where=src
)

