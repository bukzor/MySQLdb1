# Dockerfile to build Refcount checking tool
# http://gcc-python-plugin.readthedocs.org/en/latest/
FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install --no-install-recommends -y \
    git \
    make \
    g++-4.8 \
    gcc-4.8-plugin-dev

RUN apt-get install --no-install-recommends -y \
    python2.7-dbg \
    python2.7-dev \
    python-lxml \
    python-pygments \
    python-six


# docker mini-bug: ending the last line with  ' \' above makes it join
#   with the next line, no matter how many newlines in between.
WORKDIR /opt
RUN git clone git://git.fedorahosted.org/gcc-python-plugin.git

# docker mini-bug: using a relative path here gives us /gcc-python...
WORKDIR /opt/gcc-python-plugin
RUN make plugin

# running the docker acts like running this command:
# docker mini-bug: specifying this without the list makes the entrypoint always have no arguments
ENTRYPOINT ["/opt/gcc-python-plugin/gcc-with-cpychecker"]

# default arguments:
CMD ["--help"]

ENV C_INCLUDE_PATH /usr/include/python2.7_d

WORKDIR /src
VOLUME ["/src"]
