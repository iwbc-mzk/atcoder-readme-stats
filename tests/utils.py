import cssutils
from cssutils.css import CSSStyleSheet


def get_property_from_css(css, class_or_id, property):
    for rule in css.cssRules:
        if rule.typeString == "STYLE_RULE" and rule.selectorText == class_or_id:
            return rule.style[property]
    return None


def serialize_css(css: str) -> CSSStyleSheet:
    css = css.replace("\n", "")
    c = []
    q = False
    for s in css:
        if s in ["'", '"']:
            q = not q
        if q or s != " ":
            c.append(s)

    css = "".join(c)
    return cssutils.parseString(css)
