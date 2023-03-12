// window.onscroll = function() {myFunction()};

// // Get the header
// var header = document.getElementById("myHeader");

// // Get the offset position of the navbar
// var sticky = header.offsetTop;

// // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction() {
//   if (window.pageYOffset > sticky) {
//     header.classList.add("sticky");
//   } else {
//     header.classList.remove("sticky");
//   }
// }


console.log("yes");

// let getHomeF = document.getElementById("hfrom");
let getHomeForm = document.getElementById("hfrom");
let getmenuul = document.getElementById("menuul");

getmenuul.children[0].addEventListener("click", signin = () =>{
  getmenuul.children[1].children[0].setAttribute("class", "nav-link")
  getmenuul.children[0].children[0].setAttribute("class", "nav-link active")
  getHomeForm.innerHTML = '<h1>sign in</h1> <div id="forminputfield"> <input class="form-control form-control-lg" type="email" id="signinemail" name = "email" placeholder="E-mail" aria-label=".form-control-lg example"> </div> <button type="button" class="btn btn-primary" id="signinhtn"><i class="fa-solid fa-arrow-right"></i></button>';
  signinbtncall();
});

signin();


getmenuul.children[1].addEventListener("click", signup = () =>{
  getmenuul.children[0].children[0].setAttribute("class", "nav-link")
  getmenuul.children[1].children[0].setAttribute("class", "nav-link active")
  getHomeForm.innerHTML =  '<h1>sign up</h1> <div id="forminputfield"> <input class="form-control form-control-lg" type="text" id="institutename" name = "institutename" placeholder="institute name" aria-label=".form-control-lg example"> <input class="form-control form-control-lg" type="email" id="signupemail" name = "signupemail" placeholder="E-mail" aria-label=".form-control-lg example"> <input class="form-control form-control-lg" type="text" id="institutetype" name = "institutetype" placeholder="institute type" aria-label=".form-control-lg example">  </div> <button type="button" class="btn btn-primary" id="signupbtn"><i class="fa-solid fa-arrow-right"></i></button>';
  signupbtn();
});
