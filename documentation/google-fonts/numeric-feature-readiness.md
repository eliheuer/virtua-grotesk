# Numeric Feature Readiness

This generated report checks the Google Fonts requirement that default
ASCII numerals are proportional and complemented by a Tabular Numbers
(`tnum`) feature.

## Summary

- Built font files present: yes
- Default ASCII digits present in every built font: yes
- Default ASCII digits are proportional in every built font: yes
- `tnum` feature present in every built font: yes
- `tnum` substitutes all ten ASCII digits in every built font: yes
- `tnum` substitutes to equal-width digits in every built font: yes
- Numeric feature requirement ready: yes

## Font Checks

| Font | Exists | Default digits | Default widths | Proportional defaults | `tnum` | `tnum` coverage | `tnum` widths | Tabular alternates |
| --- | --- | ---: | --- | --- | --- | ---: | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes | 10/10 | 368, 548, 594, 598, 604, 628, 636, 640, 664 | yes | yes | 10/10 | 664 | yes |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | yes | 10/10 | 368, 548, 594, 598, 604, 628, 636, 640, 664 | yes | yes | 10/10 | 664 | yes |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | yes | 10/10 | 389, 572, 618, 622, 628, 652, 660, 664, 680 | yes | yes | 10/10 | 680 | yes |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | yes | 10/10 | 411, 596, 642, 646, 652, 676, 684, 688, 696 | yes | yes | 10/10 | 696 | yes |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | yes | 10/10 | 432, 620, 666, 670, 676, 700, 708, 712 | yes | yes | 10/10 | 712 | yes |

## `tnum` Substitutions

- `fonts/variable/VirtuaGrotesk[wght].ttf`: zero->zero.tf(664), one->one.tf(664), two->two.tf(664), three->three.tf(664), four->four.tf(664), five->five.tf(664), six->six.tf(664), seven->seven.tf(664), eight->eight.tf(664), nine->nine.tf(664)
- `fonts/ttf/VirtuaGrotesk-Regular.ttf`: zero->zero.tf(664), one->one.tf(664), two->two.tf(664), three->three.tf(664), four->four.tf(664), five->five.tf(664), six->six.tf(664), seven->seven.tf(664), eight->eight.tf(664), nine->nine.tf(664)
- `fonts/ttf/VirtuaGrotesk-Medium.ttf`: zero->zero.tf(680), one->one.tf(680), two->two.tf(680), three->three.tf(680), four->four.tf(680), five->five.tf(680), six->six.tf(680), seven->seven.tf(680), eight->eight.tf(680), nine->nine.tf(680)
- `fonts/ttf/VirtuaGrotesk-SemiBold.ttf`: zero->zero.tf(696), one->one.tf(696), two->two.tf(696), three->three.tf(696), four->four.tf(696), five->five.tf(696), six->six.tf(696), seven->seven.tf(696), eight->eight.tf(696), nine->nine.tf(696)
- `fonts/ttf/VirtuaGrotesk-Bold.ttf`: zero->zero.tf(712), one->one.tf(712), two->two.tf(712), three->three.tf(712), four->four.tf(712), five->five.tf(712), six->six.tf(712), seven->seven.tf(712), eight->eight.tf(712), nine->nine.tf(712)

## Required Follow-Up

- None for the current built fonts.

References:

- https://googlefonts.github.io/gf-guide/requirements.html
- https://googlefonts.github.io/gf-guide/production.html
