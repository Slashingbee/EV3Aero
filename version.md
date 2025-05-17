# 📦 Versioning Guide

This document explains the versioning scheme used in this project so users and contributors can understand the meaning of each version label.

---

## 🔧 Pre-Release / Prototype Versions

Format: `0.X.0`  
Prefix: Optional `proto-` (e.g. `proto-0.1.0`)

These versions represent the **experimental, developmental, or prototype** stage before the first official release.

- `0.1.0` — Initial prototype
- `0.2.0` — Second iteration with improvements
- `0.3.0` — Final prototype before full release

> ⚠️ These versions are not considered stable or complete.

---

## 🚀 Initial Official Release

Format: `1.0` or `2.0.0.0`

This marks the **first stable and public version** of the program.

- `1.0` — Feature-complete and considered ready for general use.

---

## 🔄 Post-Release Versioning

Format: `X.Y.Z.E`  
Structure: `Major.Minor.Patch.Extra`
------------------------------------------------------------------------
| Segment | Description                                                |
|---------|------------------------------------------------------------|
| `X`     | **Major** – Breaking changes or major feature additions    |
| `Y`     | **Minor** – New features, backward-compatible              |
| `Z`     | **Patch** – Bug fixes, performance tweaks, small updates   |
| `E`     | **Extra** – Optional hotfix, internal build, or metadata   |
------------------------------------------------------------------------
### Examples:
- `1.0.0.0` — Initial stable release  
- `1.1.0.0` — Minor new features added  
- `1.1.1.0` — Bug fix  
- `1.1.1.1` — Hotfix or internal build  
- `2.0.0.0` — Major new version with breaking changes  

---

## 📝 Notes

- Version numbers increase based on the scope of changes.
- Pre-release versions may not be backwards-compatible or fully functional.
- Stable releases follow semantic-style logic with an added `extra` digit for flexibility.

---

Thanks for using the project!  
Feel free to open an issue if you have questions about the versioning system.
