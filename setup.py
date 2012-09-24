from setuptools import setup

setup(
    name = "test-runner",
    version = "0.0.1",
    author = "Paul Hobbs",
    description = ("A simple doit post-commit hook for",
                   "running integration tests and notifying."),
    license = "BSD",
    packages=['test_runner'],
    install_requires=['doit'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
