// JS is included in the  HTML because some variables weren't available when the user wasn't authenticated
// so I had to use {% if user.is_authenticated %} on the script and to do that I needed to have the JS code in the HTML


// // Get all the picture elements
// const buttons = document.querySelectorAll('[data-pk]');
// // Get the img element from the modal
// const pictureModal = document.querySelector('#pictureModal');
// // Get modal's footer
// const pictureTags = document.querySelector('#pictureTags');
// const imageInfo = document.querySelector('#imageInfo');
// const updateForm = document.querySelector('#updateForm');
// // Get elements from the modal form to add values
// const formCheck = document.querySelector('#formCheck');
// const formImageID = document.querySelector('#image_id');
// const formImageTitle = document.querySelector('#id_title');
// const formImageDescription = document.querySelector('#id_description');
// const formImageIsVisible = document.querySelector('#id_is_visible');


// buttons.forEach(button => {
//     button.addEventListener('click', () => {
//     // Get the id from the selected image
//       const picturePK = button.getAttribute('data-pk');

//     // Set the url from the server to request the picture by their id
//       const url = `/gallery/get-picture/${picturePK}/`;
//       console.log(picturePK)
//     // Fetch the image to the server
//       fetch(url, {
//         headers: {
//           'Accept': 'application/json',
//           'X-Requested-With': 'XMLHttpRequest',
//         },
//       })
//         .then(response => {
//           return response.json();
//         })
//         .then(data => {
//             // Add the image to the modal
//             pictureModal.setAttribute('src', data.url);
            
//             // Set modal form data with current image data 
//             formImageTitle.value = data.title;
//             formImageDescription.value = data.description;
//             // Add the picture id to the form to be sent to the server
//             formImageID.value = data.id;
//             formImageIsVisible.checked = data.is_visible
         
//             // Create checkbox to clear the picture tags
//             const checkbox = document.createElement('input');
//             const initialCheckedValue = false;
//             checkbox.type = 'checkbox';
//             checkbox.name = 'clear_hashtags';
//             checkbox.id = 'clear_hashtags';
//             checkbox.className = 'form-check-input';
//             checkbox.checked = initialCheckedValue;

//             // Create label for the checkbox
//             const label = document.createElement('label');
//             label.htmlFor = 'clear_hashtags';
//             label.classList.add("me-2");
//             label.textContent = 'Clear Tags:';

//             // Clear the modal check row and add the checkbox 
//             formCheck.innerHTML = "";
//             formCheck.appendChild(label)
//             formCheck.appendChild(checkbox)
      
//             // Add the data and tags of the current picture to the modal
//             pictureTags.innerHTML = ""
//             imageInfo.innerHTML = ""

//             for (let i = 0; i < data.hashtags.length; i++) {
//                 const hashtagSpan = document.createElement("span");
//                 hashtagSpan.classList.add("badge", "text-bg-secondary");
//                 hashtagSpan.innerText = data.hashtags[i];
//                 pictureTags.appendChild(hashtagSpan);
//               };
//             const imageDescription = document.createElement("p");
//             const imageDate = document.createElement("p");
//             imageDate.id = "upload-date";

//             const dateLabel = document.createElement('label');
//             dateLabel.htmlFor = 'upload-date';
//             dateLabel.classList.add("me-2");
//             dateLabel.textContent = 'Uploaded at:';

//             imageDescription.innerText = data.description;
//             imageDate.innerText = data.uploaded_at;

//             imageInfo.appendChild(imageDescription);
//             imageInfo.appendChild(dateLabel);
//             imageInfo.appendChild(imageDate);
//         });
//     });
//   });


//   const tagSearch = document.getElementsByClassName('tag-search')

//   Array.from(tagSearch).forEach( hashtagSelect => {
//     hashtagSelect.onchange = function() {
//       document.getElementById('hashtag-form').submit();
//     }
//     hashtagSelect.onfocus = function() {
//       this.value = ' ';
//     };
//   });

  

//   // Declare let for csrf token
//   let _csrfToken = null;

//   // Function to get new csrf token
//   function getCsrfToken() {
//     return new Promise((resolve, reject) => {
//       if (_csrfToken) {
//         resolve(_csrfToken);
//       } else {
//         fetch('/gallery/csrf/')
//           .then(response => response.json())
//           .then(data => {
//             _csrfToken = data.csrfToken;
//             resolve(_csrfToken);
//           })
//           .catch(error => {
//             console.error('Error fetching CSRF token:', error);
//             reject(error);
//           });
//       }
//     });
//   }
  
//   // Funtion to create new tag
//   function createHashtag() {
//     getCsrfToken()
//       .then(csrfToken => {
//         const hashtagElements = document.getElementsByClassName('new-hashtag');
        
//         Array.from(hashtagElements).forEach(hashtagInput => {
//           const hashtagValue = hashtagInput.value;  // Obtén el valor del input
//           console.log('Hashtag:', hashtagValue);
  
//           // Create fetch only if there is a value
//           if (hashtagValue) {
//             const url = '/gallery/create-hashtag/';
//             const form = {
//               hashtag: hashtagValue
//             };
  
//             fetch(url, {
//               method: 'POST',
//               headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrfToken,
//               },
//               body: JSON.stringify(form),
//             })
//             .then(response => response.json())
//             .then(data => {
//               console.log('Server Response:', data.hashtag);
//               const hashtagList = document.getElementsByClassName('form-select');
  
//               Array.from(hashtagList).forEach(list => {
//                 const newTag = document.createElement('option'); 
//                 newTag.innerText = data.hashtag;
//                 newTag.value = list.childElementCount + 1;
//                 list.appendChild(newTag);
//               });
//               // Reset the input from the other modal, so there will always be just one filled
//               Array.from(hashtagElements).forEach(input => {
//                 input.value = "";
//               });
              
//             })
//             .catch(error => {
//               console.error('Error sending form:', error);
//             });
//           }
//         });
//       })
//       .catch(error => {
//         console.error('Error getting CSRF token:', error);
//       });
//   }
  
//   // Get all the buttons to submit a new tag
//   const createHashtagButtons = document.getElementsByClassName('create-hashtag');
//   Array.from(createHashtagButtons).forEach(button => {
//     button.addEventListener('click', createHashtag);
//   });



//   const tagSelect = document.getElementsByClassName('tag-select');

//   Array.from(tagSelect).forEach(select => {
//       $(select).select2({
//           placeholder: 'Buscar hashtags',
//           width: '100%',
//       });
//   });

