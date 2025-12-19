const Auth = {
    init() {
        this.setupSignupForm();
        this.setupLoginForm();
    },

    setupSignupForm() {
        const form = document.getElementById('signupForm');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSignup(e.target);
        });
    },

    setupLoginForm() {
        const form = document.getElementById('loginForm');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin(e.target);
        });
    },

    handleSignup(form) {
        const formData = new FormData(form);
        const userData = {
            fullName: formData.get('fullName'),
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword'),
            department: formData.get('department'),
            role: formData.get('role'),
            hobbies: formData.get('hobbies'),
            bio: formData.get('bio'),
            terms: formData.get('terms')
        };

        if (!this.validateSignup(userData)) return;

        const users = JSON.parse(localStorage.getItem('villageUsers') || '[]');
        
        if (users.some(u => u.username === userData.username)) {
            alert('Username already exists!');
            return;
        }
        
        if (users.some(u => u.email === userData.email)) {
            alert('Email already exists!');
            return;
        }

        const newUser = {
            id: Date.now(),
            fullName: userData.fullName,
            username: userData.username,
            email: userData.email,
            password: userData.password,
            department: userData.department,
            role: userData.role,
            hobbies: userData.hobbies.split(',').map(h => h.trim()),
            bio: userData.bio,
            createdAt: new Date().toISOString()
        };

        users.push(newUser);
        localStorage.setItem('villageUsers', JSON.stringify(users));
        
        localStorage.setItem('currentUser', JSON.stringify({
            id: newUser.id,
            username: newUser.username,
            fullName: newUser.fullName
        }));

        alert('Account created successfully!');
        window.location.href = 'chat.html';
    },

    validateSignup(data) {
        if (!data.fullName || !data.username || !data.email || !data.password) {
            alert('Please fill in all required fields!');
            return false;
        }

        if (data.password !== data.confirmPassword) {
            alert('Passwords do not match!');
            return false;
        }

        if (data.password.length < 6) {
            alert('Password must be at least 6 characters!');
            return false;
        }

        if (!data.terms) {
            alert('Please accept the terms and conditions!');
            return false;
        }

        return true;
    },

    handleLogin(form) {
        const formData = new FormData(form);
        const loginData = {
            usernameEmail: formData.get('usernameEmail'),
            password: formData.get('password')
        };

        const users = JSON.parse(localStorage.getItem('villageUsers') || '[]');
        const user = users.find(u => 
            (u.username === loginData.usernameEmail || u.email === loginData.usernameEmail) &&
            u.password === loginData.password
        );

        if (!user) {
            alert('Invalid credentials!');
            return;
        }

        localStorage.setItem('currentUser', JSON.stringify({
            id: user.id,
            username: user.username,
            fullName: user.fullName
        }));

        alert('Login successful!');
        window.location.href = 'chat.html';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Auth.init();
});