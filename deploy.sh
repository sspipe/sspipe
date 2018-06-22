#!/bin/bash
rm -r dist/ build/; python setup.py sdist bdist_wheel && twine upload dist/*
