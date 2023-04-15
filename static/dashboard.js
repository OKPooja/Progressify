'use strict';

async function submitForm() {
  let sleepInput = document.querySelector('[data-sleep]').value;
  let formData = new FormData();
  formData.append("sleep", sleepInput);

  try {
    const response = await fetch('/dashboard/', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });
    console.log(response);
    if (response.ok) {
      const data = await response.text();
      console.log(data);
    } else {
      console.error('Error:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

