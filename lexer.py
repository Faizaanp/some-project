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
    line_number = 1
    line_end = 0

    column_start = 0
    column_end = 0

    # Building TOKENS list
    named_patterns = []
    for token_name, pattern in TOKENS:
        named_patterns.append(f"(?P<{token_name}>{pattern})")
    master_pattern = "|".join(named_patterns)

    token_re = re.compile(master_pattern)

    
    indent_stack = [0]  # Stack to track indentation levels

    matches = list(token_re.finditer(code))
    total_length = len(matches)
    
    for i, match in enumerate(matches):
        token_type = match.lastgroup
        token_value = match.group()
        column_start = match.start() - line_start
        column_end = match.end() - line_start

        if token_type == "NEWLINE":
            line_start = match.end()
            line_number += 1

            column_start = 0
            column_end = 0

            if i + 1 < total_length:
                next_token = matches[i + 1]

                # Skip blank and comment lines
                if next_token.lastgroup in ("NEWLINE", "COMMENT"):
                    continue  

                # indentation
                indent_match = re.match(r"[ \t]*", code[line_start:])
                if indent_match:
                    indent = len(indent_match.group().replace("\t", "    "))
                    if indent > indent_stack[-1]:
                        indent_stack.append(indent)
                        tokens.append(("INDENT", indent, line_number, 0, indent))
                    while indent < indent_stack[-1]:
                        indent_stack.pop()
                        tokens.append(("DEDENT", indent, line_number, 0, indent))
            continue

        if token_type == "NUMBER":
            # num validation 
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

    #  dedents at EOF
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(("DEDENT", 0, line_number, 0, 0))

    return tokens
