import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gfs_basic',
    version='1.0.0',
    author = 'Lynn Pickering',
    author_email = 'pickerln@mail.uc.edu',
    description='Basic genetic fuzzy systems code',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pickerln/GFS_basic',
    project_urls = {
            "Bug Tracker": "https://github.com/pickerln/gfs_basic/issues"
        },
    license='MIT',
    packages=['gfs_basic'],
)

