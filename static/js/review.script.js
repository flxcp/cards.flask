var cardPosn = 0;

const questions = document.getElementsByClassName("question");

const answers = document.getElementsByClassName("answer");

const reviewCard = document.getElementsByClassName("reviewCard");

const reviewCards = document.querySelector(".reviewCards");

const reviewCardsFinished = document.querySelector(".reviewCardsFinished");

const buttonChoose = document.getElementsByClassName("buttonChoose");

const buttonAnswer = document.querySelector(".buttonAnswer");
buttonAnswer.addEventListener("click", showAnswer);

const buttonChooseEasy = document.querySelectorAll(".buttonChooseEasy");
buttonChooseEasy.forEach((button) => {
  button.addEventListener("click", sendResponse);
});
const buttonChooseMedium = document.querySelectorAll(".buttonChooseMedium");
buttonChooseMedium.forEach((button) => {
  button.addEventListener("click", sendResponse);
});
const buttonChooseHard = document.querySelectorAll(".buttonChooseHard");
buttonChooseHard.forEach((button) => {
  button.addEventListener("click", sendResponse);
});

// Function for Creating New Deck
function showAnswer(event) {
  event.preventDefault();

  if (cardPosn < reviewCard.length) {
    answers[cardPosn].classList.toggle("hidden");
    buttonAnswer.classList.toggle("hidden");
    buttonChoose[cardPosn].classList.toggle("hidden");
  }
}

// Function for Creating New Deck
function sendResponse(event) {
  event.preventDefault();

  if (cardPosn < reviewCard.length - 1) {
    reviewCard[cardPosn].classList.toggle("hidden");
    buttonChoose[cardPosn].classList.toggle("hidden");

    cardPosn++;
    reviewCard[cardPosn].classList.toggle("hidden");

    buttonAnswer.classList.toggle("hidden");
    // buttonChoose[cardPosn].classList.toggle("hidden");

    var currentCard = parseInt(
      document.querySelector(".currentCard").innerText
    );
    currentCard++;
    document.querySelector(".currentCard").innerText = currentCard;
  } else {
    reviewCards.classList.toggle("hidden");
    reviewCards.classList.toggle("d-flex");
    reviewCardsFinished.classList.toggle("d-flex");
    reviewCardsFinished.classList.toggle("hidden");
  }

  const url = event.target.href;
  console.log(url);

  try {
    const fetchOptions = {
      method: "PUT",
    };

    fetch(url, fetchOptions)
      .then((response) => response.json())
      .then((data) => console.log(data));
  } catch (error) {
    console.error(error);
  }
}
