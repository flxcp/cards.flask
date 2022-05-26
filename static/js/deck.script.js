// Declare Submit Listner for Creating New Deck
const newDeck = document.getElementById("new-deck");
newDeck.addEventListener("submit", createNewDeck);

// Declare Submit Listner for Editing Existing Deck
const editDeck = document.querySelectorAll("#edit-deck");
editDeck.forEach((deck) => {
  deck.addEventListener("submit", editExistDeck);
});

// Declare Submit Listner for Deleting Existing Deck
const delDeck = document.querySelectorAll("#delete-deck");
delDeck.forEach((deck) => {
  deck.addEventListener("click", deleteDeck);
});

// Function for Creating New Deck
function createNewDeck(event) {
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
function editExistDeck(event) {
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
function deleteDeck(event) {
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
