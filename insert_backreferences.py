"""We use BACKREFMARKER to mark backreference links so we don't have a loop of reference
This is a bit hacky as bear x-callback api ignores the title argument when the ID argument
is passed. THis allows to add some meta-data in the title argument of open-note:
"""

import bear_api
from collections import defaultdict
from bear_note import BearNote
from constants import USE_HEADER_LINKS, BACKREFMARKER, BACKREFERENCES_INTRO_TEXT, BACKREFERENCES_SECTION, BACKREFERENCE_PREFIX
from links import Link, HeaderLink
from ordered_set import OrderedSet


def main():
    bear_notes = [BearNote(note) for note in bear_api.notes()]
    notes = {note.title: note for note in bear_notes}
    backreferences, _ = find_all_links(notes)
    for note_id, note in notes.items():
        if "#_index" in note.text:
            continue

        note_back_refs = backreferences[note_id]
        if note_back_refs:
            new_note_content = ''.join(text_lines(note, backref_links=note_back_refs))
            bear_api.replace_note_text(note, new_note_content)



def markdown_link_list(links, add_intro=True):
    if not links:
        return []

    if add_intro:
        intro_markdown = BACKREFERENCES_SECTION + BACKREFERENCES_INTRO_TEXT
    else:
        intro_markdown = ""
    backref_links_text = '\n'.join(f"{BACKREFERENCE_PREFIX} {bear_api.markdown_link(l)}" for l in links)
    return intro_markdown + backref_links_text


def find_all_links(notes):
    backreferences = defaultdict(OrderedSet)
    out_links = dict()
    for note in notes.values():
        if "#_daily" in note.text:
            continue

        out_links[note.title] = list(note.outgoing_links)
        for out_link in out_links[note.title]:
            if not is_a_backreference(out_link):
                backref = Link(title=note.title)
                backreferences[out_link.title].add(backref)
    return backreferences, out_links



def filter_out_existing_links(backreferences, out_links):
    return {note_id: note_filter_out_existing_links(links, out_links[note_id]) for note_id, links in backreferences.items()}


def note_filter_out_existing_links(backreferences, out_links):
    return [l for l in backreferences if l.href_id not in [l.href_id for l in out_links]]


def filter_out_self_links(backreferences, out_links):
    return {note_id: [l for l in links if l.href_id != note_id] for note_id, links in backreferences.items()}


def is_a_backreference(link):
    try:
        return link.open_note_title == BACKREFMARKER
    except AttributeError:
        return False


def is_valid_reference(notes, link):
    is_note_link = not hasattr(link, 'header')
    if is_note_link:
        return link.href_id in notes.keys()
    else:
        return link.header in set(title for title, content in notes[link.href_id].sections)


def text_lines(note, backref_links=None):
    """
        :param backref_links: add back reference links in the right place.
            The right place is defined as the place where existing back references
            were found. If no backreference was found they are just added
            at the very end of the note. (Maybe we can append them before the tags,
            just like add-text with append does in the Bear API?
            I prefer it like this personally)
    """
    marker = BACKREFERENCES_SECTION + BACKREFERENCES_INTRO_TEXT
    text = note.text

    try:
        text = text[:text.index(marker)]
    except Exception:
        text = text

    return text + markdown_link_list(sorted(backref_links))


if __name__ == "__main__":
    bear_notes = [BearNote(note) for note in bear_api.notes()]
    titles = []
    valid = True
    for n in bear_notes:
        if n.title in titles:
            print("DUPLICATED!!!", n.title)
            valid = False

        titles.append(n.title)

    if valid:
        main()
