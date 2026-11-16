# Bangla UniJoy Keyboard Layout for macOS

A macOS keyboard layout that reproduces the **Bangla UniJoy** layout (Windows MSKLC source, locale `bn-BD`), with one addition: the `` ` `` key types the **Zero Width Joiner (U+200D)**.

---

## Contents

1. [Files](#files)
2. [Installation](#installation)
3. [Uninstalling](#uninstalling)
4. [Modifier keys](#modifier-keys)
5. [Key map](#key-map)
6. [Hasanta (dead key) behaviour](#hasanta-dead-key-behaviour)
7. [Ligatures and conjunct shortcuts](#ligatures-and-conjunct-shortcuts)
8. [Zero Width Joiner (ZWJ)](#zero-width-joiner-zwj)
9. [Typing examples](#typing-examples)
10. [Customising and rebuilding](#customising-and-rebuilding)
11. [Differences from the Windows source](#differences-from-the-windows-source)
12. [Troubleshooting](#troubleshooting)
13. [Technical reference](#technical-reference)

---

## Files

| File | Purpose |
|---|---|
| `Unijoy.klc` | Source of truth. Windows MSKLC layout data (key → character table, ligatures, dead key). Edit this to change the layout. |
| `build.py` | Converts `Unijoy.klc` into a macOS layout and bundle. |
| `Unijoy.bundle/` | The installable macOS keyboard layout bundle (generated). |
| `Unijoy.keylayout` | Standalone copy of the generated layout XML (same as the one inside the bundle). |
| `README.md` | This document. |

Bundle structure:

```
Unijoy.bundle/
└── Contents/
    ├── Info.plist                      # bundle id, input source id, language (bn)
    └── Resources/
        ├── Unijoy.keylayout            # the layout itself
        └── en.lproj/InfoPlist.strings  # display name
```

---

## Installation

1. Copy the bundle into your personal Keyboard Layouts folder:

   ```bash
   mkdir -p ~/Library/Keyboard\ Layouts
   ```

   ```bash
   cp -R ~/Desktop/Unijoy/Unijoy.bundle ~/Library/Keyboard\ Layouts/
   ```

   (To make it available to every user on the Mac, copy it to `/Library/Keyboard Layouts/` instead; that needs an administrator password.)

2. **Log out and log back in.** macOS only loads keyboard layouts at login. A full restart is not required.

3. Open **System Settings → Keyboard → Text Input → Input Sources → Edit… → +**, find **Bangla UniJoy** (under *Bengali* or *Others*), and click **Add**.

4. Switch to it from the input menu in the menu bar, or with **Ctrl+Space** / the **Globe (fn)** key.

### Updating after a change

Copy the new bundle over the old one, then log out and back in:

```bash
rm -rf ~/Library/Keyboard\ Layouts/Unijoy.bundle && cp -R ~/Desktop/Unijoy/Unijoy.bundle ~/Library/Keyboard\ Layouts/
```

---

## Uninstalling

1. Remove **Bangla UniJoy** from System Settings → Keyboard → Text Input → Input Sources.
2. Delete the bundle:

   ```bash
   rm -rf ~/Library/Keyboard\ Layouts/Unijoy.bundle
   ```

3. Log out and back in.

---

## Modifier keys

| Modifier | Behaviour |
|---|---|
| *(none)* | UniJoy base layer |
| **Shift** | UniJoy shifted layer |
| **Option** | Equivalent of Windows **Ctrl+Alt / AltGr** layer (only a few keys are defined, see below) |
| **Shift+Option** | Not defined in the source; only Space and navigation keys work |
| **Caps Lock** | No effect — UniJoy letters have no upper case, so Caps Lock gives the same result as no modifier |
| **Command** | Falls back to US QWERTY so shortcuts (⌘C, ⌘V, ⌘Z, ⌘ + `` ` `` …) work normally |
| **Control** | Falls back to US QWERTY control characters (Ctrl+A, Ctrl+E, etc. work in text fields) |

---

## Key map

Keys are named by their position on a US QWERTY keyboard.

### Number row

