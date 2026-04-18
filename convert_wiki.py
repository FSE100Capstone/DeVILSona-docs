"""
Convert GitHub Wiki markdown files to MkDocs-compatible format.
- Converts [[Display Text|Page-Name]] links to [Display Text](path/to/page.md)
- Converts [[Page-Name]] links (no display text) to [Page-Name](path/to/page.md)
- Copies files into organized subdirectories
"""
import re
import shutil
from pathlib import Path

WIKI_DIR = Path(r"c:\Users\Sean\dev\DeVILSona.wiki")
DOCS_DIR = Path(r"c:\Users\Sean\dev\DeVILSona-docs\docs")

# Map wiki page names to their MkDocs paths (relative to docs/)
PAGE_MAP = {
    # Home
    "Home": "index.md",
    
    # Educator Guide
    "Educator-Guide-Welcome-to-DeVILSona": "educator-guide/welcome.md",
    "Educator-Guide-Classroom-Setup-&-Hardware": "educator-guide/classroom-setup.md",
    "Educator-Guide-Running-a-Session": "educator-guide/running-a-session.md",
    "Educator-Guide-Student-Safety-&-Privacy": "educator-guide/safety-privacy.md",
    "Educator-Guide-Troubleshooting": "educator-guide/troubleshooting.md",
    
    # Admin Guide
    "Admin-Guide-System-Architecture-Overview": "admin-guide/system-architecture.md",
    "Admin-Guide-Hardware-Provisioning-&-Sideloading": "admin-guide/hardware-provisioning.md",
    "Admin-Guide-Network-Configuration": "admin-guide/network-configuration.md",
    "Admin-Guide-Backend-&-Cloud-Operations": "admin-guide/backend-cloud.md",
    "Admin-Guide-Logging-&-Incident-Response": "admin-guide/logging-incident-response.md",
    
    # Developer Guide
    "Developer-Guide-Onboarding-&-Environment-Setup": "developer-guide/onboarding.md",
    "Developer-Guide-Core-Architecture": "developer-guide/core-architecture.md",
    "Developer-Guide-AI-Pipeline": "developer-guide/ai-pipeline.md",
    "Developer-Guide-UE5-Implementation": "developer-guide/ue5-implementation.md",
    "Developer-Guide-Infrastructure-&-Cloud": "developer-guide/infrastructure-cloud.md",
    "Developer-Guide-Contribution-Guidelines": "developer-guide/contribution-guidelines.md",
    "Developer-Guide-Known-Issues-&-Roadmap": "developer-guide/known-issues-roadmap.md",
    "Developer-Guide-Learning-Paths": "developer-guide/learning-paths.md",
    
    # Legacy
    "Legacy/AWS-Save-System": "legacy/aws-save-system.md",
    "Legacy/AWS-Terraform": "legacy/aws-terraform.md",
    "Legacy/Auto-generated-API-Documentation": "legacy/api-documentation.md",
    "Legacy/Mac-Setup-&-Limitations-for-Unreal-Engine-(OVRLipSync,-VR,-and-AI-Integration)": "legacy/mac-setup-limitations.md",
    "Legacy/Meta-XR-Plugin": "legacy/meta-xr-plugin.md",
    "Legacy/MetaHuman-Creator": "legacy/metahuman-creator.md",
    "Legacy/Oculus-LipSync-Plugin": "legacy/oculus-lipsync.md",
    "Legacy/Save-System": "legacy/save-system.md",
    "Legacy/Subsystems": "legacy/subsystems.md",
    "Legacy/Unreal-Engine-Build-&-Packaging-Guide-(Android(apk))": "legacy/build-android-apk.md",
    "Legacy/Unreal-Engine-Build-&-Packaging-Guide-(Windows-\u2013-Shipping)": "legacy/build-windows-shipping.md",
    "Legacy/Unreal-Engine-Build-&-Packaging-Guide-(Windows---Shipping)": "legacy/build-windows-shipping.md",
}

# Reverse map: source file → dest path
FILE_COPY_MAP = {
    "Home.md": "index.md",
    "Educator-Guide-Welcome-to-DeVILSona.md": "educator-guide/welcome.md",
    "Educator-Guide-Classroom-Setup-&-Hardware.md": "educator-guide/classroom-setup.md",
    "Educator-Guide-Running-a-Session.md": "educator-guide/running-a-session.md",
    "Educator-Guide-Student-Safety-&-Privacy.md": "educator-guide/safety-privacy.md",
    "Educator-Guide-Troubleshooting.md": "educator-guide/troubleshooting.md",
    "Admin-Guide-System-Architecture-Overview.md": "admin-guide/system-architecture.md",
    "Admin-Guide-Hardware-Provisioning-&-Sideloading.md": "admin-guide/hardware-provisioning.md",
    "Admin-Guide-Network-Configuration.md": "admin-guide/network-configuration.md",
    "Admin-Guide-Backend-&-Cloud-Operations.md": "admin-guide/backend-cloud.md",
    "Admin-Guide-Logging-&-Incident-Response.md": "admin-guide/logging-incident-response.md",
    "Developer-Guide-Onboarding-&-Environment-Setup.md": "developer-guide/onboarding.md",
    "Developer-Guide-Core-Architecture.md": "developer-guide/core-architecture.md",
    "Developer-Guide-AI-Pipeline.md": "developer-guide/ai-pipeline.md",
    "Developer-Guide-UE5-Implementation.md": "developer-guide/ue5-implementation.md",
    "Developer-Guide-Infrastructure-&-Cloud.md": "developer-guide/infrastructure-cloud.md",
    "Developer-Guide-Contribution-Guidelines.md": "developer-guide/contribution-guidelines.md",
    "Developer-Guide-Known-Issues-&-Roadmap.md": "developer-guide/known-issues-roadmap.md",
    "Developer-Guide-Learning-Paths.md": "developer-guide/learning-paths.md",
}

