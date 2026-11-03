---
name: tantawi-structure
description: Scaffold only the folder structure of a new Flutter app using core and feature-first data/cubit/ui conventions. Use when asked to initialize an app structure, especially in Arabic (جهز استراكشر التطبيق). Does not implement screens, features, or integrations.
---

# Tantawi Structure

Create the organizational skeleton only. This convention is extracted from a Flutter application using Cubit, GetIt, Dio, named routes, and EasyLocalization; it does not require installing those packages to create folders.

## Scope

- Inspect the destination and its AGENTS.md and Flutter profile before scaffolding. Preserve explicit project choices. If another skill recommends a different layout, use the user's requested data/cubit/ui layout unless the destination has an explicit conflicting requirement; surface a real conflict before mixing layouts.
- Default to the current Flutter project. For an empty destination, create the folder skeleton without running `flutter create` unless the user requests a runnable Flutter project.
- Create directories and `.gitkeep` files only. Do not generate Dart placeholders, screens, sample business features, models, repositories, tests, or package/config changes. Do not replace `main.dart` or any existing file.
- Do not copy source from the reference application. Never transfer API URLs, credentials, Firebase/Sentry settings, identifiers, branding, fonts, business logic, or platform files.
- Use only feature names the user requests. Without names, create `features/` empty. Do not add auth, onboarding, dashboard, or splash by assumption.
- Do not refactor an established project merely because this skill is available.

## Layout

```text
lib/
  core/
    constant/                 # asset paths, text keys, application constants
    di/                       # dependency registration, e.g. inject.dart
    enums/
    extension/
    models/                   # genuinely shared models
    network/                  # client, API service, configuration
    routing/                  # app_routes.dart and app_router.dart when implemented
    services/                 # shared infrastructure services
    shared/
      bottom_sheets/
      screens/
      utils/
      widgets/
    theme/                    # theme and tokens when implemented
    utils/
  features/
    <requested_feature>/
      data/
        models/
      cubit/
      ui/
        widgets/
assets/
  pngs/
  svgs/
  gifs/
  fonts/
  translations/
  sound/
```

Future feature implementation places repositories directly in `data/`, Cubit and state files in `cubit/`, and screens in `ui/`. This is the reference project's lightweight convention; do not silently convert it to domain/data/presentation Clean Architecture. Keep feature-specific helpers near their feature and reserve core for shared code. A new asset directory does not imply a pubspec declaration or a real asset exists.

## Execution

Use the bundled script, with an absolute destination and optional repeated feature arguments:

```bash
python3 <skill-directory>/scripts/scaffold.py /absolute/path/to/app --feature login --feature profile
```

Without `--feature`, it creates no business features. The script adds missing folders, preserves existing content, and refuses symlink paths. If the user asks for a different layout, adapt the folder list rather than forcing this template.

Verify the resulting directory tree and report the destination, created structure, and any skipped existing content. Stop after scaffolding; implementation is a separate request.
