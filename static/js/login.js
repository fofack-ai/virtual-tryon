const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
  container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
  container.classList.remove("active");
});

document.addEventListener('DOMContentLoaded', function () {
  const signInForm = document.querySelector('.sign-in form');
  const validUsername = "exampleUser@gmail.com";
  const validPassword = "examplePassword";
  const redirectUrl = "/homw";

  signInForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const email = signInForm.querySelector('input[type="email"]').value;
    const password = signInForm.querySelector('input[type="password"]').value;

    if (email === validUsername && password === validPassword) {
      alert('Login successful!');
      window.location.href = redirectUrl;
    } else {
      alert('Invalid username or password. Please try again.');
    }
  });
});
