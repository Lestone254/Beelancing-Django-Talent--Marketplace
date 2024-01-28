

// show password function on login page
function showpsw() {
    var x = document.getElementById("logpsw");
    if (x.type == "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

// constants declaration

const humburgerBtn = document.getElementById('humburgerMenu');
const sideBar = document.getElementById('side-bar');
const closeBtn = document.getElementById('closeBtn');

// constants declaration end here

// event listeners here
humburgerBtn.addEventListener('click', function() {
    sideBar.classList.add('left');
});

closeBtn.addEventListener('click', function() {
    sideBar.classList.remove('left');
});

// sidenav dropdown
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function () {
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}


// event listeners end here


// functions here

function validateForm(event) {
    let fname = document.forms["signUp"]["fname"].value;
    let fnameError = document.getElementById('fnameError');

    if (fname == "") {
        fnameError.classList.remove('d-none');
    }
}

// functions end here

// post job form script begins here
const firstStep = document.getElementById('firstStep');
const secondStep = document.getElementById('secondStep');
const lastStep = document.getElementById('lastStep');
const nextBtn1 = document.getElementById('nextBtn1');
const prevBtn1 = document.getElementById('prevBtn1');
const nextBtn2 = document.getElementById('nextBtn2');
const prevBtn2 = document.getElementById('prevBtn2');

nextBtn1.addEventListener('click', ()=> {
    if (firstStep.classList.contains('d-block')) {
        firstStep.classList.remove('d-block');
        firstStep.classList.add('d-none');
        secondStep.classList.remove('d-none');
        secondStep.classList.add('d-block');
    }
    else if (firstStep.classList.contains('d-none')) {
        firstStep.classList.remove('d-none');
        firstStep.classList.add('d-block');
        secondStep.classList.remove('d-block');
        secondStep.classList.add('d-none');
    }
});

prevBtn1.addEventListener('click', ()=> {
    if (secondStep.classList.contains('d-block')) {
        secondStep.classList.remove('d-block');
        secondStep.classList.add('d-none');
        firstStep.classList.remove('d-none');
        firstStep.classList.add('d-block');
    }
    else if (secondStep.classList.contains('d-none')) {
        secondStep.classList.remove('d-none');
        secondStep.classList.add('d-block');
        firstStep.classList.remove('d-block');
        firstStep.classList.add('d-none');
    }
});

nextBtn2.addEventListener('click', ()=> {
    if(lastStep.classList.contains('d-none')) {
        lastStep.classList.remove('d-none');
        lastStep.classList.add('d-block');
        secondStep.classList.remove('d-block');
        secondStep.classList.add('d-none');
    }
    else if(lastStep.classList.contains('d-block')) {
        lastStep.classList.remove('d-block');
        lastStep.classList.add('d-none');
        secondStep.classList.remove('d-none');
        secondStep.classList.add('d-block');
    }
});

prevBtn2.addEventListener('click', ()=> {
    if(lastStep.classList.contains('d-block')) {
        lastStep.classList.remove('d-block');
        lastStep.classList.add('d-none');
        secondStep.classList.remove('d-none');
        secondStep.classList.add('d-block');
    }
});
// post job script ends here
