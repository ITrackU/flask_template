// Form handling functionality with encryption
class FormHandler {
    constructor() {
        this.encryptionHandler = new EncryptionHandler();
        this.initializeForm();
    }

    initializeForm() {
        const form = document.getElementById('registerForm');
        if (form) {
            form.addEventListener('submit', this.handleRegistration.bind(this));
        }
    }

    async handleRegistration(event) {
        event.preventDefault();

        const form = event.target;
        const username = form.username.value;
        const email = form.email.value;
        const password = form.password.value;
        const confirmPassword = form.confirm_password.value;

        if (!this.validatePasswords(password, confirmPassword)) {
            alert('Passwords do not match!');
            return;
        }

        try {
            await this.processRegistration(username, email, password, form.csrf_token.value);
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed. Please try again.');
        }
    }

    validatePasswords(password, confirmPassword) {
        return password === confirmPassword;
    }

    async processRegistration(username, email, password, csrfToken) {
        // Generate encryption key
        const key = await this.encryptionHandler.generateKey();
        
        // Show key backup interface
        this.showKeyBackup(key);
        
        // Store the key locally
        await this.encryptionHandler.storeKey(username, key);

        // Encrypt sensitive data before sending
        const sensitiveData = {
            email: email,
            password: password
        };

        // Encrypt the sensitive data
        const encryptedData = await this.encryptionHandler.encryptData(sensitiveData, username);
        
        // Prepare the registration payload
        const registrationData = {
            username: username, // Username sent in clear as it's needed for key identification
            encryptedData: encryptedData.encrypted,
            iv: encryptedData.iv
        };

        // Send encrypted registration data to server
        const response = await this.sendRegistrationData(registrationData, csrfToken);
        
        if (response.ok) {
            window.location.href = '/home';
        } else {
            const errorData = await response.json();
            alert(errorData.error || 'Registration failed');
        }
    }

    async sendRegistrationData(registrationData, csrfToken) {
        return fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(registrationData)
        });
    }

    showKeyBackup(key) {
        const keyBackup = document.getElementById('keyBackup');
        const encryptionKey = document.getElementById('encryptionKey');
        
        keyBackup.classList.remove('hidden');
        encryptionKey.textContent = key;

        // Add event listener for the acknowledge button
        const acknowledgeButton = keyBackup.querySelector('button');
        if (acknowledgeButton) {
            acknowledgeButton.onclick = () => this.acknowledgeKey();
        }
    }

    acknowledgeKey() {
        document.getElementById('keyBackup').classList.add('hidden');
    }
}

// Initialize form handler when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FormHandler();
});