| Key | Normal | Shift |
|---|---|---|
| `` ` `` | **ZWJ** (U+200D, invisible) | `~` |
| `1` | ১ | ! |
| `2` | ২ | @ |
| `3` | ৩ | # |
| `4` | ৪ | ৳ (Bengali Rupee sign) |
| `5` | ৫ | % |
| `6` | ৬ | ^ |
| `7` | ৭ | ঁ (chandrabindu) |
| `8` | ৮ | * |
| `9` | ৯ | ( |
| `0` | ০ | ) |
| `-` | - | _ |
| `=` | = | + |

### Top row

| Key | Normal | Shift | Option |
|---|---|---|---|
| `Q` | ং (anusvara) | ঙ | ঙ্গ |
| `W` | য | য় | |
| `E` | ড | ঢ | |
| `R` | প | ফ | |
| `T` | ট | ঠ | |
| `Y` | চ | ছ | |
| `U` | জ | ঝ | |
| `I` | হ | ঞ | |
| `O` | গ | ঘ | |
| `P` | ড় | ঢ় | |
| `[` | [ | { | |
| `]` | ] | } | |
| `\` | ৎ (khanda ta) | ঃ (visarga) | |

### Home row

| Key | Normal | Shift | Option |
|---|---|---|---|
| `A` | ৃ (ri-kar) | র্ (reph) | |
| `S` | ু (u-kar) | ূ (uu-kar) | |
| `D` | ি (i-kar) | ী (ii-kar) | |
| `F` | া (aa-kar) | অ | আ |
| `G` | ্ **hasanta — dead key** | । (dari) | |
| `H` | ব | ভ | |
| `J` | ক | খ | |
| `K` | ত | থ | |
| `L` | দ | ধ | |
| `;` | ; | : | |
| `'` | ' | " | |

### Bottom row

| Key | Normal | Shift | Option |
|---|---|---|---|
| `Z` | ্র (ra-phala) | ্য (ya-phala) | |
| `X` | ো (o-kar) | ৌ (au-kar) | |
| `C` | ে (e-kar) | ৈ (ai-kar) | |
| `V` | র | ল | র‍্য |
| `B` | ন | ণ | |
| `N` | স | ষ | |
| `M` | ম | শ | |
| `,` | , | < | |
| `.` | . | > | |
| `/` | / | ? | |

### Other keys

| Key | Output |
|---|---|
| Space | Space (also with Option) |
| Keypad `.` | . |
| Keypad digits and operators | ASCII `0–9`, `* + - / =` |
| Return, Tab, Delete, Esc, arrows, Home/End, Page Up/Down, F-keys | Unchanged from standard macOS behaviour |

---

## Hasanta (dead key) behaviour

`G` is a **dead key** for hasanta (্, U+09CD). Pressing it types nothing at first; what happens next depends on the following key.

| Sequence | Result | Explanation |
|---|---|---|
| `G` + vowel sign | Independent vowel | See table below |
| `G` + consonant | ্ + consonant | Forms a conjunct, e.g. ক + ্ + ত = ক্ত |
| `G` + `G` | ্ and still waiting | Emits one hasanta and stays in hasanta mode |
| `G` + Space | Space only | The hasanta is dropped (as in the Windows source) |
| `G` + any other key | ্ + that key's character | |

### Vowel conversion after `G`

| Keys | Vowel sign | Becomes |
|---|---|---|
| `G` `F` | া | আ |
| `G` `D` | ি | ই |
| `G` `Shift+D` | ী | ঈ |
| `G` `S` | ু | উ |
| `G` `Shift+S` | ূ | ঊ |
| `G` `A` | ৃ | ঋ |
| `G` `C` | ে | এ |
| `G` `Shift+C` | ৈ | ঐ |
| `G` `X` | ো | ও |
| `G` `Shift+X` | ৌ | ঔ |

`অ` is typed directly with `Shift+F`, and `আ` also with `Option+F`.

---

## Ligatures and conjunct shortcuts

Some keys type more than one character at once:

| Keys | Output | Code points |
|---|---|---|
| `Shift+A` | র্ (reph) | U+09B0 U+09CD |
| `Z` | ্র (ra-phala) | U+09CD U+09B0 |
| `Shift+Z` | ্য (ya-phala) | U+09CD U+09AF |
| `Option+Q` | ঙ্গ | U+0999 U+09CD U+0997 |
| `Option+V` | র‍্য | U+09B0 U+200D U+09CD U+09AF |

