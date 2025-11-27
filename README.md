# Virtua Grotesk

## Building

This project uses [fontc](https://github.com/googlefonts/fontc) to build fonts from the UFO sources.

### Prerequisites

Install fontc:
```bash
cargo install fontc
```

### Build Instructions

To build the fonts, run the build script:
```bash
./build.sh
```

The compiled fonts will be placed in the `fonts/` directory.

Note: The `fonts/` directory is excluded from version control to keep the repository size down.

## Rendering Specimens

This project uses [DesignBot](https://github.com/eliheuer/designbot) to render font specimens.

### Prerequisites

Install DesignBot:
```bash
cargo install designbot
```

### Rendering Instructions

To render a specimen, first build the fonts (see above), then run:
```bash
designbot --render designbot/001.rs --output designbot/001.png
```

The rendered specimen images will be saved in the `designbot/` directory.
