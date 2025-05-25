import re

# For input checking (DB tampering, system commands, etc.)
INPUT_BLACKLIST = [
    # Ex: DB tampering.
    r"(drop\s+table|all\s+users|users|;.*--|/\*)",
    # Ex: system files.
    r'(contents of /etc/passwd|contents of /etc/shadow)',
    # Ex: Prompt Leaking.
    r'(system prompt|prompt template|above text|top of)'
]

# For output check (DB information leak, system critical information, etc.)
OUTPUT_BLACKLIST = [
    # Ex: other user's name.
    r"(Carol|Charlie|Dave|Bob)",
    # Ex: content of /etc/passwd.
    r"(root\:x|/root\:/bin)"
]

def contains_blacklisted_pattern(text: str, patterns: list[str]) -> bool:
    # "True" if it matches any of the regular expression patterns in the list.
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