Note that reph is typed **before** the consonant it sits on (e.g. `Shift+A` `J` → র্ক), while ra-phala / ya-phala are typed **after** it.

---

## Zero Width Joiner (ZWJ)

The `` ` `` key types **U+200D ZERO WIDTH JOINER**.

- It is **invisible** and has no width, but it is a real character in the text: Backspace deletes it with one press, and it affects searching and copy-paste.
- It asks the font to join neighbouring characters or to choose an alternative joined form. In Bengali the main use is **র + ZWJ + ্ + য → র‍্য** (the "ra + ya-phala" form, as in র‍্যাব) instead of the reph form র্য.
- `G` then `` ` `` gives ্ followed by ZWJ.
- Command + `` ` `` still switches between windows of the current app, because Command uses the QWERTY layer.
- Option + `` ` `` types nothing.
- Shift + `` ` `` types `~`.

---

## Typing examples

| Word / form | Keys |
|---|---|
| কা | `J` `F` |
| কি | `J` `D` |
| কে | `J` `C` |
| ক্ত | `J` `G` `K` |
| প্র | `R` `Z` |
| ক্য | `J` `Shift+Z` |
| র্ক | `Shift+A` `J` |
| আমি | `G` `F` `M` `D` (or `Option+F` `M` `D`) |
| এক | `G` `C` `J` |
| বাংলা | `H` `F` `Q` `Shift+V` `F` |
| র‍্য | `V` `` ` `` `G` `W` (or `Option+V`) |
| ১২৩ | `1` `2` `3` |

> UniJoy on Windows is often used with software that lets you type ে / ৈ / ি **before** the consonant and reorders them. This layout does not reorder: type vowel signs **after** the consonant, in Unicode order (e.g. কে = `J` then `C`).

---

## Customising and rebuilding

All layout data lives in `Unijoy.klc`. To change a key:

1. Find the line for the key in the `LAYOUT` section. Columns are:

   ```
   SC   VK_   Cap   Normal   Shift   Ctrl   Ctrl+Alt
   ```

   - Values are hexadecimal Unicode code points (e.g. `0995` = ক).
   - `-1` = nothing, `%%` = defined in the `LIGATURE` section.
   - A trailing `@` marks a dead key (only `09cd@` on `G`).
   - The **Ctrl** column is ignored on macOS; **Ctrl+Alt** becomes **Option**.

2. For multi-character output, add a line to `LIGATURE`:

   ```
   VK_   Mod#   Char0   Char1   ...
   ```

   `Mod#` is the column number: `0` Normal, `1` Shift, `3` Ctrl+Alt (Option).

3. To change what follows hasanta, edit the `DEADKEY 09cd` table (`input  output`).

4. Rebuild and reinstall:

   ```bash
   cd ~/Desktop/Unijoy && python3 build.py
   ```

   ```bash
   rm -rf ~/Library/Keyboard\ Layouts/Unijoy.bundle && cp -R ~/Desktop/Unijoy/Unijoy.bundle ~/Library/Keyboard\ Layouts/
   ```

5. Log out and back in.

Settings at the top of `build.py`:

| Setting | Current value | Meaning |
|---|---|---|
| `NAME` | `Bangla UniJoy` | Name shown in Input Sources |
| `LAYOUT_ID` | `-24550` | Unique negative id required for custom layouts |
| `BUNDLE_ID` | `local.keyboardlayout.unijoy` | Bundle identifier |

### Validating

The layout uses XML 1.1 (needed for control-character entities such as `&#x0008;`), which `xmllint` does not support directly. To check it against Apple's DTD, mask those entities first:

```bash
sed -E -e 's/version="1.1"/version="1.0"/' -e 's/&#x00(0[0-8BCEF]|1[0-9A-F]);/X/g' Unijoy.keylayout > /tmp/check.xml && xmllint --noout --dtdvalid /System/Library/DTDs/KeyboardLayout.dtd /tmp/check.xml
```

```bash
plutil -lint Unijoy.bundle/Contents/Info.plist
```

---

## Differences from the Windows source

