# AI continuation: current version is v2

Read README_V2.md, REPRODUCE_V2.md, HISTORY_V2.md, QA_V2.md and ISSUES_V2.md first. Current code is reference-led version 2. Preserve existing public README history/gallery; do not erase unrelated changes. The v1 ZIP and QA_REPORT.md are historical, not current acceptance evidence.

Use the actual files and render images, never infer a finished reconstruction from test counts. Sources in src/assets_v2.py replace geometry deterministically. Do not rerun v1 refine scripts. Texture generation order: make_textures_v2.py then refine_materials_v2.py; then run_blender.py and build.mjs. See REPRODUCE_V2.md for winding/UV conventions, shader pass ordering, physics assumptions and GPU-timing caveats.

Work only inside this project. Commit before and after material changes, but do not push without the user's authorization. Keep source/photo attribution and historical uncertainty labels. Claims about exact 1972 architecture, full blast physics, universal FPS or photorealism are not supported. Keep the difference between confirmed historical facts and authored camera/effects explicit.
