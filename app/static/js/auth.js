// Auth helper functions
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}

async function getCurrentUser() {
    const token = localStorage.getItem('token');
    if (!token) return null;
    
    try {
        const response = await fetch('/api/users/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error('Failed to get current user', error);
    }
    
    return null;
}

// Update navigation based on auth status
async function updateAuthNav() {
    const authNav = document.getElementById('authNav');
    if (!authNav) return;
    
    if (isAuthenticated()) {
        const user = await getCurrentUser();
        if (user) {
            authNav.innerHTML = `
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                        ${user.username}
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="/profile">Profile</a></li>
                        ${user.is_admin ? '<li><a class="dropdown-item" href="/admin">Admin Panel</a></li>' : ''}
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#" onclick="logout()">Logout</a></li>
                    </ul>
                </li>
            `;
        }
    } else {
        authNav.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="/login">Login</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/register">Register</a>
            </li>
        `;
    }
}

// Check auth on protected pages
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login';
    }
}

// Initialize auth check on page load
document.addEventListener('DOMContentLoaded', updateAuthNav);
