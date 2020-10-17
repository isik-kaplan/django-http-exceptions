from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='django_http_exceptions',
    version='1.4.0',
    packages=['django_http_exceptions'],
    url='https://github.com/isik-kaplan/django_http_exceptions',
    description="django raisable http exceptions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT LICENSE',
    author='isik-kaplan',
    author_email='',
    python_requires=">=3.5",
    install_requires=['django>=2.0'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
    ],
)
