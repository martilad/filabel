from setuptools import setup


with open('README.md') as f:
    long_description = ''.join(f.readlines())


setup(
    name='filabel_martilad',
    version='0.1',
    description='Tool for labeling PRs at GitHub by globs.',
    long_description=long_description,
    author='Ladislav Martínek',
    author_email='martilad@fit.cvut.cz',
    keywords='GitHub, PRs, labels',
    license='MIT',
    url='https://github.com/martilad/filabel',
    packages=['filabel'],
    install_requires=['flask', 'configparser', 'click', 'requests'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
        ],
    },
)