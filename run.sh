#!/bin/bash

IMG="jekyll"

podman build . -t $IMG
podman run -it -v "$(realpath .):/app/src" $IMG "$@"