def sideBySideText(texts, width):
    columnWidth = width / len(texts)
    columnStringFormat = "%%-%ds" % (columnWidth)
    texts = map(lambda x: map(lambda y: y.strip(), x.split("\n")), texts)
    maxLines = max(map(lambda x: len(x), texts))
    map(lambda x: x.extend([""] * (maxLines - len(x))), texts)
    lines = map(lambda x: map(lambda y: columnStringFormat % y[:columnWidth], x), zip(*texts))
    return "\n".join(map(lambda x: " ".join(x), lines))

