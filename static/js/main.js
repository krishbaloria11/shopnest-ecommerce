/* ShopNest Pro — Interactive Glassmorphism UI/UX JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    // ----------------------------------------------------
    // 1. Theme Toggle (Dark / Light Mode)
    // ----------------------------------------------------
    const themeToggleBtns = document.querySelectorAll('#themeToggle, .theme-toggle-btn');
    const htmlElement = document.documentElement;

    const savedTheme = localStorage.getItem('shopnest_theme') || 'dark';
    setTheme(savedTheme);

    themeToggleBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const currentTheme = htmlElement.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    });

    function setTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        localStorage.setItem('shopnest_theme', theme);

        const darkIcons = document.querySelectorAll('.theme-icon-dark');
        const lightIcons = document.querySelectorAll('.theme-icon-light');

        if (theme === 'dark') {
            darkIcons.forEach(i => i.classList.remove('d-none'));
            lightIcons.forEach(i => i.classList.add('d-none'));
        } else {
            darkIcons.forEach(i => i.classList.add('d-none'));
            lightIcons.forEach(i => i.classList.remove('d-none'));
        }
    }

    // ----------------------------------------------------
    // 2. Sticky Glass Navbar on Scroll
    // ----------------------------------------------------
    const mainNavbar = document.getElementById('mainNavbar');
    const scrollTopBtn = document.getElementById('scrollTopBtn');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 40) {
            if (mainNavbar) mainNavbar.classList.add('scrolled');
            if (scrollTopBtn) scrollTopBtn.classList.add('show');
        } else {
            if (mainNavbar) mainNavbar.classList.remove('scrolled');
            if (scrollTopBtn) scrollTopBtn.classList.remove('show');
        }
    });

    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ----------------------------------------------------
    // 3. Glass Toast Notifications Generator
    // ----------------------------------------------------
    window.showToast = function (message, type = 'success') {
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) return;

        const toastId = 'toast-' + Date.now();
        let bgStyle = 'background: rgba(16, 185, 129, 0.9); color: #fff;';
        let icon = 'bi-check-circle-fill';

        if (type === 'danger' || type === 'error') {
            bgStyle = 'background: rgba(239, 68, 68, 0.95); color: #fff;';
            icon = 'bi-exclamation-triangle-fill';
        } else if (type === 'warning') {
            bgStyle = 'background: rgba(245, 158, 11, 0.95); color: #000;';
            icon = 'bi-exclamation-circle-fill';
        } else if (type === 'info') {
            bgStyle = 'background: rgba(56, 189, 248, 0.95); color: #000;';
            icon = 'bi-info-circle-fill';
        }

        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center border-0 shadow-lg mb-2" role="alert" aria-live="assertive" aria-atomic="true" style="${bgStyle} backdrop-filter: blur(12px); border-radius: 14px;">
                <div class="d-flex align-items-center p-2">
                    <div class="toast-body d-flex align-items-center fw-semibold py-1">
                        <i class="bi ${icon} me-2 fs-5"></i>
                        <span>${message}</span>
                    </div>
                    <button type="button" class="btn-close ${type === 'warning' || type === 'info' ? '' : 'btn-close-white'} me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        const toastElem = document.getElementById(toastId);
        const bsToast = new bootstrap.Toast(toastElem, { delay: 4000 });
        bsToast.show();

        toastElem.addEventListener('hidden.bs.toast', function () {
            toastElem.remove();
        });
    };

    // ----------------------------------------------------
    // 4. Process Server-Side Django Messages as Toasts
    // ----------------------------------------------------
    const djangoMessages = document.querySelectorAll('#djangoMessages [data-msg]');
    djangoMessages.forEach(function (msgElem) {
        const msg = msgElem.getAttribute('data-msg');
        const type = msgElem.getAttribute('data-type') || 'info';
        if (msg) {
            showToast(msg, type);
        }
    });

    // ----------------------------------------------------
    // 5. AJAX Add to Cart
    // ----------------------------------------------------
    document.addEventListener('submit', function (e) {
        const form = e.target.closest('.add-to-cart-form');
        if (!form) return;

        e.preventDefault();
        const btn = form.querySelector('.add-cart-btn');
        if (btn && btn.disabled) return;

        const originalBtnHTML = btn ? btn.innerHTML : '';
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Adding...`;
        }

        const actionUrl = form.getAttribute('action');
        const formData = new FormData(form);

        fetch(actionUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;

            if (data.status === 'success') {
                showToast(data.message, 'success');

                // Update Navbar Cart Badge
                const cartBadge = document.getElementById('cartBadge');
                if (cartBadge) {
                    cartBadge.textContent = data.cart_count;
                    cartBadge.style.display = data.cart_count > 0 ? 'inline-block' : 'none';
                    cartBadge.classList.add('badge-pop');
                    setTimeout(() => cartBadge.classList.remove('badge-pop'), 400);
                }
            } else {
                showToast(data.message || 'Could not add to cart.', 'danger');
            }
        })
        .catch(err => {
            console.error('Error adding to cart:', err);
            showToast('An error occurred. Please try again.', 'danger');
        })
        .finally(() => {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = originalBtnHTML;
            }
        });
    });

    // ----------------------------------------------------
    // 6. AJAX Wishlist Toggle
    // ----------------------------------------------------
    document.addEventListener('click', function (e) {
        const heartBtn = e.target.closest('.wishlist-toggle-btn');
        if (!heartBtn) return;

        e.preventDefault();
        const url = heartBtn.getAttribute('data-url') || heartBtn.getAttribute('href');
        if (!url) return;

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;

            if (data.status === 'success') {
                showToast(data.message, 'info');

                // Update Heart Button UI
                if (data.action === 'added') {
                    heartBtn.classList.add('active');
                    heartBtn.innerHTML = '<i class="bi bi-heart-fill"></i>';
                } else {
                    heartBtn.classList.remove('active');
                    heartBtn.innerHTML = '<i class="bi bi-heart"></i>';

                    // If we're on the wishlist page, optionally remove the card
                    const wishlistCardCol = heartBtn.closest('.wishlist-item-col');
                    if (wishlistCardCol) {
                        wishlistCardCol.style.transition = 'all 0.3s ease';
                        wishlistCardCol.style.opacity = '0';
                        wishlistCardCol.style.transform = 'scale(0.8)';
                        setTimeout(() => wishlistCardCol.remove(), 300);
                    }
                }

                // Update Navbar Wishlist Badge
                const wishlistBadge = document.getElementById('wishlistBadge');
                if (wishlistBadge) {
                    wishlistBadge.textContent = data.wishlist_count;
                    wishlistBadge.style.display = data.wishlist_count > 0 ? 'inline-block' : 'none';
                    wishlistBadge.classList.add('badge-pop');
                    setTimeout(() => wishlistBadge.classList.remove('badge-pop'), 400);
                }
            } else {
                showToast(data.message || 'Wishlist action failed.', 'danger');
            }
        })
        .catch(err => {
            console.error('Error toggling wishlist:', err);
            showToast('Please login to use Wishlist.', 'warning');
        });
    });

    // ----------------------------------------------------
    // 7. Auto Submit Sort Selector on Change
    // ----------------------------------------------------
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function () {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('sort', this.value);
            currentUrl.searchParams.delete('page'); // Reset to page 1 on sort
            window.location.href = currentUrl.toString();
        });
    }

    // ----------------------------------------------------
    // 8. Payment Method Card Selection Visuals
    // ----------------------------------------------------
    const paymentCards = document.querySelectorAll('.payment-method-card');
    paymentCards.forEach(card => {
        const radio = card.querySelector('input[type="radio"]');
        if (radio && radio.checked) {
            card.classList.add('selected');
        }
        card.addEventListener('click', function () {
            paymentCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            if (radio) radio.checked = true;
        });
    });

    // ----------------------------------------------------
    // 9. Failsafe Bootstrap Modal Lifecycle & Backdrop Cleanup
    // ----------------------------------------------------
    let lastActiveTrigger = null;

    document.addEventListener('show.bs.modal', function (event) {
        lastActiveTrigger = event.relatedTarget || document.activeElement;
    });

    document.addEventListener('hidden.bs.modal', function (event) {
        const modal = event.target;
        
        // Remove any orphaned backdrops if no other modal is open
        const openModals = document.querySelectorAll('.modal.show');
        if (openModals.length === 0) {
            const backdrops = document.querySelectorAll('.modal-backdrop');
            backdrops.forEach(b => b.remove());
            document.body.classList.remove('modal-open');
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
        }

        // Return focus to the trigger button for accessibility
        if (lastActiveTrigger && typeof lastActiveTrigger.focus === 'function') {
            lastActiveTrigger.focus();
        }
    });

    // ----------------------------------------------------
    // 10. Cancellation Form Double-Submission Prevention
    // ----------------------------------------------------
    document.addEventListener('submit', function (e) {
        const form = e.target.closest('.cancel-order-form');
        if (!form) return;

        const submitBtn = form.querySelector('.confirm-cancel-btn');
        if (submitBtn) {
            if (submitBtn.disabled) {
                e.preventDefault();
                return;
            }
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Cancelling Order...`;
        }
    });
});


