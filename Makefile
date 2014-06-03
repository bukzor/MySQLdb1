DOCKER ?= docker
#wrapper=-wrapper gdb,-x,/usr/lib/debug/usr/bin/python2.7-dbg-gdb.py,-ex,r,--args
export CC := $(DOCKER) run -ti -v $(PWD):/src gpp --maxtrans=1000 --dump-json $(wrapper)

docker-gpp: Dockerfile
	$(DOCKER) build -t gpp .
	touch docker-gpp


.PHONY: refcount
refcount: docker-gpp
	rm -rf build/lib*
	bash -c 'rm -f build/temp.linux-x86_64-2.7/*.{o,html,json}'
	python setup.py build
	bash -c 'git add -f build/temp.linux-x86_64-2.7/*.{html,json}'
