# Google Fonts Axis Registry Audit

Font: `fonts/variable/VirtuaGrotesk[wght].ttf`
Registry source: `/Users/eli/GH/forks/fonts/axisregistry/Lib/axisregistry/data/weight.textproto`

This report compares the built variable font's `wght` metadata to the local `google/fonts` axis registry entry used by Google Fonts for canonical axis names and fallback labels.

## Summary

- Registry tag: `wght`
- Registry display name: Weight
- Registry bounds/default: 1/400/1000
- Registry precision: 0
- Registry fallback-only: no
- Font `wght` bounds/default: 400/400/700
- Family fallback subset: Regular 400, Medium 500, SemiBold 600, Bold 700

## Axis Checks

| Check | Result |
| --- | --- |
| Registry tag is `wght` | yes |
| Font axis name matches registry display name | yes |
| Font default matches registry default | yes |
| Font range is within registry range | yes |
| Font uses registered fallback names for its range | yes |
| STAT values use registered fallback names for its range | yes |

## Registered Fallbacks

| Name | Value | In font range | fvar instance | STAT value |
| --- | ---: | --- | --- | --- |
| Thin | 100 | no |  |  |
| ExtraLight | 200 | no |  |  |
| Light | 300 | no |  |  |
| Regular | 400 | yes | Regular | Regular |
| Medium | 500 | yes | Medium | Medium |
| SemiBold | 600 | yes | SemiBold | SemiBold |
| Bold | 700 | yes | Bold | Bold |
| ExtraBold | 800 | no |  |  |
| Black | 900 | no |  |  |

## Review Notes

- The family intentionally uses the registered `wght` axis subset 400-700.
- The 600 fallback is spelled `SemiBold`, matching the Google Fonts axis registry.
- No custom axis is present, so no new axis registry proposal is needed.
- The `avar` warning remains a separate first-submission decision.
