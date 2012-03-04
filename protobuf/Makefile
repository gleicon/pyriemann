
PROTOC=/usr/local/bin/protoc
MV = /bin/mv

protobuf:
	${PROTOC} --python_out pb proto.proto
	${MV} pb ../riemann

all: protobuf
