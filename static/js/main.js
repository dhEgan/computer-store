
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const bookingDateInput = document.getElementById('id_booking_date');
    if (bookingDateInput) {
        
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        bookingDateInput.min = minDateTime;
        
       
        if (!bookingDateInput.value) {
            bookingDateInput.value = minDateTime;
        }
    }


    const ratingStars = document.querySelectorAll('.rating-stars input');
    ratingStars.forEach(star => {
        star.addEventListener('change', function() {
            const ratingValue = this.value;
            console.log(`Selected rating: ${ratingValue} stars`);
        });
    });

   
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.classList.toggle('visible');
        });
    });

    
    const authForms = document.querySelectorAll('.auth-form form');
    authForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Đang xử lý...';
            }
        });
    });

   
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('nav ul');
    
    if (menuToggle && nav) {
        menuToggle.addEventListener('click', function() {
            nav.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
});


function initChatWidget() {
    const chatIcons = document.querySelectorAll('.chat-icon');
    
    chatIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const platform = this.getAttribute('data-platform');
            let url = '';
            
            switch(platform) {
                case 'facebook':
                    url = 'https://m.me/yourspapage';
                    break;
                case 'zalo':
                    url = 'https://zalo.me/yourzalonumber';
                    break;
                case 'whatsapp':
                    url = 'https://wa.me/yourwhatsappnumber';
                    break;
                default:
                    url = '#';
            }
            
            window.open(url, '_blank');
        });
    });
}


document.addEventListener('DOMContentLoaded', function() {
    initChatWidget();
});