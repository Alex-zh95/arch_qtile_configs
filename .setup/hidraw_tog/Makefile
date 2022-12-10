CFLAGS ?= -O3 
PREFIX ?= /usr/local

all: hidraw-tog

rebuild: clean hidraw-tog

help:
	echo "TUXEDO Touchpad Switcher\n"
	echo "Instructions:\n"
	echo "Local compile:\tmake all\n"
	echo "Install software:\tsudo make install\n"
	echo "Refresh udev\tsudo make refresh-udev\n"

hidraw-tog: hidraw-tog.cpp
	g++ "$@.cpp" -o $@ $(CFLAGS)

clean:
	rm -f hidraw-tog

install: hidraw-tog
	# First install the main hidraw-tog tool, then the rules for allowing non-root access
	install -Dm755 hidraw-tog $(PREFIX)/bin/hidraw-tog
	install -Dm644 99-hidraw-tog.rules /etc/udev/rules.d/99-hidraw-tog.rules

refresh-udev:
	udevadm control --reload
	udevadm trigger

