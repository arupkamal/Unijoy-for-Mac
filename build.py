#!/usr/bin/env python3
"""Convert Unijoy.klc (Windows MSKLC source) into a macOS keyboard layout bundle.

Usage:  python3 build.py
Output: Unijoy.bundle/ (copy it into ~/Library/Keyboard Layouts/)

Windows modifier columns map to macOS like this:
  col 0 (base)      -> no modifier
  col 1 (Shift)     -> Shift
  col 3 (Ctrl+Alt)  -> Option   (AltGr on Windows)
Command and Control fall back to US QWERTY so shortcuts like Cmd+C keep working.
"""
import os
import plistlib
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
KLC = os.path.join(HERE, "Unijoy.klc")
BUNDLE = os.path.join(HERE, "Unijoy.bundle")
NAME = "Bangla UniJoy"
FILE_BASE = "Unijoy"
LAYOUT_ID = "-24550"  # custom layouts use a negative id
BUNDLE_ID = "local.keyboardlayout.unijoy"

# Windows scan code -> macOS virtual key code (ANSI positions)
SC_TO_MAC = {
    "29": 50, "02": 18, "03": 19, "04": 20, "05": 21, "06": 23, "07": 22, "08": 26,
    "09": 28, "0a": 25, "0b": 29, "0c": 27, "0d": 24,
    "10": 12, "11": 13, "12": 14, "13": 15, "14": 17, "15": 16, "16": 32,
    "17": 34, "18": 31, "19": 35, "1a": 33, "1b": 30,
    "1e": 0, "1f": 1, "20": 2, "21": 3, "22": 5, "23": 4, "24": 38,
    "25": 40, "26": 37, "27": 41, "28": 39, "2b": 42,
    "2c": 6, "2d": 7, "2e": 8, "2f": 9, "30": 11, "31": 45, "32": 46,
    "33": 43, "34": 47, "35": 44, "39": 49, "53": 65,
}

# US QWERTY characters by macOS key code (for Command / Control layers)
QWERTY = {
    0: "a", 1: "s", 2: "d", 3: "f", 4: "h", 5: "g", 6: "z", 7: "x", 8: "c",
    9: "v", 10: "§", 11: "b", 12: "q", 13: "w", 14: "e", 15: "r",
    16: "y", 17: "t", 18: "1", 19: "2", 20: "3", 21: "4", 22: "6", 23: "5",
    24: "=", 25: "9", 26: "7", 27: "-", 28: "8", 29: "0", 30: "]", 31: "o",
    32: "u", 33: "[", 34: "i", 35: "p", 37: "l", 38: "j", 39: "'", 40: "k",
    41: ";", 42: "\\", 43: ",", 44: "/", 45: "n", 46: "m", 47: ".", 49: " ",
    50: "`",
}

# Keys that behave the same on every layer (Return, arrows, keypad, ...)
SPECIAL = {
    36: "\r", 48: "\t", 51: "\b", 52: "\x03", 53: "\x1b", 76: "\x03",
    71: "\x1b", 114: "\x05", 115: "\x01", 116: "\x0b", 117: "\x7f",
    119: "\x04", 121: "\x0c", 123: "\x1c", 124: "\x1d", 125: "\x1f",
    126: "\x1e", 67: "*", 69: "+", 75: "/", 78: "-", 81: "=",
    82: "0", 83: "1", 84: "2", 85: "3", 86: "4", 87: "5", 88: "6",
    89: "7", 91: "8", 92: "9",
}
for fk in (122, 120, 99, 118, 96, 97, 98, 100, 101, 109, 103, 111, 105,
           107, 113, 106, 64, 79, 80, 90):
    SPECIAL[fk] = "\x10"

COL_TO_LAYER = {0: 0, 1: 1, 3: 2}  # klc column index -> mac keyMap index


def parse_klc(path):
    layers = {0: {}, 1: {}, 2: {}}
    dead_key = None
    dead_table = {}
    section = None
    vk_to_sc = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.split("//")[0].rstrip()
            if not line.strip():
                continue
            head = line.split()[0]
            if head in ("LAYOUT", "LIGATURE", "KEYNAME", "KEYNAME_EXT",
                        "KEYNAME_DEAD", "DESCRIPTIONS", "LANGUAGENAMES",
                        "SHIFTSTATE", "ENDKBD"):
                section = head
                continue
            if head == "DEADKEY":
                section = "DEADKEY"
                dead_key = chr(int(line.split()[1], 16))
                continue
            f = line.split()
            if section == "LAYOUT":
                sc, vk, cols = f[0].lower(), f[1], f[3:]
                vk_to_sc[vk] = sc
                for i, val in enumerate(cols):
                    if i not in COL_TO_LAYER or val in ("-1", "%%"):
                        continue
                    is_dead = val.endswith("@")
                    ch = chr(int(val.rstrip("@"), 16))
                    layers[COL_TO_LAYER[i]][SC_TO_MAC[sc]] = (ch, is_dead)
            elif section == "LIGATURE":
                vk, mod, chars = f[0], int(f[1]), f[2:]
                text = "".join(chr(int(c, 16)) for c in chars)
                code = SC_TO_MAC[vk_to_sc[vk]]
                layers[COL_TO_LAYER[mod]][code] = (text, False)
            elif section == "DEADKEY":
                dead_table[chr(int(f[0], 16))] = chr(int(f[1], 16))
    return layers, dead_key, dead_table


def ent(s):
    return "".join(f"&#x{ord(c):04X};" for c in s)


