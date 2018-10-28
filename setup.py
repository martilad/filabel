from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = ''.join(f.readlines())


setup(
    name='filabel_martilad',
    version='0.3',
    description='Tool for labeling PRs at GitHub by globs.',
    long_description=long_description,
    author='Ladislav Martínek',
    author_email='martilad@fit.cvut.cz',
    keywords='GitHub, PRs, labels, GitHubAPI',
    license='MIT',
    url='https://github.com/martilad/filabel',
    packages=find_packages(),
    package_data={
        'filabel': [
            'static/*.css',
            'templates/*.html',
            '../test/fixtures/*'
        ]
    },
    entry_points={
        'console_scripts': [
            'filabel = filabel:main',
        ]
    },
    install_requires=[
        'flask', 
        'configparser', 
        'click', 
        'requests'],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest'
    ],
    classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Development Status :: 4 - Beta',
        ],
    zip_safe=False,
)