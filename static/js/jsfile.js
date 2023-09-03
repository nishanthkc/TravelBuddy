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
  if (charField.checkValidity()) {
    submitButton.disabled = false;
    errorMessage.textContent = '';
  } else {
    submitButton.disabled = true;
    errorMessage.textContent = 'Hey Buddy, we can only build itineraries for less than 10-days';
  }
});

intField.addEventListener('input', () => {
  if (intField.checkValidity() && intField.value <= 10 && intField.value > 0) {
    submitButton.disabled = false;
    errorMessage.textContent = '';
  } else {
    submitButton.disabled = true;
    if (intField.value > 10) {
      errorMessage.textContent = 'Hey Buddy, we can only build itineraries for less than 10-days';
    }
    else if (intField.value < 1){
      errorMessage.textContent = 'Hey Buddy, please provide a valid duration';
    }
    else {
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




// COPY TO CLIPBOARD



function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
  .then(() => {
  Swal.fire({
  title: 'Link copied to clipboard',
  icon: 'success',
  timer: 1500
  });
  })
  .catch((error) => console.log(error));
}


function popup() {  
  var modal = new bootstrap.Modal(document.getElementById("staticBackdrop"));
  modal.show();
}
function food_popup() {  
  var modal = new bootstrap.Modal(document.getElementById("foodModal"));
  modal.show();
}

function test() {
  // Replace this with your actual logic
  alert('Getting food recommendations for ');
  // You can also perform AJAX requests or other actions here
}