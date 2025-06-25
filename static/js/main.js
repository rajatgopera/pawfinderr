// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add animation to cards on scroll
    const animateOnScroll = function() {
        const cards = document.querySelectorAll('.card, .puppy-card');
        
        cards.forEach((card, index) => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (cardPosition < screenPosition) {
                card.style.animation = `fadeIn 0.5s ease forwards ${index * 0.1}s`;
            }
        });
    };
    
    // Run on load and scroll
    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Form validation feedback
    document.querySelectorAll('.needs-validation').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Image preview for file inputs
    document.querySelectorAll('.img-preview-input').forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            const preview = this.nextElementSibling;
            const reader = new FileReader();
            
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
            
            if (file) {
                reader.readAsDataURL(file);
            }
        });
    });
});

// Puppy search map functionality
function initPuppyMap() {
    if (typeof google === 'undefined') return;
    
    const mapElement = document.getElementById('puppyMap');
    if (!mapElement) return;
    
    const locations = JSON.parse(mapElement.dataset.locations || '[]');
    if (locations.length === 0) return;
    
    const map = new google.maps.Map(mapElement, {
        zoom: 12,
        center: new google.maps.LatLng(locations[0].lat, locations[0].lng),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    
    const infowindow = new google.maps.InfoWindow();
    let marker, i;
    
    for (i = 0; i < locations.length; i++) {  
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i].lat, locations[i].lng),
            map: map,
            icon: {
                url: locations[i].status === 'LOST' ? 
                    '/static/images/lost-marker.png' : 
                    '/static/images/found-marker.png',
                scaledSize: new google.maps.Size(40, 40)
            }
        });
        
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infowindow.setContent(`
                    <div class="map-info-window">
                        <h6>${locations[i].name}</h6>
                        <p>${locations[i].breed}, ${locations[i].age} yrs</p>
                        <small>Last seen: ${locations[i].date}</small>
                        <div class="text-center mt-2">
                            <a href="/puppy/${locations[i].id}" class="btn btn-sm btn-primary">View Details</a>
                        </div>
                    </div>
                `);
                infowindow.open(map, marker);
            }
        })(marker, i));
    }
}

// Load Google Maps API if needed
function loadGoogleMaps() {
    if (document.getElementById('puppyMap')) {
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initPuppyMap`;
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
    }
}

// Call loadGoogleMaps when needed
if (document.getElementById('puppyMap')) {
    loadGoogleMaps();
}