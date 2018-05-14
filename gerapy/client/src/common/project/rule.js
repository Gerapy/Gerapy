export const ruleItemOptions = [
  {
    value: 'callback',
    label: 'callback'
  }, {
    value: 'allow',
    label: 'allow'
  }, {
    value: 'deny',
    label: 'deny'
  }, {
    value: 'allow_domains',
    label: 'allow_domains'
  }, {
    value: 'deny_domains',
    label: 'deny_domains'
  }, {
    value: 'restrict_xpaths',
    label: 'restrict_xpaths'
  }, {
    value: 'restrict_css',
    label: 'restrict_css'
  }, {
    value: 'cb_kwargs',
    label: 'cb_kwargs'
  }, {
    value: 'follow',
    label: 'follow'
  }, {
    value: 'process_request',
    label: 'process_request'
  }, {
    value: 'process_links',
    label: 'process_links'
  }, {
    value: 'tags',
    label: 'tags'
  }, {
    value: 'attrs',
    label: 'attrs'
  }, {
    value: 'canonicalize',
    label: 'canonicalize'
  }, {
    value: 'unique',
    label: 'unique'
  }, {
    value: 'process_value',
    label: 'process_value'
  }, {
    value: 'strip',
    label: 'strip'
  },
];

export const ruleItemInit = {
  callback: '',
  allow: [],
  deny: [],
  allow_domains: [],
  deny_domains: [],
  deny_extensions: [],
  restrict_xpaths: [],
  restrict_css: [],
  tags: [],
  attrs: [],
  canonicalize: false,
  unique: false,
  strip: false,
  follow: false,
  process_value: '',
  process_links: '',
  process_request: '',
}
