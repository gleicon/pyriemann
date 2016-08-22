rpm:
	python setup.py bdist_rpm --requires protobuf-python --build_requires protobuf-compiler

clean:
	python setup.py clean


