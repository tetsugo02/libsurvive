#!/bin/sh
# libusb without udev for the roboloom wheels (cibuildwheel's before-all, in the
# manylinux container). The distribution's libusb links libudev, which auditwheel would
# then bundle with libmount, libblkid and libselinux; udev's library belongs to the
# system. Without udev, libusb enumerates devices and detects hotplug through netlink.
set -eu
VERSION=1.0.30
SHA256=fea36f34f9156400209595e300840767ab1a385ede1dc7ee893015aea9c6dbaf
dnf install -y bzip2 zlib-devel
cd /tmp
curl -sSLO "https://github.com/libusb/libusb/releases/download/v${VERSION}/libusb-${VERSION}.tar.bz2"
echo "${SHA256}  libusb-${VERSION}.tar.bz2" | sha256sum -c -
tar xjf "libusb-${VERSION}.tar.bz2"
cd "libusb-${VERSION}"
./configure --prefix=/usr/local --disable-udev --disable-static
make -j"$(nproc)"
make install
ldconfig
