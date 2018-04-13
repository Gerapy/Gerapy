export default {
  timeout: null,
  intervals: [],
  lang:onLoad(),
}
function onLoad (){
  if (typeof(Storage) !== "undefined" && localStorage .getItem("gerapy-lang")  !== "undefined") {
    return localStorage.getItem("gerapy-lang");
  } else {
    return 'en'
  }
}
