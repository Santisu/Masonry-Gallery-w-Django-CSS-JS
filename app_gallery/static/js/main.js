// Get all the picture elements
const buttons = document.querySelectorAll('[data-pk]');
// Get the img element from the modal
const pictureModal = document.querySelector('#pictureModal');
// Get modal's footer
const pictureTags = document.querySelector('#pictureTags');
const imageInfo = document.querySelector('#imageInfo');
const updateForm = document.querySelector('#updateForm');
// Get elements from the modal form to add values
const formCheck = document.querySelector('#formCheck');
const formImageID = document.querySelector('#image_id');
const formImageTitle = document.querySelector('#id_title');
const formImageDescription = document.querySelector('#id_description');
const formImageIsVisible = document.querySelector('#id_is_visible');


buttons.forEach(button => {
    button.addEventListener('click', () => {
    // Get the id from the selected image
      const picturePK = button.getAttribute('data-pk');

    // Set the url from the server to request the picture by their id
      const url = `/gallery/get-picture/${picturePK}/`;

    // Fetch the image to the server
      fetch(url, {
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
        .then(response => {
          return response.json();
        })
        .then(data => {
            // Add the image to the modal
            pictureModal.setAttribute('src', data.url);
            
            // Set modal form data with current image data 
            formImageTitle.value = data.title;
            formImageDescription.value = data.description;
            // Add the picture id to the form to be sent to the server
            formImageID.value = data.id;
            formImageIsVisible.value = data.is_visible
         
            // Create checkbox to clear the picture tags
            const checkbox = document.createElement('input');
            const initialCheckedValue = false;
            checkbox.type = 'checkbox';
            checkbox.name = 'clear_hashtags';
            checkbox.id = 'clear_hashtags';
            checkbox.className = 'form-check-input';
            checkbox.checked = initialCheckedValue;

            // Create label for the checkbox
            const label = document.createElement('label');
            label.htmlFor = 'clear_hashtags';
            label.classList.add("me-2");
            label.textContent = 'Clear Tags:';

            // Clear the modal check row and add the checkbox 
            formCheck.innerHTML = "";
            formCheck.appendChild(label)
            formCheck.appendChild(checkbox)
      
            // Add the data and tags of the current picture to the modal
            pictureTags.innerHTML = ""
            imageInfo.innerHTML = ""

            for (let i = 0; i < data.hashtags.length; i++) {
                const hashtagSpan = document.createElement("span");
                hashtagSpan.classList.add("badge", "text-bg-secondary");
                hashtagSpan.innerText = data.hashtags[i];
                pictureTags.appendChild(hashtagSpan);
              };
            const imageDescription = document.createElement("p");
            const imageDate = document.createElement("p");
            imageDate.id = "upload-date";
            const dateLabel = document.createElement('label');
            dateLabel.htmlFor = 'upload-date';
            dateLabel.classList.add("me-2");
            dateLabel.textContent = 'Uploaded at:';
            imageDescription.innerText = data.description;
            imageDate.innerText = data.uploaded_at;

            imageInfo.appendChild(imageDescription);
            imageInfo.appendChild(dateLabel);
            imageInfo.appendChild(imageDate);
        });
    });
  });