LEGACY_FILE_MAP = {
    "AWS-Save-System.md": "legacy/aws-save-system.md",
    "AWS-Terraform.md": "legacy/aws-terraform.md",
    "Auto-generated-API-Documentation.md": "legacy/api-documentation.md",
    "Mac-Setup-&-Limitations-for-Unreal-Engine-(OVRLipSync,-VR,-and-AI-Integration).md": "legacy/mac-setup-limitations.md",
    "Meta-XR-Plugin.md": "legacy/meta-xr-plugin.md",
    "MetaHuman-Creator.md": "legacy/metahuman-creator.md",
    "Oculus-LipSync-Plugin.md": "legacy/oculus-lipsync.md",
    "Save-System.md": "legacy/save-system.md",
    "Subsystems.md": "legacy/subsystems.md",
    "Unreal-Engine-Build-&-Packaging-Guide-(Android(apk)).md": "legacy/build-android-apk.md",
    "Unreal-Engine-Build-&-Packaging-Guide-(Windows-\u2013-Shipping).md": "legacy/build-windows-shipping.md",
}


def compute_relative_link(from_path: str, to_path: str) -> str:
    """Compute a relative link from one docs file to another."""
    from_parts = Path(from_path).parent.parts
    to_parts = Path(to_path).parts
    
    # Find common prefix length
    common = 0
    for a, b in zip(from_parts, to_parts):
        if a == b:
            common += 1
        else:
            break
    
    # Go up from source, then down to target
    up_count = len(from_parts) - common
    relative_parts = [".."] * up_count + list(to_parts[common:])
    
    if not relative_parts:
        return Path(to_path).name
    
    return "/".join(relative_parts)


def convert_wiki_links(content: str, current_file_path: str) -> str:
    """Convert [[Display|Page]] and [[Page]] wiki links to standard markdown links."""
    
    def replace_link(match):
        inner = match.group(1)
        if "|" in inner:
            display, page = inner.split("|", 1)
            display = display.strip()
            page = page.strip()
        else:
            display = inner.strip()
            page = inner.strip()
        
        # Handle same-page anchor links
        if page.startswith("#"):
            return f"[{display}]({page})"
        
        # Look up the page in our map
        if page in PAGE_MAP:
            target = PAGE_MAP[page]
            rel_link = compute_relative_link(current_file_path, target)
            return f"[{display}]({rel_link})"
        else:
            # Fallback: just make it a plain text reference
            print(f"  WARNING: Could not resolve link [[{inner}]] in {current_file_path}")
            return f"[{display}](#)"
    
    # Match [[...]] patterns, being careful not to match inside code blocks
    # Simple approach: just replace all [[...]] patterns
    result = re.sub(r'\[\[(.+?)\]\]', replace_link, content)
    return result


def convert_wiki_tables_with_links(content: str, current_file_path: str) -> str:
    """
    Handle the escaped wiki links inside markdown tables.
    In Home.md, links are escaped as [[text\\|page]] inside table cells.
    """
    def replace_escaped_link(match):
        inner = match.group(1)
        if "\\|" in inner:
            display, page = inner.split("\\|", 1)
            display = display.strip()
            page = page.strip()
            
            if page in PAGE_MAP:
                target = PAGE_MAP[page]
                rel_link = compute_relative_link(current_file_path, target)
                return f"[{display}]({rel_link})"
            else:
                print(f"  WARNING: Could not resolve escaped link in {current_file_path}")
                return f"[{display}](#)"
        return match.group(0)
    
    result = re.sub(r'\[\[(.+?)\]\]', replace_escaped_link, content)
    return result


def process_file(src: Path, dest_relative: str):
    """Read a wiki file, convert links, write to docs/."""
    content = src.read_text(encoding="utf-8")
    dest_path = DOCS_DIR / dest_relative
    
    # First handle escaped pipe links (tables), then normal links
    content = convert_wiki_tables_with_links(content, dest_relative)
    content = convert_wiki_links(content, dest_relative)
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(content, encoding="utf-8")
    print(f"  {src.name} -> {dest_relative}")


def main():
    print("Converting wiki files to MkDocs format...\n")
    
    # Process main files
    print("Main pages:")
    for src_name, dest_path in FILE_COPY_MAP.items():
        src = WIKI_DIR / src_name
        if src.exists():
            process_file(src, dest_path)
        else:
            print(f"  MISSING: {src_name}")
    
    # Process legacy files
    print("\nLegacy pages:")
    for src_name, dest_path in LEGACY_FILE_MAP.items():
        src = WIKI_DIR / "Legacy" / src_name
        if src.exists():
            process_file(src, dest_path)
        else:
            print(f"  MISSING: Legacy/{src_name}")
    
    print("\nDone! All files converted.")


if __name__ == "__main__":
    main()
