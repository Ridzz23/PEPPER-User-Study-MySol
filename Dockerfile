FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    jq \
    sed \
    gawk \
    coreutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /pepper

COPY pepper-install /pepper/pepper-install
COPY pepper.sh /pepper/pepper.sh
COPY tasks /pepper/tasks

RUN chmod +x /pepper/pepper.sh

WORKDIR /pepper/tasks

CMD ["/bin/bash"]