from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='django_http_exceptions',
    version='1.3.0',
    packages=['django_http_exceptions'],
    url='https://github.com/isik-kaplan/django_http_exceptions',
    description="django raisable http exceptions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='APGL-3.0',
    author='isik-kaplan',
    author_email='',
    python_requires=">=3.5",
    install_requires=['django>=2.0']
)
