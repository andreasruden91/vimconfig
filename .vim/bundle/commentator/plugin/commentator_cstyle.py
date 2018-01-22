import vim

comment_start = '/*'
comment_end = '*/'
end_replace = '^/'

def main():
    assert len(comment_start) == len(comment_end) == len(end_replace)

    # Get selected lines
    buf = vim.current.buffer
    (srow, scol) = buf.mark('<')
    (erow, ecol) = buf.mark('>')
    lines = vim.eval('getline(%d, %d)' % (srow, erow))

    if len(lines) == 0:
        return

    # Advance scol to after indentation if needed
    if scol == 0:
        while scol < len(lines[0]) and (lines[0][scol]).isspace():
            scol += 1
    
    if ecol == (1 << 31) - 1:
        ecol = len(lines[-1])
    elif ecol < len(lines[-1]):
        ecol += 1

    try:
        start = lines[0][scol:scol + len(comment_start)]
    except IndexError:
        start = ''
    if start != comment_start:
        # Disable all comment ends currently in multi-line text
        if srow != erow:
            lines = [l.replace(comment_end, end_replace) for l in lines]
        insert_comment(srow, erow, scol, ecol, lines)
    else:
        remove_comment(srow, erow, scol, ecol, lines)
        # Restore old comment ends in multi-line text
        if srow != erow:
            lines = [l.replace(end_replace, comment_end) for l in lines]

    # Escape strings before feeding to vim
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace('\\', '\\\\')
        lines[i] = lines[i].replace('"', '\\"')

    # Write changes
    i = srow
    for line in lines:
        vim.eval('setline(%d, "%s")' % (i, line))
        i += 1

def insert_comment(srow, erow, scol, ecol, lines):
    # Single word selection (no extra spaces)
    if srow == erow and not ' ' in lines[0][scol:ecol]:
        lines[0] = (lines[0][:scol] + comment_start + lines[0][scol:ecol] +
            comment_end + lines[0][ecol:])
    # Multi-word or line selection
    else:
        add = comment_start + ' '
        lines[0] = lines[0][:scol] + add + lines[0][scol:]
        if srow == erow:
            ecol += len(add)
        lines[-1] = lines[-1][:ecol] + ' ' + comment_end + lines[-1][ecol:]

def remove_comment(srow, erow, scol, ecol, lines):
    space = not (srow == erow and not ' ' in lines[0][scol:ecol])
    # Remove comment start
    lines[0] = list(lines[0])
    for _ in range(0, len(comment_start) + (1 if space else 0)):
        del lines[0][scol]
    lines[0] = ''.join(lines[0])
    # Adjust ecol
    ecol -= (len(comment_end) + (1 if space else 0)) * (2 if srow == erow else
        1)
    # Remove comment end
    lines[-1] = list(lines[-1])
    for _ in range(0, len(comment_end) + (1 if space else 0)):
        del lines[-1][ecol]
    lines[-1] = ''.join(lines[-1])

def disable_old_comments(lines):
    for i in range(0, len(lines - 1)):
        lines[i].replace(comment_end, end_replace)

if __name__ == '__main__':
    main()
