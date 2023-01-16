function test() {
    alert("test");
}


function onChange(event) {
    var reader = new FileReader();
    reader.onload = onReaderLoad;
    reader.readAsText(event.target.files[0]);
}
function onReaderLoad(event){
    console.log(event.target.result);
    obj = JSON.parse(event.target.result);
}

document.getElementById('file').addEventListener('change', onChange);
