export default {
  timeout: null,
  intervals: [],
  lang: 'en',
}
function onLoad() {
  if (typeof(Storage) !== 'undefined' && localStorage.getItem('gerapy-lang') !== 'undefined') {
    return localStorage.getItem('gerapy-lang');
  } else {
    return 'en'
  }
}
