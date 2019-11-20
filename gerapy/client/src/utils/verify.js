import {phone} from './regex'

exports.isUrl = url => {
	return (/(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/i).test(url)
}

exports.isTel = tel => {
	return (phone).test(tel)
}

exports.isObject = o => {
	return !!value && Object.prototype.toString.call(o) === '[object Object]';
}

exports.isArray = o => {
	return Object.prototype.toString.call(o) === '[object Array]';
}
