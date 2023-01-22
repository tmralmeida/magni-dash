from setuptools import setup, find_namespace_packages

setup(
    name="magni_dash",
    version="0.1.0",
    description="Dashboard for Magni dataset",
    license="MIT",
    author="Tiago Rodrigues de Almeida",
    author_email="tmr.almeida96@gmail.com",
    python_requires="==3.10.8",
    url="https://github.com/tmralmeida/magni-dash",
    packages=find_namespace_packages(exclude=["tests", ".tests", "tests_*", "scripts"]),
)
