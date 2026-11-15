# isahhah.com

**Build your strength.** A personalised, military-inspired home-training app for adults.

The first release contains three weeks of training: nine strength sessions and six optional low-impact conditioning sessions, with 72 animated movement guides and female coaching. The 72 count includes regressions, progressions, left/right guides, warm-ups and cooldowns. The schedule uses 50 distinct main-work station entries and retains the opening session for the final comparison.

Sessions contain 10, 12 or 14 active minutes according to the selected level, including warm-up and cooldown. Rest is tracked separately. Timed practice also counts toward the hard 15-minute active cap. Onboarding asks about experience, goals, equipment, schedule, floor capability and exercise restrictions before assigning a routine. Progress stays in the current browser.

## Run and check

Serve `public/` using a static web server, for example:

```sh
python3 -m http.server 8766 --directory public
npm test
```

All runtime dependencies and media are served locally from this app. The pinned Three.js dependency is vendored in `public/vendor/` so the production app makes no runtime CDN requests. Vercel serves `public/` using the checked-in configuration. The custom icon is configured for the browser, Apple home-screen shortcut and web app manifest.

## Reusable animations

`public/media/3d/instructor.glb` contains the approved female instructor in shorts and all 72 authored animations. The app plays them directly, with pause, front/side views and free camera rotation. The original approved squat MP4 remains available in `public/media/squat.mp4`.

The editable source is `animation/source/instructor.blend`; textures are packed. Motion-authoring code lives in `animation/`. With Blender 4.5 LTS installed, rebuild with:

```sh
blender --background --python animation/build_library.py
```

No MPFB installation or paid generation service is needed to rebuild from that source. MakeHuman assets are CC0; the asset license is included next to the source. Third-party Three.js and Kokoro licenses accompany their distributed files. The production bundle combines 44 previously generated coaching recordings with 30 recordings made locally using the Kokoro female voice. No new paid generation calls were made for this library.

## Verification and limits

Tests cover all three weeks across 810 profile/schedule combinations, time caps, rest accounting, substitutions, media coverage and icon configuration. All 72 motions pass authored limb-reach and loop-closure checks. Review images were inspected for standing and floor poses; these are production checks, not a qualified trainer's assessment or clinical validation.

This mat-and-chair foundation has limited progressive pulling resistance. It is general fitness, not rehabilitation or military test preparation. More than three weeks will be added only with the owner's go-ahead.

See [the training programme](docs/training-program.md).
