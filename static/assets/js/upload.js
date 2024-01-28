var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next >>";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}


// get input fields value to another input value

window.onload = function() {
  var src = document.getElementById("title");
  var dst = document.getElementById("title2");

  src.addEventListener('input', function() {
    dst.value = src.value;
  });

  var slc = document.getElementById("jbcategory");
  var slc2 = document.getElementById("jbcategory2");

  slc.addEventListener('change', function() {
    slc2.selectedIndex = slc.selectedIndex;
  });

  var txt1 = document.getElementById("desc");
  var txt2 = document.getElementById("desc2");

  txt1.addEventListener('input', function() {
    txt2.value = txt1.value;
  });

  var prj = document.getElementById("projectlength");
  var prj2 = document.getElementById("projectlength2");

  prj.addEventListener('change', function() {
    prj2.selectedIndex = prj.selectedIndex;
  });

  var payop = document.getElementById("payoption");
  var payop2 = document.getElementById("payoption2");

  payop.addEventListener('change', function() {
    payop2.selectedIndex = payop.selectedIndex;
  });

  var amount = document.getElementById("amount");
  var amount2 = document.getElementById("amount2");

  amount.addEventListener('input', function() {
    amount2.value = amount.value;
  });

  var prjtype = document.getElementById("projecttype");
  var prjtype2 = document.getElementById("projecttype2");

  prjtype.addEventListener('change', function() {
    prjtype2.selectedIndex = prjtype.selectedIndex;
  });

  var explvl = document.getElementById("expertiselevel");
  var explvl2 = document.getElementById("expertiselevel2");

  explvl.addEventListener('change', function() {
    explvl2.selectedIndex = explvl.selectedIndex;
  });

  var skill = document.getElementById("skills");
  var skill2 = document.getElementById("skills2");

  skill.addEventListener('input', function() {
    skill2.value = skill.value;
  });
}