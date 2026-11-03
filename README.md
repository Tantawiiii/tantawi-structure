# Tantawi Structure

مهارة لـ Codex لتجهيز هيكل مجلدات تطبيق Flutter فقط، بتنظيم `core` و`features`، وداخل كل ميزة `data` و`cubit` و`ui`.

A reusable Codex skill that creates only a Flutter folder skeleton. No application code, dependencies, credentials, or product integrations are included. Requires Python 3.9 or later.

## التثبيت / Installation

نزّل المستودع أو اعمله clone، ثم نفّذ من داخله الأمر التالي. يثبت المهارة في مجلد Codex العام، ويحافظ على أي نسخة موجودة بدل استبدالها تلقائيًا.

Clone or download this repository, then run this from its root:

```bash
python3 - <<'PYTHON'
import os
from pathlib import Path
import shutil

source = Path.cwd()
assert (source / "SKILL.md").is_file(), "Run from the repository root"
base = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
target = base / "skills" / "tantawi-structure"
if target.exists():
    raise SystemExit(f"Already installed: {target}")
for relative in ("SKILL.md", "agents/openai.yaml", "scripts/scaffold.py"):
    destination = target / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / relative, destination)
print(f"Installed: {target}")
PYTHON
```

## الاستخدام / Usage

داخل مشروعك الجديد، اطلب من Codex:

```text
$tantawi-structure جهّز استراكشر التطبيق بس
```

لتجهيز ميزات محددة:

```text
$tantawi-structure جهّز الاستراكشر بميزات login و profile فقط
```

You can also use the script directly, without Codex:

```bash
python3 scripts/scaffold.py /absolute/path/to/app --feature login --feature profile
```

Feature names use lowercase snake_case. Omit `--feature` to leave `features/` empty. Use a physical absolute destination path: symlink paths are rejected, including aliased parent directories (on macOS, use `/private/tmp` rather than `/tmp`). Existing files are preserved. Empty folders receive `.gitkeep` files.

## الهيكل / Structure

```text
lib/
  core/
    constant/
    di/
    enums/
    extension/
    models/
    network/
    routing/
    services/
    shared/
      bottom_sheets/
      screens/
      utils/
      widgets/
    theme/
    utils/
  features/
    <requested_feature>/
      data/models/
      cubit/
      ui/widgets/
assets/
  pngs/
  svgs/
  gifs/
  fonts/
  translations/
  sound/
```

لا تنشئ المهارة شاشات أو كود Dart، ولا تعدّل `pubspec.yaml` أو ملفات التطبيق الموجودة. إنشاء مجلدات assets لا يسجلها تلقائيًا في Flutter.

The conventions are compatible with Cubit, GetIt, Dio, and EasyLocalization, but the scaffold does not install or require these packages. It does not create a runnable Flutter project; use `flutter create` separately when needed.

## الرفع على GitHub / Publishing

أنشئ مستودع GitHub فارغ باسم `tantawi-structure`، ثم نفّذ الأوامر من هذا المجلد فقط. استبدل `YOUR_USERNAME` باسم حسابك:

```bash
git init -b main
git add SKILL.md agents/openai.yaml scripts/scaffold.py README.md .gitignore
git commit -m "Add Tantawi Structure skill"
git remote add origin https://github.com/YOUR_USERNAME/tantawi-structure.git
git push -u origin main
```

ارفع محتويات هذا المجلد فقط؛ لا ترفع مشروع التطبيق المحيط به. لم يتم إنشاء مستودع بعيد أو رفع أي ملفات تلقائيًا.

Upload only this folder's contents, not the surrounding application repository. No remote repository is created by the skill.
# tantawi-structure
