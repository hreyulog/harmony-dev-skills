# HarmonyOS OpenCode Skill Packages (OpenCode)

Introduction
- This repository's top-level folders are OpenCode Skill Packages, used by OpenCode for loading and executing skills. Each folder contains a runnable skill implementation along with metadata and documentation.

Current Skill Packages
- harmonyos-api-snippets — HarmonyOS API usage snippets for quick reference of common APIs.
- harmonyos-atomic-service — HarmonyOS atomic service example demonstrating inter-service communication and lifecycle patterns.
- harmonyos-code-translator — Code migration/translation tooling for the HarmonyOS ecosystem.
- harmonyos-debugger — Debugging tools and scenarios to help diagnose and fix HarmonyOS apps.
- harmonyos-widget-gallery — HarmonyOS Widget gallery demonstrating UI patterns and interactions.
- website-to-harmonyos — Tools and examples for migrating a website to HarmonyOS-compatible structure.
- website2uniapp — Utilities to port website apps to uni-app.
- miniprogram2uniapp — Converter tools for mini-programs to uni-app.

Usage
- OpenCode discovers and loads skill packages at runtime from subfolders in the root directory. To add a new skill package, create a new folder at the root with a standard skill.json (metadata) and an entry script (e.g., index.js or main.js), plus an optional README.md.
- Example fields for skill.json (recommended):
  {
    "name": "skill-name",
    "version": "0.1.0",
    "description": "Brief description of the skill",
    "entry": "index.js"
  }
- See each skill's README.md for implementation details and usage.

Contributing
- Add new skill packages: create a new folder at the root and provide skill.json, an entry script, and a README.
- Ensure documentation is clear, accurate, and easy to understand for others.

License
- MIT

Contact
- If you have questions, please raise an issue in this repository or contact the maintainers.
