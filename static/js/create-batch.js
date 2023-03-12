console.log("hello12345")
let int = 1;
document.getElementById("addinputbtn").addEventListener("click", ()=>{
    let inputbox = document.getElementsByClassName("sunjectinputs")[0];
    int++;
    let input = document.createElement('input');
    input.setAttribute("class", "form-control");
    input.setAttribute("type", "text");
    input.setAttribute("id", int);
    input.setAttribute("placeholder", "Enter Subject Name");
    inputbox.appendChild(input);
});

document.getElementById("createbtn").addEventListener("click", ()=>{
    let batchName = document.getElementById("batchname").value;
    let subjectNames = [];
    let subjectbox = document.getElementsByClassName("sunjectinputs")[0];
    let slenstatus = 0;
    for(let count = 0; count<subjectbox.children.length; count++)
    {
        subjectNames[count] = subjectbox.children[count].value;
        if(subjectbox.children[count].value.length==0)
        {
            let slenstatus = 1; 
        }
    }
    console.log(subjectNames);
    let collegeStartT= document.getElementById("cStartT").value;
    let collegeEndT = document.getElementById("cEndT").value;
   

    if(batchName.length != 0 && slenstatus==0 && collegeStartT.length !=0 && collegeEndT.length !=0)
    {
    let data = JSON.stringify({
        data : {
            bName : batchName,
            bsubjects : subjectNames,
            CsT : collegeStartT,
            CeT : collegeEndT
        }
    })
    console.log("fdfdsf");

    let api = "/Admin/batchApi";
    fetch(api, {
        method: "POST",
        body: data,

        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })

        .then(response => response.json())

        .then(json => {
            if (json.code == 0) {
                alert(json.status);
                window.location.reload();
            }
            else{
                alert(json.status);
            }

        })
        .catch((e) => { 
            alert("Try Again");
            window.location.reload();
        });
    }
    else{
        alert("Please Fill All Fields");
    }
});
