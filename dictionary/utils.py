import emoji


def get_first_emoji(word):
    emoji_re = emoji.get_emoji_regexp()
    match = emoji_re.search(word)
    if match is None:
        return None
    return match.group(1)
