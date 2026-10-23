#!/usr/bin/env python3
"""Build an allowlisted OpenAI draft ZIP and inspect the archive we wrote.

Usage: python3 scripts/package-openai.py /absolute/path/openwhispr-1.0.0.zip
No dependencies, network access, account access, or credential files are needed.
Portal scans, OAuth, reviewer access and demo playback are separate checks.
"""

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import struct
import sys
import unicodedata
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "ask-my-notes", "dictionary-builder", "meeting-recap",
    "snippet-builder", "transcribe-recording", "weekly-review",
)
PACKAGE_FILES = (
    "plugin.json", "mcp.json", "LICENSE", "assets/icon.png",
    *(f"skills/{name}/SKILL.md" for name in SKILLS),
)
OAUTH_SCOPES = [
    "notes:read", "notes:write", "transcriptions:read", "transcriptions:write",
    "usage:read", "dictionary:read", "dictionary:write", "snippets:read",
    "snippets:write", "openid", "email",
]
CATEGORIES = {
    "Business & Operations", "Communication", "Creativity", "Data & Analytics",
    "Developer Tools", "Education & Research", "Entertainment", "Finance",
    "Healthcare", "Other", "Productivity", "Scientific Research", "Security", "Travel",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def short_text(value, limit, label):
    require(isinstance(value, str) and value.strip(), f"{label}: nonempty text required")
    require(len(value) <= limit and not any(c in value for c in "\r\n"), f"{label}: length/line limit")


def validate(archive):
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, "ZIP integrity failed")
        names = z.namelist()
        require(sorted(names) == sorted(PACKAGE_FILES), "Archive differs from the explicit file allowlist")
        require(len(names) <= 5000, "Too many archive entries")
        require(sum(i.file_size for i in z.infolist()) <= 512 * 1024**2, "Archive too large")
        normalized = [unicodedata.normalize("NFC", n).casefold() for n in names]
        require(len(set(normalized)) == len(names), "Duplicate/colliding archive paths")
        for n in names:
            path = PurePosixPath(n)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in n, "Unsafe archive path")
            require(len(path.parts) <= 20, "Archive path too deep")
            require(not any(p.startswith(".") for p in path.parts), "Unexpected hidden file")
        m = json.loads(z.read("plugin.json"))
        require(m["name"] == "openwhispr" and m["version"] == "1.0.0", "Unexpected plugin identity")
        require(not any(k in m for k in ["apps", "hooks", "mcpServers", "skills", "interface"]), "Unsupported root fields")
        oa = m["extensions"]["com.openai"]
        require("apps" not in oa and ".app.json" not in names, "App references are forbidden")
        ui = oa["interface"]
        for field, limit in [("displayName", 30), ("shortDescription", 30), ("developerName", 80)]:
            short_text(ui[field], limit, field)
        require(0 < len(ui["longDescription"]) <= 4000, "Long description length")
        require(ui["category"] in CATEGORIES, "Unsupported category")
        require(len(ui["capabilities"]) <= 20, "Too many capabilities")
        for capability in ui["capabilities"]:
            short_text(capability, 120, "capability")
        prompts = ui["defaultPrompt"]
        require(isinstance(prompts, list) and len(prompts) <= 3, "Starter prompts must be a list of at most 3")
        for prompt in prompts:
            short_text(prompt, 128, "starter prompt")
            require("@" not in prompt, "Starter prompt contains an app mention")
        require(len({" ".join(unicodedata.normalize("NFKC", p).split()) for p in prompts}) == len(prompts), "Duplicate starter prompts")
        from urllib.parse import urlparse
        for field in ["websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"]:
            value = ui[field]
            parsed = urlparse(value)
            require(len(value) <= 1024 and parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password, f"Invalid {field}")
        require(re.fullmatch(r"#[0-9A-Fa-f]{6}", ui["brandColor"]), "Invalid brand color")
        rgb = [int(ui["brandColor"][i:i+2], 16) / 255 for i in (1, 3, 5)]
        channels = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055)**2.4 for c in rgb]
        contrast = 1.05 / (sum(c*w for c,w in zip(channels, [0.2126, 0.7152, 0.0722])) + 0.05)
        require(contrast >= 2, "Brand color must contrast at least 2:1 with white")
        for field, minimum in [("logo", 256), ("composerIcon", 48)]:
            ref = ui[field]
            require(ref.startswith("./") and ".." not in PurePosixPath(ref).parts, "Unsafe icon reference")
            data = z.read(ref[2:])
            require(data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) <= 5 * 1024**2, "Invalid PNG")
            width, height = struct.unpack(">II", data[16:24])
            require(width == height and minimum <= width <= 4096, f"Invalid {field} dimensions")
        config = json.loads(z.read("mcp.json"))
        require(list(config["mcpServers"]) == ["openwhispr"], "Exactly one MCP server required")
        server = config["mcpServers"]["openwhispr"]
        require(server["type"] == "streamable-http" and server["url"] == "https://mcp.openwhispr.com/mcp", "Unexpected MCP endpoint")
        require(not server.get("headers"), "Embedded headers are forbidden")
        require(set(server) == {"type", "url", "extensions"}, "Unexpected MCP server fields")
        require(server["extensions"] == {"com.openai": {"auth": {
            "type": "oauth", "client": {"mode": "dcr"}, "baseScopes": OAUTH_SCOPES,
        }}}, "Declare OpenAI OAuth/DCR and the existing data plus identity scopes; no credentials or endpoint overrides")
        review = oa["review"]
        require(not any(k in review for k in ["test_credentials", "reviewer_instructions"]), "Reviewer access must stay outside the ZIP")
        cases = review["test_cases"]
        require(len(cases["positive"]) == 5 and len(cases["negative"]) == 3, "Need 5 positive and 3 negative cases")
        for kind in ["positive", "negative"]:
            for case in cases[kind]:
                for field in ["description", "prompt"] + (["tools_triggered", "expected_behavior"] if kind == "positive" else []):
                    require(isinstance(case[field], str) and case[field].strip(), f"Missing case {field}")
        require(oa["publication"]["countries"] == [], "Expected all-country availability")
        require(oa["publication"]["release_notes"].strip(), "Missing release notes")
        require(review["commerce"] is False, "Expected no-commerce declaration")
        skills = [n for n in names if re.fullmatch(r"skills/[^/]+/SKILL.md", n)]
        require(len(skills) == 6, "Expected six existing skills")
        for name in skills:
            text = z.read(name).decode()
            require(text.startswith("---\n"), f"Missing frontmatter: {name}")
            frontmatter = text.split("---", 2)[1]
            match = re.search(r"^name: (.+)$", frontmatter, re.M)
            description = re.search(r"^description: (.+)$", frontmatter, re.M)
            require(match and match[1] == PurePosixPath(name).parts[1], f"Skill name mismatch: {name}")
            require(description and len(description[1]) <= 1024, f"Skill description invalid: {name}")
            require(not re.search(r"claude|cowork", text, re.I), f"Provider-specific instructions: {name}")
        return {"files": len(names), "skills": len(skills), "mcp_servers": 1, "contrast_on_white": round(contrast, 2), "demo_recording_url_present": bool(review.get("demo_recording_url"))}


def main():
    require(len(sys.argv) == 2, "Provide the output ZIP path")
    output = Path(sys.argv[1]).expanduser().resolve()
    require(output.suffix == ".zip", "Output must be a ZIP")
    output.parent.mkdir(parents=True, exist_ok=True)
    files = [ROOT / name for name in PACKAGE_FILES]
    for p in files:
        require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(ROOT), "Missing files, symlinks or escaping paths are forbidden")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            info = zipfile.ZipInfo(p.relative_to(ROOT).as_posix(), (2026, 10, 21, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes())
    result = validate(output)
    result.update({"archive": str(output), "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "bytes": output.stat().st_size})
    print(json.dumps(result, indent=2))
    print("Draft archive checks passed. Demo video, deployed OAuth/domain verification, portal scans and attestations remain separate.")
    print("OpenAI's documented MCP auth extension is checked locally. The published generic MCP schema currently excludes that extension; see submission/validation.md.")


if __name__ == "__main__":
    main()
