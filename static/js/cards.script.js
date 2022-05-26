// Declare Submit Listner for Creating New Deck
const newCard = document.getElementById("new-card");
newCard.addEventListener("submit", createnewCard);

// Declare Submit Listner for Editing Existing Deck
const editCard = document.querySelectorAll("#edit-card");
editCard.forEach((card) => {
  card.addEventListener("submit", editExistCard);
});

// Declare Submit Listner for Deleting Existing Deck
const delCard = document.querySelectorAll("#delete-card");
delCard.forEach((card) => {
  card.addEventListener("click", deleteCard);
});

// Function for Creating New Deck
function createnewCard(event) {
  event.preventDefault();

  const form = event.currentTarget;
  const url = form.action;

  try {
    const formData = new FormData(form);
    const plainFormData = Object.fromEntries(formData.entries());
    const formDataJsonString = JSON.stringify(plainFormData);

    const fetchOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: formDataJsonString,
    };

    fetch(url, fetchOptions)
      .then((response) => response.json())
      .then((data) => console.log(data))
      .then(() => window.location.reload())
      .then(() => form.reset());
  } catch (error) {
    console.error(error);
  }
}

// Function for Editing Existing Deck
function editExistCard(event) {
  event.preventDefault();

  const form = event.currentTarget;
  const url = form.action;

  try {
    const formData = new FormData(form);
    const plainFormData = Object.fromEntries(formData.entries());
    const formDataJsonString = JSON.stringify(plainFormData);

    const fetchOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: formDataJsonString,
    };

    fetch(url, fetchOptions)
      .then((response) => response.json())
      .then((data) => console.log(data))
      .then(() => window.location.reload());
  } catch (error) {
    console.error(error);
  }
}

// Function for Deleting Existing Deck
function deleteCard(event) {
  event.preventDefault();

  const url = event.target.href;

  try {
    const fetchOptions = {
      method: "DELETE",
    };

    fetch(url, fetchOptions).then(() => window.location.reload());
  } catch (error) {
    console.error(error);
  }
}