| Item | Windows (.klc) | macOS build |
|---|---|---|
| `` ` `` key | Not defined (types nothing) | ZWJ; Shift gives `~` (added at your request) |
| Ctrl+Alt layer | Ctrl+Alt / AltGr | **Option** |
| Ctrl layer | Empty | Control characters (QWERTY), for text-field shortcuts |
| Command | n/a | US QWERTY, so app shortcuts work |
| ISO extra key (§ / next to left Shift) | n/a | Same as `` ` `` |
| `KEYNAME` / `KEYNAME_EXT` sections | Present | Not used on macOS; omitted from the saved `.klc` |
| Everything else | — | Identical |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Layout not listed in Input Sources | Check the bundle is at `~/Library/Keyboard Layouts/Unijoy.bundle`, then log out and back in. Look under *Others* as well as *Bengali*. |
| Changes don't take effect | Log out and back in. If still old: remove the layout from Input Sources, add it again; if that fails, restart. |
| Keyboard shortcuts type Bangla instead of acting | Shouldn't happen (Command uses QWERTY). If an app ignores this, switch to ABC briefly. |
| Conjuncts show as separate letters with a visible ্ | The font lacks the conjunct; try a Bengali font such as *Kohinoor Bangla*, *Bangla Sangam MN* or *Noto Sans Bengali*. |
| র‍্য shows as র্য | The app or font ignores ZWJ; try another font. |
| `G` seems to do nothing | Expected: it waits for the next key. Press a consonant or vowel sign next. |
| Layout shows a generic icon | No custom icon is included; this does not affect typing. |

---

## Technical reference

### Windows scan code → macOS key code

| Key | Scan code | Mac code | | Key | Scan code | Mac code |
|---|---|---|---|---|---|---|
| `` ` `` | 29 | 50 | | `A` | 1e | 0 |
| `1` | 02 | 18 | | `S` | 1f | 1 |
| `2` | 03 | 19 | | `D` | 20 | 2 |
| `3` | 04 | 20 | | `F` | 21 | 3 |
| `4` | 05 | 21 | | `G` | 22 | 5 |
| `5` | 06 | 23 | | `H` | 23 | 4 |
| `6` | 07 | 22 | | `J` | 24 | 38 |
| `7` | 08 | 26 | | `K` | 25 | 40 |
| `8` | 09 | 28 | | `L` | 26 | 37 |
| `9` | 0a | 25 | | `;` | 27 | 41 |
| `0` | 0b | 29 | | `'` | 28 | 39 |
| `-` | 0c | 27 | | `\` | 2b | 42 |
| `=` | 0d | 24 | | `Z` | 2c | 6 |
| `Q` | 10 | 12 | | `X` | 2d | 7 |
| `W` | 11 | 13 | | `C` | 2e | 8 |
| `E` | 12 | 14 | | `V` | 2f | 9 |
| `R` | 13 | 15 | | `B` | 30 | 11 |
| `T` | 14 | 17 | | `N` | 31 | 45 |
| `Y` | 15 | 16 | | `M` | 32 | 46 |
| `U` | 16 | 32 | | `,` | 33 | 43 |
| `I` | 17 | 34 | | `.` | 34 | 47 |
| `O` | 18 | 31 | | `/` | 35 | 44 |
| `P` | 19 | 35 | | Space | 39 | 49 |
| `[` | 1a | 33 | | Keypad `.` | 53 | 65 |
| `]` | 1b | 30 | | | | |

### Key map indices in the `.keylayout`

| Index | Selected by | Contents |
|---|---|---|
| 0 | no modifier, Caps Lock | UniJoy normal |
| 1 | Shift (± Caps Lock) | UniJoy shift |
| 2 | Option (± Caps Lock) | UniJoy Ctrl+Alt |
| 3 | Shift+Option | empty (Space and navigation only) |
| 4 | Command (+ any) | US QWERTY |
| 5 | Control (+ Shift/Option) | US QWERTY control characters |

### Dead key implementation

- `G` (key code 5) in map 0 triggers action `dead_hasanta`, which enters state `hasanta`.
- Every vowel-sign key and Space has an action with a `hasanta` branch giving the independent vowel (or space).
- Any other key in state `hasanta` outputs the terminator ্ (U+09CD) followed by its own character.

### Bundle metadata

| Key | Value |
|---|---|
| `CFBundleIdentifier` | `local.keyboardlayout.unijoy` |
| `TISInputSourceID` | `local.keyboardlayout.unijoy.unijoy` |
| `TISIntendedLanguage` | `bn` |
| Layout `group` / `id` | `126` (Unicode) / `-24550` |
