# Posts

Single **static** feed images (1:1, 4:5, or 1.91:1). One `.rs` per post → `.png`.

`font-garden.rs` renders a 2048 × 2048 square with seven “Font.Garden” rows
in Virtua Grotesk Regular, light gray on a black background with generous margins.
From the repository root after `make build`:

```sh
designbot --raw documentation/social-assets/posts/font-garden.rs
```

The PNG is saved beside the script. Use `GRID_VIEW=1` and a separate
`--output /tmp/font-garden-grid.png` to inspect the layout grid.
