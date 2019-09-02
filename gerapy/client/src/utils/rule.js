export const ruleItemOptions = [
	// in scrapy link extractors
	{
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
		value: 'deny_extensions',
		label: 'deny_extensions'
	}, {
		value: 'restrict_xpaths',
		label: 'restrict_xpaths'
	}, {
		value: 'restrict_css',
		label: 'restrict_css'
	}, {
		value: 'restrict_text',
		label: 'restrict_text'
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
		value: 'strip',
		label: 'strip'
	}, {
		value: 'process_value',
		label: 'process_value'
	},
	// scrapy rules
	{
		value: 'process_links',
		label: 'process_links'
	}, {
		value: 'process_request',
		label: 'process_request'
	}, {
		value: 'follow',
		label: 'follow'
	}, {
		value: 'cb_kwargs',
		label: 'cb_kwargs'
	}, {
		value: 'meta',
		label: 'meta'
	}, {
		value: 'callback',
		label: 'callback'
	},
	// gerapy rules
	{
		value: 'method',
		label: 'method'
	}, {
		value: 'data',
		label: 'data'
	}, {
		value: 'params',
		label: 'params'
	}, {
		value: 'priority',
		label: 'priority'
	}, {
		value: 'dont_filter',
		label: 'dont_filter'
	}, {
		value: 'proxy',
		label: 'proxy'
	}, {
		value: 'render',
		label: 'render'
	}, {
		value: 'dont_redirect',
		label: 'dont_redirect'
	}, {
		value: 'dont_retry',
		label: 'dont_retry'
	}, {
		value: 'handle_httpstatus_list',
		label: 'handle_httpstatus_list'
	}, {
		value: 'handle_httpstatus_all',
		label: 'handle_httpstatus_all'
	}, {
		value: 'dont_cache',
		label: 'dont_cache'
	}, {
		value: 'dont_obey_robotstxt',
		label: 'dont_obey_robotstxt'
	}, {
		value: 'download_timeout',
		label: 'download_timeout'
	}, {
		value: 'max_retry_times',
		label: 'max_retry_times'
	},
	{
		value: 'process_body',
		label: 'process_body'
	},
]

export const ruleItemInit = {
	allow: [],
	deny: [],
	allow_domains: [],
	deny_domains: [],
	deny_extensions: [],
	restrict_xpaths: [],
	restrict_css: [],
	restrict_text: [],
	follow: false,
	callback: 'parse',
	method: 'GET',
	data: null,
	params: null,
	priority: null,
	dont_filter: false,
	meta: null,
	cb_kwargs: null,
	proxy: null,
	render: false,
	dont_redirect: false,
	dont_retry: false,
	handle_httpstatus_list: [],
	handle_httpstatus_all: false,
	dont_cache: false,
	dont_obey_robotstxt: false,
	download_timeout: null,
	max_retry_times: null,
	tags: [],
	attrs: [],
	canonicalize: false,
	unique: false,
	strip: false,
	process_value: null,
	process_links: null,
	process_request: null,
	process_body: null,
}
