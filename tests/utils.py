def get_property_from_css(css, class_or_id, property):
    for rule in css.cssRules:
        if rule.typeString == "STYLE_RULE" and rule.selectorText == class_or_id:
            return rule.style[property]
    return None
