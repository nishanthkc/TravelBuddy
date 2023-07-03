// const charField = document.getElementById('place_id');
// const intField = document.getElementById('duration_id');
// const submitButton = document.getElementById('submit_button');

// submitButton.disabled = true;

// charField.addEventListener('input', () => {
//   if (charField.checkValidity() && intField.checkValidity()) {
//     submitButton.disabled = false;
//   } else {
//     submitButton.disabled = true;
//   }
// });

// intField.addEventListener('input', () => {
//   if (charField.checkValidity() && intField.checkValidity()) {
//     submitButton.disabled = false;
//   } else {
//     submitButton.disabled = true;
//   }
// });



const charField = document.getElementById('place_id');
const intField = document.getElementById('duration_id');
const submitButton = document.getElementById('submit_button');
const errorMessage = document.getElementById('error_message');

submitButton.disabled = true;

charField.addEventListener('input', () => {
  if (charField.checkValidity() && intField.checkValidity() && intField.value <= 10) {
    submitButton.disabled = false;
    errorMessage.textContent = '';
  } else {
    submitButton.disabled = true;
    if (intField.value > 10) {
      errorMessage.textContent = 'Currently, we can only build itineraries for less than 10-days';
    } else {
      errorMessage.textContent = '';
    }
  }
});

intField.addEventListener('input', () => {
  if (charField.checkValidity() && intField.checkValidity() && intField.value <= 10) {
    submitButton.disabled = false;
    errorMessage.textContent = '';
  } else {
    submitButton.disabled = true;
    if (intField.value > 10) {
      errorMessage.textContent = 'Currently, we can only build itineraries for less than 10-days';
    } else {
      errorMessage.textContent = '';
    }
  }
});



// function MakeVisible() {
//     var text = document.getElementById("make-visible");
//     text.innerHTML = "Building Itinerary... may take upto 20sec";
    
//   }

function typeWriter(text, i, fnCallback) {
    if (i < text.length) {
      document.getElementById("make-visible").innerHTML += text.charAt(i);
      i++;
      setTimeout(function() {
        typeWriter(text, i, fnCallback)
      }, 100);
    } else if (typeof fnCallback == "function") {
      setTimeout(fnCallback, 700);
    }
  }
  
function startTyping() {
    var text = "Building Itinerary... may take upto 30sec";
    typeWriter(text, 0, function() {
      console.log("Text has been typed out!");
    });
    var submit_button = document.getElementById('submit_button');
    var get_itinerary = document.getElementById('get_itinerary_form');
    submit_button.disabled = true;
    get_itinerary.submit();
  }

function startFoodTyping() {
    var text = "Building Food Recommendation... may take upto 10sec";
    typeWriter(text, 0, function() {
      console.log("Text has been typed out!");
    });
    
    var submit_button = document.getElementById('submit_button');
    var get_food_rec = document.getElementById('get_food_rec_form');
    submit_button.disabled = true;
    get_food_rec.submit();
  }

function startWaiting() {
    var text = "Building a Personalized Itinerary just for you. Please be patient while we revolutionalize the way you travel with our AI-powered platform";
    typeWriter(text, 0, function() {
      console.log("Text has been typed out!");
    });
    
    var submit_button = document.getElementById('submit_button');
    var get_itinerary = document.getElementById('get_another_itinerary_form');
    submit_button.disabled = true;
    get_itinerary.submit();
  }




document.addEventListener('DOMContentLoaded', function() {
    var doableButton = document.getElementById('doable-button');
    doableButton.addEventListener('click', function() {
        doableButton.disabled = true;
        doableButton.innerText = 'Processing...';
        // Add your logic for the button action here
        // For example, you can make an AJAX request or submit a form
    });
});

