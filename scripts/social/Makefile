# Virtua Grotesk social assets. See README.md.
#
#   make            # build + render all three example formats (PNGs + mp4/gif)
#   make carousel   # §03 dyadic-grid carousel slides
#   make square     # 2048x2048 weight-morph animation (mp4 + gif)
#   make reel       # 1080x1920 grid-as-dataset loop (mp4 + gif)
#   make build      # cargo build --release only
#   make check      # cargo check
#   make clean      # remove rendered out/ (sources are the truth)

.PHONY: all carousel square reel build check clean

all:
	./render.sh all

carousel:
	./render.sh carousel

square:
	./render.sh square

reel:
	./render.sh reel

build:
	cargo build --release

check:
	cargo check

clean:
	rm -rf out
