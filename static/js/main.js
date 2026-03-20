// Main JS Utilities

document.addEventListener("DOMContentLoaded", () => {
    updateNavbar();
});

function getToken() {
    return localStorage.getItem('token');
}

function getAuthUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function showLoader() {
    document.getElementById('loader').classList.remove('d-none');
}

function hideLoader() {
    document.getElementById('loader').classList.add('d-none');
}

function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastPlacement');
    const toastId = 'toast-' + Date.now();
    
    // Icon mapping
    const icon = type === 'success' ? 'bi-check-circle-fill' : 
                 type === 'danger' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle-fill';

    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 mb-2 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex p-2">
                <div class="toast-body d-flex align-items-center fs-6 fw-semibold">
                    <i class="bi ${icon} me-2 fs-5"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastEl = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastEl, { delay: 4000 });
    bsToast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}

function updateNavbar() {
    const user = getAuthUser();
    const navUl = document.getElementById('auth-nav');
    if(!navUl) return;

    let html = `
        <li class="nav-item">
            <a class="nav-link fw-semibold px-3" href="${HOME_URL}">Home</a>
        </li>
        <li class="nav-item">
            <a class="nav-link fw-semibold px-3" href="${JOBS_URL}">Explore Jobs</a>
        </li>
    `;

    if(user) {
        const dashboardUrl = user.role === 'employer' ? EMPLOYER_DASHBOARD_URL : CANDIDATE_DASHBOARD_URL;
        html += `
            <li class="nav-item">
                <a class="nav-link fw-semibold px-3 text-warning" href="${dashboardUrl}">
                    <i class="bi bi-speedometer2 me-1"></i> Dashboard
                </a>
            </li>
            <li class="nav-item ms-lg-3">
                <a class="btn btn-light text-primary fw-bold px-4 rounded-pill shadow-sm mt-2 mt-lg-0" href="#" onclick="logout(event)">
                    Logout <i class="bi bi-box-arrow-right ms-1"></i>
                </a>
            </li>
        `;
    } else {
        html += `
            <li class="nav-item ms-lg-3">
                <a class="btn btn-outline-light fw-bold px-4 rounded-pill mt-2 mt-lg-0 me-2" href="${LOGIN_URL}">Sign In</a>
            </li>
            <li class="nav-item">
                <a class="btn btn-light text-primary fw-bold px-4 rounded-pill shadow-sm mt-2 mt-lg-0" href="${REGISTER_URL}">Sign Up</a>
            </li>
        `;
    }
    navUl.innerHTML = html;
}

async function logout(e) {
    if(e) e.preventDefault();
    const token = getToken();
    if(token) {
        showLoader();
        try {
            await fetch('/api/auth/logout/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'X-CSRFToken': CSRF_TOKEN
                }
            });
        } catch(err) {
            console.error(err);
        } finally {
            hideLoader();
        }
    }
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = HOME_URL;
}

function requireAuth(role = null) {
    const user = getAuthUser();
    if(!user) {
        window.location.href = LOGIN_URL;
        return false;
    }
    if(role && user.role !== role) {
        window.location.href = HOME_URL;
        return false;
    }
    return true;
}

// Shared component renderer for job cards (used in home and jobs list)
function renderJobs(jobs, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!jobs || jobs.length === 0) {
        container.innerHTML = `<div class="col-12 text-center py-5">
            <div class="display-1 text-muted mb-3"><i class="bi bi-search"></i></div>
            <h3 class="fw-bold text-muted">No jobs found</h3>
            <p>Try adjusting your filters or search keywords.</p>
        </div>`;
        return;
    }

    const html = jobs.map((job, index) => {
        const delay = (index % 6) * 0.1; // Staggered animation
        
        // Define badge color based on job type
        const typeBadgeMap = {
            'full-time': 'bg-success',
            'part-time': 'bg-warning text-dark',
            'internship': 'bg-info text-dark'
        };
        const badgeClass = typeBadgeMap[job.job_type] || 'bg-secondary';
        const typeLabel = job.job_type.replace('-', ' ').toUpperCase();
        
        // Format skills
        const skillsSnippet = job.skills.split(',').slice(0, 3).map(s => `<span class="badge bg-light text-dark border me-1">${s.trim()}</span>`).join('');
        
        const applyBtnText = getAuthUser() && getAuthUser().role === 'employer' ? 'View Job' : 'View & Apply';
        const btnClass = getAuthUser() && getAuthUser().role === 'employer' ? 'btn-outline-secondary' : 'btn-outline-primary';

        return `
        <div class="col-md-6 col-lg-4 animate-slide-up" style="animation-delay: ${delay}s">
            <div class="card h-100 border-0 shadow-sm rounded-4 hover-lift">
                <div class="card-body p-4 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <span class="badge ${badgeClass} mb-2">${typeLabel}</span>
                            <h5 class="card-title fw-bold mb-1">${job.title}</h5>
                            <h6 class="card-subtitle text-muted flex-grow-1"><i class="bi bi-building me-1"></i>${job.company}</h6>
                        </div>
                    </div>
                    
                    <div class="mb-3 text-muted small">
                        <div class="mb-1"><i class="bi bi-geo-alt-fill text-danger me-2"></i>${job.location}</div>
                        <div><i class="bi bi-cash-stack text-success me-2"></i>${job.salary}</div>
                    </div>

                    <div class="mb-4">
                        ${skillsSnippet}
                        ${job.skills.split(',').length > 3 ? `<span class="badge bg-light text-muted border">+ more</span>` : ''}
                    </div>

                    <div class="mt-auto pt-3 border-top d-flex justify-content-between align-items-center">
                        <small class="text-muted"><i class="bi bi-clock me-1"></i>${new Date(job.created_at).toLocaleDateString()}</small>
                        <a href="/jobs/${job.id}/" class="btn ${btnClass} btn-sm rounded-pill px-3 fw-bold">${applyBtnText}</a>
                    </div>
                </div>
            </div>
        </div>
        `;
    }).join('');

    container.innerHTML = html;
}
