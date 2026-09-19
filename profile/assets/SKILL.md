---
name: zarishhealth-brand
description: Apply the ZarishHealth visual identity. Use whenever generating, reviewing or assembling anything that carries ZarishHealth branding — websites, READMEs, app UI, favicons, app icons, social cards, banners, slide decks, emails, print. Provides the exact colour tokens, typography, logo files, file-naming convention, per-platform sizes and accessibility limits, plus the misuse rules that must never be broken.
license: MIT
version: 1.0.0
---

# ZarishHealth Brand Skill

Machine-readable companion to `BRANDING.md`. Read this before producing any ZarishHealth-branded artefact. Full rationale and per-platform detail live in `BRANDING.md`; exact values live in `brand-tokens.json`.

## When to use

Trigger on: ZarishHealth logo, icon, favicon, app icon, avatar, banner, OG/social card, README header, badge, colour, palette, font, brand review, "make it on-brand", or any asset destined for a ZarishHealth surface.

Do **not** trigger for: unrelated projects, generic design questions with no ZarishHealth context.

## Non-negotiables

1. **Never redraw or re-typeset the logo.** Reference a shipped file. The wordmark is outlined Inter 800 at −0.015em — approximations are wrong and visible.
2. **Never recolour** outside the approved variants (§ Variants below).
3. **Never** add shadow, glow, bevel, outline, gradient, rotation or distortion to the mark.
4. **The gap where the cross meets the shield is intentional.** Do not "fix", close or fill it.
5. **Name every file** `zarishhealth-<type>-<target>[-<variant>][-<WxH>].<ext>`, lowercase, hyphenated.
6. **Below 32 px use the simplified mark** (`*-simple-*` files). Below 16 px, do not render the mark at all.
7. **iOS icons must be opaque.** Transparency renders as black.
8. **Social platforms and email do not render SVG.** Ship PNG there.
9. **White text on Vital Green fails contrast (2.2:1).** Never do it.
10. **"ZarishHealth"** — one word, capital Z, capital H. Never split, never all-caps.

## Colour tokens

```
primary        #017CF5   Zarish Blue      mark, links, primary action
primary-hover  #0163C4
primary-active #014A93                    also: blue for body text on white
accent         #10B981   Vital Green      the cross, success, positive vitals
accent-alt     #06B6D4   Care Teal        data, charts, connectivity
ink            #02091C   Deep Navy        dark surfaces, headings
surface        #F5F7FA   Cloud            app background
on-brand       #FFFFFF
dark-mode-primary #3D97F7 (blue-400)      substitute for #017CF5 on navy
```

Ramps: `blue` 50–900, `navy` 600–900, `green` 400–600, `teal` 400–600, `slate` 50–900.
States: success `#10B981` · warning `#F59E0B` · danger `#EF4444` · info `#017CF5` · critical `#BE123C`.
Gradients: brand `linear-gradient(135deg,#017CF5,#0148A8)` · network `linear-gradient(135deg,#02091C,#061532 55%,#0A2247)`.

**Ratio:** blue dominates; green stays under ~10% of any composition. In clinical UI reserve red and amber for real alerts only.

## Typography

- **Inter** — everything. 400 body, 500/600 UI, 700/800 headings.
- **JetBrains Mono** — code, IDs, terminal, API samples.
- Tracking: −0.015em display, 0 body, +0.08em caps labels.
- Fallback: `ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`.
- Both fonts are SIL OFL 1.1.

Ladder: H1 56–72/800 · H2 40–48/700 · H3 28–32/700 · body-lg 20–22/400 · body 16–18/400 · label 14–15/600 · caps 12–14/700.

## Variants — pick by background

| Background | Logo file suffix |
| --- | --- |
| White / light | `-light` |
| Navy / dark / photo | `-dark` |
| Marketing hero | `-duotone` |
| Single-colour print, engraving | `-mono-black` |
| Dark photo, embroidery | `-mono-white` |
| Single-colour brand use | `-mono-blue` |
| Platform strips transparency | `logo/zarishhealth-logo-plate-*` |

## Asset lookup

