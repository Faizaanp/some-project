import re

TOKENS = [
    ("KEYWORD", r"\b(def|for|if|else|elif|return|print|in|while|import|from|as|break|continue|class|pass|and|or|not|True|False|None|global|nonlocal|lambda|try|except|finally|raise|with|yield|assert|del|is)\b"),
    ("NUMBER", r"\b\d+(\.\d+)?([eE][+-]?\d+)?\b"),  
    ("STRING", r"(\"\"\"([^\"\\]|\\.)*\"\"\"|\'\'\'([^\'\\]|\\.)*\'\'\'|\"([^\"\\]|\\.)*\"|\'([^\'\\]|\\.)*\')"),  
    ("IDENT",  r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("SYMBOL", r"(==|!=|<=|>=|\*\*|//|->|:=|[()\[\]{},:;=+\-*/%<>|&^~.])"),
    ("NEWLINE", r"\n"),
    ("SKIP",   r"[ \t]+"),
    ("COMMENT", r"#.*"),
    ("MISMATCH", r".")
]


def tokenize(code):
    """
    Convert source code into a list of (TOKEN_TYPE, TOKEN_VALUE, LINE_NUMBER, COLUMN_START, COLUMN_END) tuples.
    """
    tokens = []
    
    line_start = 0
    line_number = 1  # Ensure line_number starts at 1

    indent_stack = [0]  # Stack to track indentation levels

    column_start = 0
    column_end = 0

    # Building TOKENS list
    named_patterns = []
    for token_name, pattern in TOKENS:
        named_patterns.append(f"(?P<{token_name}>{pattern})")
    master_pattern = "|".join(named_patterns)

    token_re = re.compile(master_pattern)

    matches = list(token_re.finditer(code))
    total_length = len(matches)
    
    for i, match in enumerate(matches):
        token_type = match.lastgroup
        token_value = match.group()
        column_start = match.start() - line_start
        column_end = match.end() - line_start

        if token_type == "NEWLINE":
            line_start = match.end()
            line_number += 1  # Increment line_number for each NEWLINE

            # Reset column positions for NEWLINE tokens
            column_start = 0
            column_end = 0

            if i + 1 < total_length:
                next_token = matches[i + 1].lastgroup

                if next_token not in ("NEWLINE", "COMMENT"):
                    indent_match = re.match(r"[ \t]*", code[line_start:])
                    if indent_match:
                        indent_str = indent_match.group()
                        if "\t" in indent_str and " " in indent_str:
                            raise SyntaxError("Mixed tabs and spaces detected for indentation.")
                        indent_len = len(indent_str.replace("\t", "    "))

                        if indent_len > indent_stack[-1]:
                            indent_stack.append(indent_len)
                            tokens.append(("INDENT", indent_len, line_number, 0, indent_len))
                        while indent_len < indent_stack[-1]:
                            indent_stack.pop()
                            tokens.append(("DEDENT", indent_len, line_number, 0, indent_len))
            continue

        if token_type == "STRING":
            # Adjust column_end for multi-line strings
            lines_in_string = token_value.splitlines()
            if len(lines_in_string) > 1:
                start_line = line_number
                end_line = line_number + len(lines_in_string) - 1
                line_number = end_line
                line_start = match.end() - len(lines_in_string[-1])
                column_end = len(lines_in_string[-1])
                tokens.append((token_type, token_value, start_line, column_start, end_line, column_end))
                continue

        if token_type == "NUMBER":
            # Validate number format before conversion
            if re.fullmatch(r"\d+\.\d+", token_value):
                token_value = float(token_value)
            elif re.fullmatch(r"\d+", token_value):
                token_value = int(token_value)
            else:
                lines = code.splitlines()
                line_text = lines[line_number-1] if line_number-1 < len(lines) else ""
                raise SyntaxError(f"Unexpected character: {token_value} at line {line_number}, col {column_start}\nLine: {line_text}")

        if token_type in ("SKIP", "COMMENT"):
            continue

        if token_type == "MISMATCH":
            raise SyntaxError(f"Unexpected character: {token_value} at line {line_number}, col {column_start}")

        tokens.append((token_type, token_value, line_number, column_start, column_end))

    # Handle remaining dedents at the end of the file
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(("DEDENT", 0, line_number, 0, 0))

    return tokens
