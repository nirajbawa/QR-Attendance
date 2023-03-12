console.log("hello");

function signinbtncall() {
    setTimeout(() => {
        let getHomeF = document.getElementById("hfrom");
        document.getElementById("signinhtn").addEventListener("click", (event) => {
            if (document.getElementById("signinemail").value.match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            )) {
                let api = '/sign-in'
                let email = document.getElementById("signinemail").value;
                document.getElementById("hfrom").innerHTML = '<div class="loader"> <div class="spinner-border" role="status"> <span class="visually-hidden">Loading...</span></div> </div>';
                fetch(api, {

                    // Adding method type
                    method: "POST",

                    // Adding body or contents to send
                    body: JSON.stringify({
                        email: email
                    }),

                    // Adding headers to the request
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })

                    // Converting to JSON
                    .then(response => response.json())

                    // Displaying results to console
                    .then(json => {
                        if (json.code == 0) {
                            getHomeF.innerHTML = '<h1>sign in</h1> <div id="forminputfield"> <p style="font-size: 1.5rem;" id="siginmsg">Please Check Your Inbox And Enter OTP</p> <input class="form-control form-control-lg" type="text" id="signinotp" name = "signupotp" placeholder="OTP" autocomplete="off" aria-label=".form-control-lg example"><a onClick = "signin()" style= "font-size: 1.5rem;">Resend OTP</a></div> <button type="button" class="btn btn-primary" id="signinotpbtn"><i class="fa-solid fa-arrow-right"></i></button>';
                            event.target.innerText = "Sign in";
                            event.target.id = "Signinotpbtn";
                            signinotp();
                            document.getElementById("siginmsg").value = json.status;
                        }
                        else {
                            alert(json.status);
                            window.location.reload()
                        }
                    })
                    .catch((e) => { 
                        alert("Try Again") 
                        window.location.reload()
                    });
            }
            else {
                alert("Please Enter Vaild E-mail")
            }
        })
            

    }, 100);
}

function signinotp() {
    setTimeout(() => {
        document.getElementById("signinotpbtn").addEventListener("click", () => {
            let Iotp = document.getElementById("signinotp").value;
            if(Iotp.length != 0)
            {
                let api = window.location.href + "/sign-in-to-admin";
                fetch(api, {
                    method: "POST",
                    body: JSON.stringify({
                        otp: Iotp
                    }),
    
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
    
                    .then(response => response.json())
    
                    .then(json => {
                        if (json.code == 0) {
                            window.location = json.url;
                        }
                        else if(json.code == 2){
                            window.location.reload();
                        }
                        else{
                            document.getElementById("siginmsg").innerText = json.status;
                        }
    
                    })
                    .catch((e) => { 
                        alert("Try Again") 
                        window.location.reload()
                    });
            }
            else{
                document.getElementById("siginmsg").value = "Please Enter Valid OTP";
            }
        })
    }, 100)
}


function signupbtn() {
    setTimeout(() => {

        document.getElementById("signupbtn").addEventListener("click", () => {
            console.log("12345");
            if (document.getElementById("signupemail").value.match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            ) && document.getElementById("institutename").value.length != 0 && document.getElementById("institutetype").value.length != 0) {
                let email = document.getElementById("signupemail").value;
                let institutename = document.getElementById("institutename").value;
                let institutetype = document.getElementById("institutetype").value;
                document.getElementById("hfrom").innerHTML = '<div class="loader"> <div class="spinner-border" role="status"> <span class="visually-hidden">Loading...</span></div> </div>'
                let api = window.location.href + '/sign-up'
                fetch(api, {
                    method: "POST",
                    body: JSON.stringify({
                        email: email,
                        institutename: institutename,
                        institutetype: institutetype,
                    }),

                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })

                    .then(response => response.json())
                    .then(json => {
                        if (json.code == "0") {
                            document.getElementById("hfrom").innerHTML = '<h1>sign up</h1> <div id="forminputfield"> <p style="font-size: 1.5rem;" id="otpmsg">Please Check Your Inbox And Enter OTP</p> <input class="form-control form-control-lg" type="text" id="signupotp" name = "signupotp" placeholder="OTP" autocomplete="off" aria-label=".form-control-lg example"><a onClick = "signup()" style= "font-size: 1.5rem;">Resend OTP</a></div> <button type="button" class="btn btn-primary" id="createaccount"><i class="fa-solid fa-arrow-right"></i></button>';
                            createaccountotp();
                            document.getElementById("otpmsg").innerText = json.status;
                        }
                        else {
                            alert(json.status);
                            signup();
                        }
                        console.log(json)

                    })
                    .catch((e) => { 
                        alert("Try Again") 
                        window.location.reload()
                    });
            }
            else {
                alert("Please Enter Vaild Details")
            }
        });

    }, 100);
}

function createaccountotp() {
    document.getElementById("createaccount").addEventListener("click", () => {
        if (document.getElementById("signupotp").value.length) {
            let api = '/createAccout';
            fetch(api, {
                method: "POST",
                body: JSON.stringify({
                    signupotp: document.getElementById("signupotp").value
                }),

                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })

                .then(response => response.json())

                .then(json => {
                    if (json.code == 0) {
                        window.location = json.url
                    }
                    else {
                        document.getElementById("otpmsg").innerText = json.status;
                    }

                })
                .catch((e) => { 
                    alert("Try Again") 
                    window.location.reload()
                });

        }
        else {
            alert("Please Enter OTP");
        }
    })
}