| Need | Path |
| --- | --- |
| Header / navbar logo | `logo/zarishhealth-logo-horizontal-{light,dark}.svg` |
| Square or centred logo | `logo/zarishhealth-logo-stacked-*.svg` |
| Symbol only | `icon/zarishhealth-icon-transparent-color.svg` |
| Symbol on a plate | `icon/zarishhealth-icon-{solid,circle}-{blue,navy,white}.svg` |
| Small sizes (<32 px) | `icon/zarishhealth-icon-simple-*.svg` |
| Favicon (ship all three) | `favicon/zarishhealth-favicon-web.ico` + `.svg` + `app-icon/zarishhealth-appicon-ios-180x180.png` |
| Android adaptive | `app-icon/zarishhealth-appicon-maskable-android-{192,512}*.png` |
| OG / link preview | `social/zarishhealth-social-opengraph-1200x630.png` |
| GitHub social preview | `social/zarishhealth-social-github-1280x640.png` |
| README hero | `banner/zarishhealth-banner-github-readme-1280x320.png` |
| Profile picture | `avatar/zarishhealth-avatar-{github,social,slack}-*.png` |
| README shield | `badge/zarishhealth-badge-readme-*.svg` |
| Dark background art | `pattern/zarishhealth-pattern-*.svg` |
| Tokens for code | `brand-tokens.json` · `brand.css` |
| `<head>` block | `head-snippet.html` |

## Canonical sizes

```
favicon      16, 32, 48 (in .ico) · svg · 96 · 192 · 512
apple-touch  180 (opaque)
ios store    1024 (no alpha)
android      192, 512 + maskable 192, 512 (content in central 80%)
windows tile 150, 270, 310
avatar       400, 460, 512, 800, 1024 (square, circle-safe)
open graph   1200x630   (universal — Facebook, LinkedIn, Slack, Discord, WhatsApp)
x card       1200x675   (summary_large_image)
github social 1280x640
linkedin     company 1128x191 · personal 1584x396 · post 1200x627
x header     1500x500
facebook     cover 851x315
youtube      2560x1440 (safe area 1546x423)
email        600x200
```

## Layout rules

- Clear space = 25% of mark height on all four sides.
- Minimums: full mark 32 px · simplified 16 px · horizontal lockup 120 px · stacked 96 px.
- Social cards: keep content inside the centre 1080×600 of a 1200×630 canvas.
- Focus ring: 2 px `#017CF5`, 2 px offset. Touch targets ≥ 44×44 px.

## Accessibility limits

| Pair | Ratio | Allowed for |
| --- | --- | --- |
| navy `#02091C` on white | 18.9:1 | everything |
| white on blue `#017CF5` | 3.6:1 | **large text & UI only** |
| white on blue-700 `#014A93` | 9.1:1 | everything |
| blue-600 `#0163C4` on white | 5.6:1 | body text |
| blue `#017CF5` on white | 3.6:1 | large text, icons, borders — not body |
| white on green `#10B981` | 2.2:1 | **never** |
| blue-400 `#3D97F7` on navy | 7.4:1 | everything (dark mode) |

Never encode meaning in colour alone. Respect `prefers-reduced-motion`.

## Decision procedure

1. Identify the surface (web / README / app / social / print / email).
2. Identify the background (light, dark, photo, single-colour) → pick the variant.
3. Pick vector unless the surface forbids it (social, email, app icons → PNG).
4. Check the size against the minimums; swap to the simplified mark under 32 px.
5. Apply clear space.
6. Check the contrast pair against the table.
7. Name the output with the convention.

## Generating a new size

Derive from vector; never upscale a PNG.

```bash
rsvg-convert -w <N> -h <N> <master>.svg -o zarishhealth-<type>-<target>-<N>x<N>.png
magick out-16.png out-32.png out-48.png zarishhealth-favicon-web.ico
```

Masters: `icon/zarishhealth-icon-transparent-color.svg`, `app-icon/zarishhealth-appicon-source-master.svg`, `logo/zarishhealth-logo-horizontal-light.svg`.

## Known placeholders

- The tagline **"Open health infrastructure"** on `social/` cards is a stand-in. Ask before shipping it; the `banner/` files carry no tagline.
- `badge/*-hipaa-ready`, `*-fhir-r4` and `*-certified` are visual badges only. Do not present them as attestations unless the claim is independently true.

## Review checklist

- [ ] Correct variant for the background
- [ ] Vector where possible; PNG where required
- [ ] Clear space respected, above minimum size
- [ ] Simplified mark used below 32 px
- [ ] Contrast pair passes
- [ ] Green under ~10% of the composition
- [ ] "ZarishHealth" spelled as one word, correct capitals
- [ ] Filename follows the convention
- [ ] Logo unmodified — no recolour, effect, rotation or distortion
- [ ] iOS icons opaque; Android maskable icons full-bleed
