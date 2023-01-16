
let accueuil = document.getElementById("accueuil");
let ProfesseurId = document.getElementById("Professeur");

function Etudiant(){
    alert(123);
    download();
}

function Professeur(){
    accueuil.style.display = "none";
    ProfesseurId.style.display = "flex";
}

function Accueuil(){
    accueuil.style.display = "flex";
    ProfesseurId.style.display = "none";
}


function download(){
const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(obj, null, 2)], {
    type: "application/json"
  }));
  a.setAttribute("download", "data.json");
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}



let obj;



function onChange(event) {
    var reader = new FileReader();
    reader.onload = onReaderLoad;
    reader.readAsText(event.target.files[0]);
}
 
document.getElementById('file').addEventListener('change', onChange);

const dropArea = document.getElementById("drop-area");

dropArea.addEventListener("dragover", (event)=>{
    event.preventDefault();
    dropArea.style.backgroundColor = "red";
  });

dropArea.addEventListener("dragleave", ()=>{
    dropArea.style.backgroundColor = "white";
});

dropArea.addEventListener("drop", (event)=>{
    event.preventDefault();
    let file = event.dataTransfer.files[0];
    let fileType = file.type;
    let validExtensions = ["application/json"];

    if(validExtensions.includes(fileType)){
        let fileReader = new FileReader(); 
        fileReader.onload = onReaderLoad;
        fileReader.readAsText(file);
    }
    else{
      alert("This is not a good format");
    }
  });
  function onReaderLoad(event){
    console.log(event.target.result);
    obj = JSON.parse(event.target.result);
    dropArea.style.backgroundColor = "white";
}