jQuery.fn.extend({
    getPath: function () {
        var path, node = this;
        while (node.length) {
            var realNode = node[0], name = realNode.localName;

            var classes = jQuery(realNode).attr('class');
            var cls = '';
            if (classes) {
                classes = classes.split(' ');
                for (let i = 0; i < classes.length; i++) {
                    if (classes[i] && classes[i] !== 'gerapy-chosen') {
                        cls += '.' + classes[i];
                    }
                }
            }

            if (!name) break;
            name = name.toLowerCase();

            if (cls) {
                name = name + cls;
            }

            var parent = node.parent();

            var sameTagSiblings = parent.children(name);
            if (sameTagSiblings.length > 1) {
                var allSiblings = parent.children();
                var index = allSiblings.index(realNode) + 1;
                if (index > 1) {
                    name += ':nth-child(' + index + ')';
                }
            }

            if (name !== 'html') {
                path = name + (path ? ' > ' + path : '');
            }
            node = parent;

        }
        return path;
    }
});

(function () {
    var CssSelectorGenerator, root,
        indexOf = [].indexOf || function (item) {
                for (var i = 0, l = this.length; i < l; i++) {
                    if (i in this && this[i] === item) return i;
                }
                return -1;
            };

    CssSelectorGenerator = (function () {
        CssSelectorGenerator.prototype.default_options = {
            selectors: ['id', 'class', 'tag', 'nthchild']
        };

        function CssSelectorGenerator(options) {
            if (options === null) {
                options = {};
            }
            this.options = {};
            this.setOptions(this.default_options);
            this.setOptions(options);
        }

        CssSelectorGenerator.prototype.setOptions = function (options) {
            var key, results, val;
            if (options == null) {
                options = {};
            }
            results = [];
            for (key in options) {
                val = options[key];
                if (this.default_options.hasOwnProperty(key)) {
                    results.push(this.options[key] = val);
                } else {
                    results.push(void 0);
                }
            }
            return results;
        };

        CssSelectorGenerator.prototype.isElement = function (element) {
            return !!((element != null ? element.nodeType : void 0) === 1);
        };

        CssSelectorGenerator.prototype.getParents = function (element) {
            var current_element, result;
            result = [];
            if (this.isElement(element)) {
                current_element = element;
                while (this.isElement(current_element)) {
                    result.push(current_element);
                    current_element = current_element.parentNode;
                }
            }
            return result;
        };

        CssSelectorGenerator.prototype.getTagSelector = function (element) {
            return this.sanitizeItem(element.tagName.toLowerCase());
        };

        CssSelectorGenerator.prototype.sanitizeItem = function (item) {
            var characters;
            characters = (item.split('')).map(function (character) {
                if (character === ':') {
                    return "\\" + (':'.charCodeAt(0).toString(16).toUpperCase()) + " ";
                } else if (/[ !"#$%&'()*+,.\/;<=>?@\[\\\]^`{|}~]/.test(character)) {
                    return "\\" + character;
                } else {
                    return escape(character).replace(/\%/g, '\\');
                }
            });
            return characters.join('');
        };

        CssSelectorGenerator.prototype.getIdSelector = function (element) {
            var id, sanitized_id;
            id = element.getAttribute('id');
            if ((id != null) && (id !== '') && !(/\s/.exec(id)) && !(/^\d/.exec(id))) {
                sanitized_id = "#" + (this.sanitizeItem(id));
                if (element.ownerDocument.querySelectorAll(sanitized_id).length === 1) {
                    return sanitized_id;
                }
            }
            return null;
        };

        CssSelectorGenerator.prototype.getClassSelectors = function (element) {
            var class_string, item, result;
            result = [];
            class_string = element.getAttribute('class');
            if (class_string != null) {
                class_string = class_string.replace(/\s+/g, ' ');
                class_string = class_string.replace(/^\s|\s$/g, '');
                if (class_string !== '') {
                    result = (function () {
                        var k, len, ref, results;
                        ref = class_string.split(/\s+/);
                        results = [];
                        for (k = 0, len = ref.length; k < len; k++) {
                            item = ref[k];
                            results.push("." + (this.sanitizeItem(item)));
                        }
                        return results;
                    }).call(this);
                }
            }
            return result;
        };

        CssSelectorGenerator.prototype.getAttributeSelectors = function (element) {
            var attribute, blacklist, k, len, ref, ref1, result;
            result = [];
            blacklist = ['id', 'class'];
            ref = element.attributes;
            for (k = 0, len = ref.length; k < len; k++) {
                attribute = ref[k];
                if (ref1 = attribute.nodeName, indexOf.call(blacklist, ref1) < 0) {
                    result.push("[" + attribute.nodeName + "=" + attribute.nodeValue + "]");
                }
            }
            return result;
        };

        CssSelectorGenerator.prototype.getNthChildSelector = function (element) {
            var counter, k, len, parent_element, sibling, siblings;
            parent_element = element.parentNode;
            if (parent_element != null) {
                counter = 0;
                siblings = parent_element.childNodes;
                for (k = 0, len = siblings.length; k < len; k++) {
                    sibling = siblings[k];
                    if (this.isElement(sibling)) {
                        counter++;
                        if (sibling === element) {
                            return ":nth-child(" + counter + ")";
                        }
                    }
                }
            }
            return null;
        };

        CssSelectorGenerator.prototype.testSelector = function (element, selector) {
            var is_unique, result;
            is_unique = false;
            if ((selector != null) && selector !== '') {
                result = element.ownerDocument.querySelectorAll(selector);
                if (result.length === 1 && result[0] === element) {
                    is_unique = true;
                }
            }
            return is_unique;
        };

        CssSelectorGenerator.prototype.getAllSelectors = function (element) {
            var result;
            result = {
                t: null,
                i: null,
                c: null,
                a: null,
                n: null
            };
            if (indexOf.call(this.options.selectors, 'tag') >= 0) {
                result.t = this.getTagSelector(element);
            }
            if (indexOf.call(this.options.selectors, 'id') >= 0) {
                result.i = this.getIdSelector(element);
            }
            if (indexOf.call(this.options.selectors, 'class') >= 0) {
                result.c = this.getClassSelectors(element);
            }
            if (indexOf.call(this.options.selectors, 'attribute') >= 0) {
                result.a = this.getAttributeSelectors(element);
            }
            if (indexOf.call(this.options.selectors, 'nthchild') >= 0) {
                result.n = this.getNthChildSelector(element);
            }
            return result;
        };

        CssSelectorGenerator.prototype.testUniqueness = function (element, selector) {
            var found_elements, parent;
            parent = element.parentNode;
            found_elements = parent.querySelectorAll(selector);
            return found_elements.length === 1 && found_elements[0] === element;
        };

        CssSelectorGenerator.prototype.testCombinations = function (element, items, tag) {
            var item, k, l, len, len1, ref, ref1;
            ref = this.getCombinations(items);
            for (k = 0, len = ref.length; k < len; k++) {
                item = ref[k];
                if (this.testUniqueness(element, item)) {
                    return item;
                }
            }
            if (tag != null) {
                ref1 = items.map(function (item) {
                    return tag + item;
                });
                for (l = 0, len1 = ref1.length; l < len1; l++) {
                    item = ref1[l];
                    if (this.testUniqueness(element, item)) {
                        return item;
                    }
                }
            }
            return null;
        };

        CssSelectorGenerator.prototype.getUniqueSelector = function (element) {
            var found_selector, k, len, ref, selector_type, selectors;
            selectors = this.getAllSelectors(element);
            ref = this.options.selectors;
            for (k = 0, len = ref.length; k < len; k++) {
                selector_type = ref[k];
                switch (selector_type) {
                    case 'id':
                        if (selectors.i != null) {
                            return selectors.i;
                        }
                        break;
                    case 'tag':
                        if (selectors.t != null) {
                            if (this.testUniqueness(element, selectors.t)) {
                                return selectors.t;
                            }
                        }
                        break;
                    case 'class':
                        if ((selectors.c != null) && selectors.c.length !== 0) {
                            found_selector = this.testCombinations(element, selectors.c, selectors.t);
                            if (found_selector) {
                                return found_selector;
                            }
                        }
                        break;
                    case 'attribute':
                        if ((selectors.a != null) && selectors.a.length !== 0) {
                            found_selector = this.testCombinations(element, selectors.a, selectors.t);
                            if (found_selector) {
                                return found_selector;
                            }
                        }
                        break;
                    case 'nthchild':
                        if (selectors.n != null) {
                            return selectors.n;
                        }
                }
            }
            return '*';
        };

        CssSelectorGenerator.prototype.getSelector = function (element) {
            var all_selectors, item, k, l, len, len1, parents, result, selector, selectors;
            all_selectors = [];
            parents = this.getParents(element);
            for (k = 0, len = parents.length; k < len; k++) {
                item = parents[k];
                selector = this.getUniqueSelector(item);
                if (selector != null) {
                    all_selectors.push(selector);
                }
            }
            selectors = [];
            for (l = 0, len1 = all_selectors.length; l < len1; l++) {
                item = all_selectors[l];
                selectors.unshift(item);
                result = selectors.join(' > ');
                if (this.testSelector(element, result)) {
                    return result;
                }
            }
            return null;
        };

        CssSelectorGenerator.prototype.getCombinations = function (items) {
            var i, j, k, l, ref, ref1, result;
            if (items == null) {
                items = [];
            }
            result = [[]];
            for (i = k = 0, ref = items.length - 1; 0 <= ref ? k <= ref : k >= ref; i = 0 <= ref ? ++k : --k) {
                for (j = l = 0, ref1 = result.length - 1; 0 <= ref1 ? l <= ref1 : l >= ref1; j = 0 <= ref1 ? ++l : --l) {
                    result.push(result[j].concat(items[i]));
                }
            }
            result.shift();
            result = result.sort(function (a, b) {
                return a.length - b.length;
            });
            result = result.map(function (item) {
                return item.join('');
            });
            return result;
        };

        return CssSelectorGenerator;

    })();

    if (typeof define !== "undefined" && define !== null ? define.amd : void 0) {
        define([], function () {
            return CssSelectorGenerator;
        });
    } else {
        root = typeof exports !== "undefined" && exports !== null ? exports : this;
        root.CssSelectorGenerator = CssSelectorGenerator;
    }

}).call(this);

cssGenerator = new CssSelectorGenerator;

/* See license.txt for terms of usage */
"use strict";

// Constants
var Xpath = {};

Xpath.getElementXPath = function (element) {
    if (element && element.id)
        return '//*[@id="' + element.id + '"]';
    else
        return Xpath.getElementTreeXPath(element);
};

Xpath.getElementTreeXPath = function (element) {
    var paths = [];

    // Use nodeName (instead of localName) so namespace prefix is included (if any).
    for (; element && element.nodeType == Node.ELEMENT_NODE; element = element.parentNode) {
        var index = 0;
        var hasFollowingSiblings = false;
        for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {
            // Ignore document type declaration.
            if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
                continue;

            if (sibling.nodeName == element.nodeName)
                ++index;
        }

        for (var sibling = element.nextSibling; sibling && !hasFollowingSiblings; sibling = sibling.nextSibling) {
            if (sibling.nodeName == element.nodeName)
                hasFollowingSiblings = true;
        }

        var tagName = (element.prefix ? element.prefix + ":" : "") + element.localName;
        var pathIndex = (index || hasFollowingSiblings ? "[" + (index + 1) + "]" : "");
        paths.splice(0, 0, tagName + pathIndex);
    }

    return paths.length ? "/" + paths.join("/") : null;
};

Xpath.cssToXPath = function (rule) {
    var regElement = /^([#.]?)([a-z0-9\\*_-]*)((\|)([a-z0-9\\*_-]*))?/i;
    var regAttr1 = /^\[([^\]]*)\]/i;
    var regAttr2 = /^\[\s*([^~=\s]+)\s*(~?=)\s*"([^"]+)"\s*\]/i;
    var regPseudo = /^:([a-z_-])+/i;
    var regCombinator = /^(\s*[>+\s])?/i;
    var regComma = /^\s*,/i;

    var index = 1;
    var parts = ["//", "*"];
    var lastRule = null;

    while (rule.length && rule != lastRule) {
        lastRule = rule;

        // Trim leading whitespace
        rule = Str.trim(rule);
        if (!rule.length)
            break;

        // Match the element identifier
        var m = regElement.exec(rule);
        if (m) {
            if (!m[1]) {
                // XXXjoe Namespace ignored for now
                if (m[5])
                    parts[index] = m[5];
                else
                    parts[index] = m[2];
            } else if (m[1] == '#')
                parts.push("[@id='" + m[2] + "']");
            else if (m[1] == '.')
                parts.push("[contains(concat(' ',normalize-space(@class),' '), ' " + m[2] + " ')]");

            rule = rule.substr(m[0].length);
        }

        // Match attribute selectors
        m = regAttr2.exec(rule);
        if (m) {
            if (m[2] == "~=")
                parts.push("[contains(@" + m[1] + ", '" + m[3] + "')]");
            else
                parts.push("[@" + m[1] + "='" + m[3] + "']");

            rule = rule.substr(m[0].length);
        } else {
            m = regAttr1.exec(rule);
            if (m) {
                parts.push("[@" + m[1] + "]");
                rule = rule.substr(m[0].length);
            }
        }

        // Skip over pseudo-classes and pseudo-elements, which are of no use to us
        m = regPseudo.exec(rule);
        while (m) {
            rule = rule.substr(m[0].length);
            m = regPseudo.exec(rule);
        }

        // Match combinators
        m = regCombinator.exec(rule);
        if (m && m[0].length) {
            if (m[0].indexOf(">") != -1)
                parts.push("/");
            else if (m[0].indexOf("+") != -1)
                parts.push("/following-sibling::");
            else
                parts.push("//");

            index = parts.length;
            parts.push("*");
            rule = rule.substr(m[0].length);
        }

        m = regComma.exec(rule);
        if (m) {
            parts.push(" | ", "//", "*");
            index = parts.length - 1;
            rule = rule.substr(m[0].length);
        }
    }

    var xpath = parts.join("");
    return xpath;
};

Xpath.getElementsBySelector = function (doc, css) {
    var xpath = Xpath.cssToXPath(css);
    return Xpath.getElementsByXPath(doc, xpath);
};

Xpath.getElementsByXPath = function (doc, xpath) {
    try {
        return Xpath.evaluateXPath(doc, xpath);
    } catch (ex) {
        return [];
    }
};

/**
 * Evaluates an XPath expression.
 *
 * @param {Document} doc
 * @param {String} xpath The XPath expression.
 * @param {Node} contextNode The context node.
 * @param {int} resultType
 *
 * @returns {*} The result of the XPath expression, depending on resultType :<br> <ul>
 *          <li>if it is XPathResult.NUMBER_TYPE, then it returns a Number</li>
 *          <li>if it is XPathResult.STRING_TYPE, then it returns a String</li>
 *          <li>if it is XPathResult.BOOLEAN_TYPE, then it returns a boolean</li>
 *          <li>if it is XPathResult.UNORDERED_NODE_ITERATOR_TYPE
 *              or XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, then it returns an array of nodes</li>
 *          <li>if it is XPathResult.ORDERED_NODE_SNAPSHOT_TYPE
 *              or XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, then it returns an array of nodes</li>
 *          <li>if it is XPathResult.ANY_UNORDERED_NODE_TYPE
 *              or XPathResult.FIRST_ORDERED_NODE_TYPE, then it returns a single node</li>
 *          </ul>
 */
Xpath.evaluateXPath = function (doc, xpath, contextNode, resultType) {
    if (contextNode === undefined)
        contextNode = doc;

    if (resultType === undefined)
        resultType = XPathResult.ANY_TYPE;

    var result = doc.evaluate(xpath, contextNode, null, resultType, null);

    switch (result.resultType) {
        case XPathResult.NUMBER_TYPE:
            return result.numberValue;

        case XPathResult.STRING_TYPE:
            return result.stringValue;

        case XPathResult.BOOLEAN_TYPE:
            return result.booleanValue;

        case XPathResult.UNORDERED_NODE_ITERATOR_TYPE:
        case XPathResult.ORDERED_NODE_ITERATOR_TYPE:
            var nodes = [];
            for (var item = result.iterateNext(); item; item = result.iterateNext())
                nodes.push(item);
            return nodes;

        case XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE:
        case XPathResult.ORDERED_NODE_SNAPSHOT_TYPE:
            var nodes = [];
            for (var i = 0; i < result.snapshotLength; ++i)
                nodes.push(result.snapshotItem(i));
            return nodes;

        case XPathResult.ANY_UNORDERED_NODE_TYPE:
        case XPathResult.FIRST_ORDERED_NODE_TYPE:
            return result.singleNodeValue;
    }
};

Xpath.getRuleMatchingElements = function (rule, doc) {
    var css = rule.selectorText;
    var xpath = Xpath.cssToXPath(css);
    return Xpath.getElementsByXPath(doc, xpath);
};

var xpathGenerator = Xpath;


function getXPathByElement(element) {
    return xpathGenerator.getElementXPath(element);
}


function getCSSSelectorByElement(element) {
    return jQuery(element).getPath();
}

function getElementsByXPath(XPath) {
    var xresult = document.evaluate(XPath, document, null, XPathResult.ANY_TYPE, null)
    var xnodes = [];
    var xres;
    while (xres = xresult.iterateNext()) {
        xnodes.push(xres);
    }
    return xnodes;
}

function getElementsByCSSSelector(CSSSelector) {
    return document.querySelectorAll(CSSSelector);
}


function reverse(s) {
    return s.split("").reverse().join("");
}

function commonSubstring(string1, string2) {
    let forward = '';
    let length1 = string1.length;

    for (let i = 0; i < length1; i++) {
        if (string1[i] === string2[i]) {
            forward += string1[i];
        } else {
            break;
        }
    }

    string1 = reverse(string1);
    string2 = reverse(string2);

    let backward = '';
    length1 = string1.length;

    for (let i = 0; i < length1; i++) {
        if (string1[i] === string2[i]) {
            backward += string1[i];
        } else {
            break;
        }
    }
    return forward + reverse(backward);
}

function exists(array, target) {
    var length = array.length;
    for (var i = 0; i < length; i++) {
        element = array[i];
        if ($(element).is($(target))) {
            console.log('IS', $(element).is($(target)));
            return i;
        }
    }
    return -1;
}

function removeStyle(element) {
    $(element).removeClass('gerapy-chosen')
}

function addStyle(element) {
    $(element).addClass('gerapy-chosen')
}