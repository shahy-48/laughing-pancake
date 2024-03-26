from setuptools import setup, find_packages

def get_requirements(filename:str)->list[str]:
    """Read requirements file and return as list of strings"""
    requirements = []
    with open(filename, 'r') as f:
        # read each and storing them as one of list objects
        requirements = f.readlines()
        # removing new line characters from each package name   
        requirements = [req.replace('\n','') for req in requirements]
        # Added this condition to remove the local package installation
        # '-e .' is added into requirements file when we are installing the package in editable mode
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements

setup(
    name='ml_projects',
    version='0.1',
    author='Yash',
    author_email='shahy.data04@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)