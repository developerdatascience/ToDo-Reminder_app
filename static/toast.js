const signupForm = document.getElementById('signupForm');
const main = document.getElementById('main');

signupForm.addEventListener('submit', async (event) => {
    // Prevent default form submission
    event.preventDefault();

    // Collect form data
    const formData = new FormData(signupForm);
    const formObject = Object.fromEntries(formData.entries());

    try {
        // Send data to the server using fetch
        const response = await fetch(signupForm.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formObject),
        });

        if (response.ok) {
            // Notify success
            createNotification('User created successfully!', 'success');
            signupForm.reset(); // Optional: Clear the form
        } else {
            // Notify error
            const errorData = await response.json();
            createNotification(`Error: ${errorData.message}`, 'error');
        }
    } catch (error) {
        // Handle network or server errors
        createNotification(`Error: ${error.message}`, 'error');
    }
});

function createNotification(message, type) {
    const notif = document.createElement('div');
    notif.classList.add('toast', type); // Use type for styling (success or error)
    notif.innerText = message;
    main.appendChild(notif);

    // Remove the notification after 3 seconds
    setTimeout(() => {
        notif.remove();
    }, 3000);
}
