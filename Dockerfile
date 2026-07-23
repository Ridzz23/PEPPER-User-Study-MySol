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

# add the package freeze thing so no segfaults when dependencies dont match in the future when reviews run it
# like: numpy==2.5.1 matplotlib==3.11.1 pillow==12.3.0 or chekc if build already comes with it then its fine. as long as they dont have to reinstall these at the time