def build_keylayout(layers, dead_key, dead_table):
    state = "hasanta"
    actions = {}  # id -> list of (state, output|None, next|None)

    def key_xml(code, text, is_dead, layer_has_actions=True):
        if is_dead:
            aid = "dead_hasanta"
            actions[aid] = [("none", None, state), (state, dead_key, state)]
            return f'<key code="{code}" action="{aid}"/>'
        if layer_has_actions and text in dead_table:
            aid = f"act_{ord(text):04X}"
            actions[aid] = [("none", text, None), (state, dead_table[text], None)]
            return f'<key code="{code}" action="{aid}"/>'
        return f'<key code="{code}" output="{ent(text)}"/>'

    maps = []
    # 0 base, 1 shift, 2 option, 3 shift+option (empty in source)
    for idx in range(4):
        keys = dict((c, key_xml(c, ch, d)) for c, (ch, d) in layers.get(idx, {}).items())
        maps.append(keys)
    # ISO keyboards' extra key (left of 1 / next to Shift) mirrors the ` key
    for idx in (0, 1):
        if 50 in maps[idx]:
            maps[idx].setdefault(10, maps[idx][50].replace('code="50"', 'code="10"'))
    # space should still type a space with Option held
    for idx in (2, 3):
        maps[idx].setdefault(49, key_xml(49, " ", False, False))
        maps[idx].setdefault(65, key_xml(65, ".", False, False))
    # 4 command -> qwerty, 5 control -> control chars
    cmd = {c: f'<key code="{c}" output="{ent(ch)}"/>' for c, ch in QWERTY.items()}
    ctrl = {}
    for c, ch in QWERTY.items():
        if "a" <= ch <= "z":
            out = chr(ord(ch) - 96)
        else:
            out = {"[": "\x1b", "\\": "\x1c", "]": "\x1d"}.get(ch, ch)
        ctrl[c] = f'<key code="{c}" output="{ent(out)}"/>'
    maps += [cmd, ctrl]
    for keys in maps:
        for c, s in SPECIAL.items():
            keys.setdefault(c, f'<key code="{c}" output="{ent(s)}"/>')

    out = []
    w = out.append
    w('<?xml version="1.1" encoding="UTF-8"?>')
    w('<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">')
    w(f'<keyboard group="126" id="{LAYOUT_ID}" name="{NAME}" maxout="4">')
    w('  <layouts>')
    w('    <layout first="0" last="17" mapSet="ANSI" modifiers="Modifiers"/>')
    w('  </layouts>')
    w('  <modifierMap id="Modifiers" defaultIndex="0">')
    for idx, mods in [
        (0, ["", "caps"]),
        (1, ["anyShift caps?"]),
        (2, ["anyOption caps?"]),
        (3, ["anyShift anyOption caps?"]),
        (4, ["command anyShift? anyOption? caps? anyControl?"]),
        (5, ["anyControl anyShift? anyOption? caps?"]),
    ]:
        w(f'    <keyMapSelect mapIndex="{idx}">')
        for m in mods:
            w(f'      <modifier keys="{m}"/>')
        w('    </keyMapSelect>')
    w('  </modifierMap>')
    w('  <keyMapSet id="ANSI">')
    for idx, keys in enumerate(maps):
        w(f'    <keyMap index="{idx}">')
        for c in sorted(keys):
            w(f'      {keys[c]}')
        w('    </keyMap>')
    w('  </keyMapSet>')
    w('  <actions>')
    for aid in sorted(actions):
        w(f'    <action id="{aid}">')
        for st, o, nxt in actions[aid]:
            attrs = f'state="{st}"'
            if o is not None:
                attrs += f' output="{ent(o)}"'
            if nxt is not None:
                attrs += f' next="{nxt}"'
            w(f'      <when {attrs}/>')
        w('    </action>')
    w('  </actions>')
    w('  <terminators>')
    w(f'    <when state="{state}" output="{ent(dead_key)}"/>')
    w('  </terminators>')
    w('</keyboard>')
    return "\n".join(out) + "\n"


def main():
    layers, dead_key, dead_table = parse_klc(KLC)
    xml = build_keylayout(layers, dead_key, dead_table)

    if os.path.exists(BUNDLE):
        shutil.rmtree(BUNDLE)
    res = os.path.join(BUNDLE, "Contents", "Resources")
    os.makedirs(os.path.join(res, "en.lproj"))
    with open(os.path.join(res, f"{FILE_BASE}.keylayout"), "w", encoding="utf-8") as fh:
        fh.write(xml)
    with open(os.path.join(res, "en.lproj", "InfoPlist.strings"), "w", encoding="utf-16") as fh:
        fh.write(f'"{NAME}" = "{NAME}";\n')
    info = {
        "CFBundleIdentifier": BUNDLE_ID,
        "CFBundleName": NAME,
        "CFBundleVersion": "1.0",
        "CFBundleShortVersionString": "1.0",
        "CFBundleDevelopmentRegion": "en",
        f"KLInfo_{NAME}": {
            "TISInputSourceID": f"{BUNDLE_ID}.unijoy",
            "TISIntendedLanguage": "bn",
        },
    }
    with open(os.path.join(BUNDLE, "Contents", "Info.plist"), "wb") as fh:
        plistlib.dump(info, fh)
    # also drop a standalone copy next to the bundle
    with open(os.path.join(HERE, f"{FILE_BASE}.keylayout"), "w", encoding="utf-8") as fh:
        fh.write(xml)
    print("Built", BUNDLE)


if __name__ == "__main__":
    main()
