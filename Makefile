.PHONY : build clean

build:
	mkdir -p build
	cd build && g++ -std=c++11 ../src/**/*.cpp -o ec && cp ec /usr/local/bin && cd ..

clean:
	rm -rf build
	rm -rf dist
	rm -rf ec.egg-info
	rm -rf docs/_build
	rm -rf docs/api
