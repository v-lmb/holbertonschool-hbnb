const API_URL = 'http://localhost:5000';

/* ---- EASTER EGGS ---- */

// Tab title change on visibility
const originalTitle = document.title;
document.addEventListener('visibilitychange', () => {
    document.title = document.hidden
        ? 'Come back — the case is not yet closed...'
        : originalTitle;
});

// Logo click — 5 clicks = citation
const QUOTES = [
    '« Élémentaire, mon cher Watson. » — Sherlock Holmes',
    '« Quand vous avez éliminé l\'impossible, ce qui reste doit être la vérité. » — S. Holmes',
    '« Je suis Arsène Lupin, gentleman-cambrioleur. » — Arsène Lupin',
    '« La vie est une aventure ou elle n\'est rien. » — Arsène Lupin',
    '« Mon cerveau se révolte à la stagnation. » — Sherlock Holmes',
    '« Il n\'est de problème que l\'intelligence humaine ne puisse résoudre. » — S. Holmes',
];
let logoClickCount = 0;
document.addEventListener('DOMContentLoaded', () => {
    const logo = document.querySelector('.logo');
    if (logo) {
        logo.addEventListener('click', (e) => {
            e.preventDefault();
            logoClickCount++;
            if (logoClickCount >= 5) {
                logoClickCount = 0;
                const quote = QUOTES[Math.floor(Math.random() * QUOTES.length)];
                alert(quote);
            } else {
                window.location.href = 'index.html';
            }
        });
    }
});

/* ---- CORNER DECORATIONS ---- */
document.addEventListener('DOMContentLoaded', () => {
    const cornersData = [
        { cls: 'top-left',     src: 'images/Corner-top-left.png' },
        { cls: 'top-right',    src: 'images/Corner-top-right.png' },
        { cls: 'bottom-left',  src: 'images/Corner-bottom-left.png' },
        { cls: 'bottom-right', src: 'images/Corner-bottom-right.png' },
    ];
    cornersData.forEach(({ cls, src }) => {
        const img = document.createElement('img');
        img.src = src;
        img.className = `corner-img ${cls}`;
        img.alt = '';
        document.body.appendChild(img);
    });

    function updateCorners() {
        const header = document.querySelector('header');
        const footer = document.querySelector('footer');
        const headerBottom = header ? Math.max(0, header.getBoundingClientRect().bottom) : 0;
        const footerOffset = footer ? Math.max(0, window.innerHeight - footer.getBoundingClientRect().top) : 0;
        document.querySelectorAll('.corner-img.top-left, .corner-img.top-right').forEach(el => {
            el.style.top = headerBottom + 'px';
        });
        document.querySelectorAll('.corner-img.bottom-left, .corner-img.bottom-right').forEach(el => {
            el.style.bottom = (footerOffset + 1) + 'px';
        });
    }

    window.addEventListener('scroll', updateCorners, { passive: true });
    window.addEventListener('resize', updateCorners);
    updateCorners();
});

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

function decodeToken(token) {
    try { return JSON.parse(atob(token.split('.')[1])); } catch { return null; }
}

let toastTimer = null;
function showToast(message, type = 'info') {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.className = `toast toast-${type}`;
    clearTimeout(toastTimer);
    requestAnimationFrame(() => {
        toast.classList.add('visible');
        toastTimer = setTimeout(() => toast.classList.remove('visible'), 3500);
    });
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesList = document.getElementById('places-list');
    const placeDetails = document.getElementById('place-details');
    const reviewForm = document.getElementById('review-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    if (placesList) {
        populatePriceFilter();
        populateCountryFilter();
        checkAuthIndex();
        document.getElementById('price-filter').addEventListener('change', applyFilters);
        document.getElementById('country-filter').addEventListener('change', applyFilters);
    }

    if (placeDetails) {
        const placeId = getPlaceIdFromURL();
        checkAuthPlace(placeId);
    }

    if (document.getElementById('mystery-page')) {
        initMysteryPage();
    }

    if (document.getElementById('profile-content')) {
        initProfilePage();
    }

    if (document.getElementById('my-places-content')) {
        initMyPlacesPage();
    }

    if (document.getElementById('messages-page')) {
        initMessagesPage();
    }

    if (reviewForm && document.getElementById('rating')) {
        const token = checkAuthReview();
        const placeId = getPlaceIdFromURL();
        if (token && placeId) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const reviewText = document.getElementById('review').value;
                const rating = parseInt(document.getElementById('rating').value, 10);
                await submitReview(token, placeId, reviewText, rating);
            });
        }
    }
});

/* ---- LOGIN ---- */

async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        showToast('Elementary, my dear friend — incorrect login details.', 'error');
    }
}

/* ---- INDEX ---- */

function populatePriceFilter() {
    const select = document.getElementById('price-filter');
    ['All', 10, 50, 100].forEach(val => {
        const opt = document.createElement('option');
        opt.value = val === 'All' ? 'all' : val;
        opt.textContent = val === 'All' ? 'All' : `$${val}`;
        select.appendChild(opt);
    });
}

function populateCountryFilter() {
    const select = document.getElementById('country-filter');
    if (!select) return;
    const countries = [...new Set(Object.values(PLACE_COUNTRIES))].sort();
    [{ value: 'all', label: 'All' }, ...countries.map(c => ({ value: c, label: c }))].forEach(({ value, label }) => {
        const opt = document.createElement('option');
        opt.value = value;
        opt.textContent = label;
        select.appendChild(opt);
    });
}

function applyFilters() {
    const priceVal = document.getElementById('price-filter').value;
    const countryVal = document.getElementById('country-filter').value;
    document.querySelectorAll('.place-card').forEach(card => {
        const priceOk = priceVal === 'all' || parseFloat(card.dataset.price) <= parseFloat(priceVal);
        const countryOk = countryVal === 'all' || card.dataset.country === countryVal;
        card.style.display = (priceOk && countryOk) ? 'block' : 'none';
    });
}

function checkAuthIndex() {
    const token = getCookie('token');
    updateAuthButton(token);
    fetchPlaces(token);
}

function updateAuthButton(token) {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;
    if (token) {
        const payload = decodeToken(token);
        const userId = payload ? payload.sub : '';
        [
            { href: `profile.html?user_id=${userId}`, text: 'Profile' },
            { href: 'messages.html', text: 'Messages' },
            { href: 'my_places.html', text: 'My Places' },
        ].forEach(({ href, text }) => {
            const a = document.createElement('a');
            a.href = href;
            a.textContent = text;
            a.className = 'login-button';
            loginLink.insertAdjacentElement('beforebegin', a);
        });
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            document.cookie = 'token=; path=/; max-age=0';
            window.location.href = 'index.html';
        });
    } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
    }
}

async function fetchPlaces(token) {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const response = await fetch(`${API_URL}/api/v1/places/`, { headers });
    if (response.ok) {
        const places = await response.json();
        displayPlaces(places);
    }
}

const CHARACTER_BIOS = {
    'holmes@baker.st': {
        bio: 'I am a consulting detective — the only one of my kind in the world. I created the profession myself. When Scotland Yard finds itself out of its depth, which is most of the time, they come to me. My methods are founded on observation, deduction, and a thorough knowledge of criminal history. I am currently between cases, though my mind is never entirely at rest.',
        initials: 'SH', color: '#4A3728',
    },
    'watson@baker.st': {
        bio: 'I served as an army surgeon in Afghanistan before a jezail bullet cut short my career in the field. Since returning to London, I have had the privilege — and occasional misfortune — of accompanying Mr Sherlock Holmes on a great number of his investigations. I record what I witness as faithfully as I can, though Holmes invariably finds fault with my prose.',
        initials: 'JW', color: '#3A5240',
    },
    'irene@opera.fr': {
        bio: 'I am a contralto, formerly of the Imperial Opera of Warsaw, now residing in Paris on my own terms. I have been called adventuress, which I take as a compliment. I once outmanoeuvred Mr Sherlock Holmes in a matter of some personal importance. I do not speak of it often — I find that silence is more effective.',
        initials: 'IA', color: '#5C2D4A',
    },
    'moriarty@consulting.co': {
        bio: 'I held the chair of Mathematics at a university I prefer not to name. I resigned to pursue more interesting work. My organisational abilities are, I am told, considerable — I coordinate endeavours of some complexity across several countries simultaneously. Mr Holmes has called me the Napoleon of Crime. I consider the comparison flattering to Napoleon.',
        initials: 'JM', color: '#1A2A3A',
    },
    'ganimard@prefecture.fr': {
        bio: 'I have served the Sûreté de Paris for thirty-two years and I am proud of my record — with one persistent exception. Arsène Lupin has eluded me on more occasions than I care to count. I am, however, a patient man. I will be there when he finally makes his error. In the meantime, I am available for all other matters of criminal investigation.',
        initials: 'IG', color: '#5A4A20',
    },
    'lupin@nowhere.fr': {
        bio: 'I am Arsène Lupin, gentleman-cambrioleur. I rob only those who deserve it, I never harm the innocent, and I always leave a calling card — it seems only sporting. I have been arrested twice. Neither occasion lasted long. If you are reading this profile, I am probably not where you think I am. I wish you the very best of luck.',
        initials: 'AL', color: '#2A3060',
    },
    'admin@hbnb.io': {
        bio: 'I administer the HBnB registry. I maintain the records, manage the listings, and ensure that everything remains in order. I ask no questions and I answer very few. The platform runs smoothly. That is all you need to know.',
        initials: 'AD', color: '#3A3A3A',
    },
};

const PLACE_CLUES = {
    '221B Baker Street': `Watson's private journal, 3 May 1891.<br><em>"H. has booked passage to Switzerland. He refused to explain why, but his manner was that of a man settling his affairs. He spoke of a final confrontation — a waterfall, somewhere in the mountains, beyond the reach of London. I fear I understand more than he wishes me to."</em>`,
    "The Spider's Web, Pall Mall": `Recovered from a locked drawer, addressed to no one.<br><em>"The appointment stands. The falls at R. are ideal — no path, no witnesses, no return. Holmes will come. He always does. This will be the last game."</em>`,
    'Manoir de Gueures': `Found folded behind the third bookcase, handwriting unknown.<br><em>"I have warned all agents. Holmes is travelling south-east. His destination is Meiringen. The professor will be waiting at the falls. Whatever happens there — this file must not survive."</em>`,
    'Sussex Downs Cottage': `From an undated page torn from a beekeeping notebook.<br><em>"I have stood at the edge of those falls once. I looked down and saw nothing but white water and the end of something. Moriarty is gone. I came back. I do not intend to return to that place — not even in writing."</em>`,
};

const PLACE_COUNTRIES = {
    '221B Baker Street':                  'England',
    'Aiguille Creuse Manor':              'France',
    "The Spider's Web, Pall Mall":        'England',
    'Villa Cagliostro':                   'Monaco',
    'Manoir de Gueures':                  'France',
    'Rue Pergolèse Apartment, Paris':     'France',
    'Montague Street Rooms, Bloomsbury':  'England',
    'Sussex Downs Cottage':               'England',
};

const PLACE_IMAGES = {
    '221B Baker Street':               ['images/221BakerStreet(1).png',   'images/221BakerStreet(2).png',  'images/211BakerStreet(3).png'],
    'Aiguille Creuse Manor':           ['images/AuguilleManor(1).png',    'images/AuguilleManor(2).png',   'images/AuguilleManor(3).png'],
    "The Spider's Web, Pall Mall":     ['images/SpiderWeb(1).png'],
    'Villa Cagliostro':                ['images/VillaCagliostro(1).png',  'images/VillaCagliostro(2).png'],
    'Manoir de Gueures':               ['images/Gueures(1).png',          'images/Gueures(2).png',         'images/Gueures(3).png'],
    'Rue Pergolèse Apartment, Paris':  ['images/Pergolèse(1).png',        'images/Pergolèse(2).png',       'images/Pergolèse(3).png'],
    'Montague Street Rooms, Bloomsbury': ['images/Montague(1).png',       'images/Montague(2).png'],
    'Sussex Downs Cottage':            ['images/Sussex(1).png',           'images/Sussex(2).png',          'images/Sussex(3).png'],
};

function initLightbox() {
    const lb = document.getElementById('lightbox');
    if (!lb) return;
    document.querySelectorAll('[data-lightbox]').forEach(el => {
        el.addEventListener('click', () => {
            lb.querySelector('img').src = el.dataset.lightbox;
            lb.classList.add('open');
        });
    });
    lb.querySelector('.lightbox-close').addEventListener('click', () => lb.classList.remove('open'));
    lb.addEventListener('click', e => { if (e.target === lb) lb.classList.remove('open'); });
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    list.innerHTML = '';
    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('place-card');
        card.dataset.price = place.price;
        card.dataset.country = PLACE_COUNTRIES[place.title] || 'all';
        const stars = place.avg_rating
            ? '★'.repeat(Math.round(place.avg_rating)) + '☆'.repeat(5 - Math.round(place.avg_rating))
            : '☆☆☆☆☆';
        const ratingLabel = place.avg_rating
            ? `${place.avg_rating}/5 <span class="review-count">(${place.review_count} review${place.review_count > 1 ? 's' : ''})</span>`
            : '<em>No reviews yet</em>';
        const imgs = PLACE_IMAGES[place.title];
        const imgStyle = imgs
            ? `style="background-image: url('${imgs[0]}'); background-size: cover; background-position: center;"`
            : '';
        card.innerHTML = `
            <div class="place-card-photo" ${imgStyle}></div>
            <h3>${place.title}</h3>
            <p class="card-stars">${stars} ${ratingLabel}</p>
            <p>$${place.price} / night</p>
            <a href="place.html?place_id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });

    const mysteryCard = document.createElement('div');
    mysteryCard.classList.add('place-card', 'mystery-card');
    mysteryCard.dataset.price = '0';
    const solved = localStorage.getItem('mystery_solved');
    mysteryCard.innerHTML = `
        <div class="place-card-photo mystery-photo"></div>
        <h3>???</h3>
        <p class="card-stars mystery-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</p>
        <p>${solved ? 'Classified &mdash; Resolved' : 'Classified &mdash; Access Denied'}</p>
        <a href="mystery.html" class="details-button mystery-button">Investigate</a>
    `;
    list.appendChild(mysteryCard);
}

/* ---- PLACE DETAILS ---- */

function checkAuthPlace(placeId) {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    updateAuthButton(token);
    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (addReviewSection) {
            addReviewSection.style.display = 'block';
            const btn = document.getElementById('add-review-btn');
            if (btn) btn.href = `add_review.html?place_id=${placeId}`;
        }
    }
    fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const [placeRes, reviewsRes] = await Promise.all([
        fetch(`${API_URL}/api/v1/places/${placeId}`, { headers }),
        fetch(`${API_URL}/api/v1/places/${placeId}/reviews`, { headers })
    ]);
    if (!placeRes.ok) return;

    const place = await placeRes.json();
    const reviews = reviewsRes.ok ? await reviewsRes.json() : [];

    const ownerRes = await fetch(`${API_URL}/api/v1/users/${place.owner_id}`, { headers });
    const owner = ownerRes.ok ? await ownerRes.json() : null;

    const userIds = [...new Set(reviews.map(r => r.user_id))];
    const userMap = {};
    await Promise.all(userIds.map(async id => {
        const res = await fetch(`${API_URL}/api/v1/users/${id}`, { headers });
        if (res.ok) userMap[id] = await res.json();
    }));

    displayPlaceDetails(place, owner, reviews, userMap);
}

function displayPlaceDetails(place, owner, reviews, userMap) {
    const section = document.getElementById('place-details');
    const token = getCookie('token');
    const hostName = owner ? `${owner.first_name} ${owner.last_name}` : place.owner_id;

    const overallStars = place.avg_rating
        ? '★'.repeat(Math.round(place.avg_rating)) + '☆'.repeat(5 - Math.round(place.avg_rating))
        : null;

    const imgs = PLACE_IMAGES[place.title] || [];
    const mainStyle = imgs[0] ? `style="background-image: url('${imgs[0]}'); background-size: cover; background-position: center;"` : '';
    const mainLightbox = imgs[0] ? `data-lightbox="${imgs[0]}"` : '';
    const thumb1Style = imgs[1] ? `style="background-image: url('${imgs[1]}'); background-size: cover; background-position: center;"` : '';
    const thumb1Lightbox = imgs[1] ? `data-lightbox="${imgs[1]}"` : '';
    const thumb2Style = imgs[2] ? `style="background-image: url('${imgs[2]}'); background-size: cover; background-position: center;"` : '';
    const thumb2Lightbox = imgs[2] ? `data-lightbox="${imgs[2]}"` : '';

    const amenitiesHTML = place.amenities && place.amenities.length
        ? place.amenities.map(a => `<div class="amenity-item"><span class="amenity-check">&#10003;</span>${a.name}</div>`).join('')
        : '<p class="no-amenities">No amenities listed.</p>';

    const ratingBar = overallStars
        ? `<div class="place-rating-bar"><span class="place-stars">${overallStars}</span><span class="place-score">${place.avg_rating}/5</span><span class="place-review-count">&mdash; ${place.review_count} review${place.review_count > 1 ? 's' : ''}</span></div>`
        : `<div class="place-rating-bar place-no-rating">No reviews yet</div>`;

    section.innerHTML = `
        <div class="place-details">
            <h1 class="place-title">${place.title}</h1>
            <div class="place-gallery">
                <div class="gallery-main" ${mainStyle} ${mainLightbox}></div>
                <div class="gallery-side">
                    <div class="gallery-thumb" ${thumb1Style} ${thumb1Lightbox}></div>
                    <div class="gallery-thumb" ${thumb2Style} ${thumb2Lightbox}></div>
                </div>
            </div>
            <div class="place-info">
                ${ratingBar}
                <p class="place-host">Hosted by <a href="profile.html?user_id=${place.owner_id}" class="place-host-link">${hostName}</a></p>
                <div class="place-body">
                    <p class="place-description">${place.description || 'No description provided.'}</p>
                    <p class="place-price">$${place.price} <span>/ night</span></p>
                </div>
                <div id="map" style="height: 300px; margin-top: 2rem; border-radius: 8px;"></div>
                <div class="amenities-section">
                    <h2>Amenities</h2>
                    <div class="amenities-grid">${amenitiesHTML}</div>
                </div>
                ${token ? `
                <div class="booking-section">
                    <h2>Reserve this place</h2>
                    <form id="booking-form-inner">
                        <div class="booking-row">
                            <div class="booking-field">
                                <label for="checkin">Check-in</label>
                                <input type="date" id="checkin" required>
                            </div>
                            <div class="booking-field">
                                <label for="checkout">Check-out</label>
                                <input type="date" id="checkout" required>
                            </div>
                            <div class="booking-field">
                                <label for="guests">Guests</label>
                                <input type="number" id="guests" min="1" max="20" value="1" required>
                            </div>
                        </div>
                        <p id="booking-total" class="booking-total"></p>
                        <button type="submit">Book Now</button>
                    </form>
                    <div id="booking-confirmation" class="booking-confirmation" style="display:none;"></div>
                </div>` : ''}
            </div>
        </div>
    `;

    initLightbox();
    if (token) initBookingForm(place.price);

    if (PLACE_CLUES[place.title]) {
        const caseFile = document.createElement('div');
        caseFile.classList.add('case-file');
        caseFile.innerHTML = `
            <div class="case-file-header">
                <span class="case-stamp">CLASSIFIED</span>
                <span class="case-file-toggle">Case File &mdash; click to unseal</span>
            </div>
            <div class="case-file-content">${PLACE_CLUES[place.title]}</div>
        `;
        caseFile.querySelector('.case-file-header').addEventListener('click', () => {
            caseFile.classList.toggle('open');
        });
        section.querySelector('.place-details').appendChild(caseFile);
    }

    if (!document.getElementById('leaflet-css')) {
        const link = document.createElement('link');
        link.id = 'leaflet-css';
        link.rel = 'stylesheet';
        link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        document.head.appendChild(link);
    }
    if (!window.L) {
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        script.onload = () => initMap(place.latitude, place.longitude, place.title);
        document.head.appendChild(script);
    } else {
        initMap(place.latitude, place.longitude, place.title);
    }

    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    if (reviews && reviews.length) {
        reviews.forEach(r => {
            const user = userMap[r.user_id];
            const userName = user ? `${user.first_name} ${user.last_name}` : 'Anonymous';
            const date = new Date(r.created_at).toLocaleDateString('fr-FR', {
                year: 'numeric', month: 'long', day: 'numeric'
            });
            const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
            const card = document.createElement('div');
            card.classList.add('review-card');
            card.innerHTML = `
                <p class="review-stars">${stars}</p>
                <p class="review-text">${r.text}</p>
                <p class="review-author">By <strong>${userName}</strong> &mdash; ${date}</p>
            `;
            reviewsSection.appendChild(card);
        });
    } else {
        const noReview = document.createElement('p');
        noReview.textContent = 'No reviews yet.';
        reviewsSection.appendChild(noReview);
    }
}

function initBookingForm(pricePerNight) {
    const form = document.getElementById('booking-form-inner');
    const checkin = document.getElementById('checkin');
    const checkout = document.getElementById('checkout');
    const totalEl = document.getElementById('booking-total');
    const confirmation = document.getElementById('booking-confirmation');

    const today = new Date().toISOString().split('T')[0];
    checkin.min = today;
    checkout.min = today;

    function updateTotal() {
        const ci = new Date(checkin.value);
        const co = new Date(checkout.value);
        if (checkin.value && checkout.value && co > ci) {
            const nights = Math.round((co - ci) / 86400000);
            const total = (nights * pricePerNight).toFixed(2);
            totalEl.textContent = `${nights} night${nights > 1 ? 's' : ''} × $${pricePerNight} = $${total}`;
        } else {
            totalEl.textContent = '';
        }
    }

    checkin.addEventListener('change', () => {
        if (checkout.value && checkout.value <= checkin.value) checkout.value = '';
        checkout.min = checkin.value || today;
        updateTotal();
    });
    checkout.addEventListener('change', updateTotal);

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const ci = new Date(checkin.value);
        const co = new Date(checkout.value);
        if (!checkin.value || !checkout.value || co <= ci) {
            showToast('Please select valid check-in and check-out dates.', 'error');
            return;
        }
        const nights = Math.round((co - ci) / 86400000);
        const total = (nights * pricePerNight).toFixed(2);
        const guests = document.getElementById('guests').value;
        const fmt = d => d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
        form.style.display = 'none';
        confirmation.style.display = 'block';
        confirmation.innerHTML = `
            <strong>Booking confirmed.</strong><br>
            Check-in: ${fmt(ci)}<br>
            Check-out: ${fmt(co)}<br>
            Guests: ${guests}<br>
            Duration: ${nights} night${nights > 1 ? 's' : ''}<br>
            Total: <strong>$${total}</strong>
        `;
    });
}

function initMap(lat, lng, title) {
    const map = L.map('map').setView([lat, lng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    L.marker([lat, lng]).addTo(map).bindPopup(title).openPopup();
}

/* ---- MYSTERY ---- */

function initMysteryPage() {
    updateAuthButton(getCookie('token'));
    if (localStorage.getItem('mystery_solved')) {
        showMysteryReveal();
        return;
    }
    const btn = document.getElementById('mystery-submit');
    const input = document.getElementById('mystery-answer');
    const error = document.getElementById('mystery-error');
    btn.addEventListener('click', () => {
        const answer = input.value.trim().toUpperCase();
        if (answer === 'REICHENBACH') {
            localStorage.setItem('mystery_solved', '1');
            showMysteryReveal();
        } else {
            error.textContent = 'That is not the answer. The case remains open.';
        }
    });
    input.addEventListener('keydown', e => { if (e.key === 'Enter') btn.click(); });
}

function showMysteryReveal() {
    document.getElementById('mystery-intro').style.display = 'none';
    const reveal = document.getElementById('mystery-reveal');
    reveal.style.display = 'block';
    const resetBtn = document.getElementById('mystery-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            localStorage.removeItem('mystery_solved');
            window.location.reload();
        });
    }
    if (getCookie('token')) {
        const bookingEl = document.getElementById('mystery-booking');
        if (bookingEl) {
            bookingEl.style.display = 'block';
            initMysteryBookingForm(189);
        }
    }
}

function initMysteryBookingForm(pricePerNight) {
    const form = document.getElementById('mystery-booking-form');
    const checkin = document.getElementById('mystery-checkin');
    const checkout = document.getElementById('mystery-checkout');
    const totalEl = document.getElementById('mystery-booking-total');
    const confirmation = document.getElementById('mystery-booking-confirmation');

    const today = new Date().toISOString().split('T')[0];
    checkin.min = today;
    checkout.min = today;

    function updateTotal() {
        const ci = new Date(checkin.value);
        const co = new Date(checkout.value);
        if (checkin.value && checkout.value && co > ci) {
            const nights = Math.round((co - ci) / 86400000);
            const total = (nights * pricePerNight).toFixed(2);
            totalEl.textContent = `${nights} night${nights > 1 ? 's' : ''} × $${pricePerNight} = $${total}`;
        } else {
            totalEl.textContent = '';
        }
    }

    checkin.addEventListener('change', () => {
        if (checkout.value && checkout.value <= checkin.value) checkout.value = '';
        checkout.min = checkin.value || today;
        updateTotal();
    });
    checkout.addEventListener('change', updateTotal);

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const ci = new Date(checkin.value);
        const co = new Date(checkout.value);
        if (!checkin.value || !checkout.value || co <= ci) {
            showToast('Please select valid check-in and check-out dates.', 'error');
            return;
        }
        const nights = Math.round((co - ci) / 86400000);
        const total = (nights * pricePerNight).toFixed(2);
        const guests = document.getElementById('mystery-guests').value;
        const fmt = d => d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
        form.style.display = 'none';
        confirmation.style.display = 'block';
        confirmation.innerHTML = `
            <strong>Booking confirmed.</strong><br>
            Check-in: ${fmt(ci)}<br>
            Check-out: ${fmt(co)}<br>
            Guests: ${guests}<br>
            Duration: ${nights} night${nights > 1 ? 's' : ''}<br>
            Total: <strong>$${total}</strong>
        `;
    });
}

/* ---- ADD REVIEW ---- */

function checkAuthReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

async function submitReview(token, placeId, reviewText, rating) {
    const response = await fetch(`${API_URL}/api/v1/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text: reviewText, rating: rating, place_id: placeId })
    });
    if (response.ok) {
        showToast('Review submitted successfully!', 'success');
        window.location.href = `place.html?place_id=${placeId}`;
    } else {
        const data = await response.json().catch(() => ({}));
        showToast('Failed to submit review: ' + (data.error || response.statusText), 'error');
    }
}

/* ---- MESSAGES ---- */

const CONVERSATIONS = [
    {
        participants: ['holmes@baker.st', 'moriarty@consulting.co'],
        label: 'S. Holmes \u2014 J. Moriarty',
        date: '4\u20135 May 1891',
        messages: [
            { from: 'moriarty@consulting.co', sender: 'Moriarty', time: '4 May 1891 \u2014 09:14',
              text: 'Mr Holmes. I trust you received my note regarding the chess set at the Spider\u2019s Web. My bishop was moved in your absence. A professional courtesy.' },
            { from: 'holmes@baker.st', sender: 'Holmes', time: '4 May 1891 \u2014 09:47',
              text: 'I observed it. I also observed the loose floorboard beneath the study desk and the absence of the Meissen figurine. Careless, Professor.' },
            { from: 'moriarty@consulting.co', sender: 'Moriarty', time: '4 May 1891 \u2014 10:03',
              text: 'Not careless. A test. You passed, as expected. That is the tedious part about you, Mr Holmes. You always pass.' },
            { from: 'holmes@baker.st', sender: 'Holmes', time: '4 May 1891 \u2014 10:31',
              text: 'Then I suggest we meet somewhere the stakes are higher. I have Meiringen in mind. The falls are picturesque this time of year.' },
            { from: 'moriarty@consulting.co', sender: 'Moriarty', time: '5 May 1891 \u2014 08:55',
              text: 'I know the place. Thursday, then. Do bring your coat. The mist off the Reichenbach is considerable.' },
        ],
    },
    {
        participants: ['lupin@nowhere.fr', 'ganimard@prefecture.fr'],
        label: 'A. Lupin \u2014 Inspecteur Ganimard',
        date: 'March 1902',
        messages: [
            { from: 'lupin@nowhere.fr', sender: 'Lupin', time: '12 March 1902 \u2014 07:20',
              text: 'My dear Ganimard. By the time you read this, I shall be in Monaco. The warrant issued at Calais was most flattering. Please give my regards to the Commissioner.' },
            { from: 'ganimard@prefecture.fr', sender: 'Ganimard', time: '12 March 1902 \u2014 14:06',
              text: 'Lupin. I have your description on every port from Calais to Nice. You will make an error eventually. You always do.' },
            { from: 'lupin@nowhere.fr', sender: 'Lupin', time: '13 March 1902 \u2014 09:44',
              text: 'I made one already \u2014 I booked the Villa Cagliostro under my own name. But the view was worth it. Do try the pool before winter. You have earned it.' },
            { from: 'ganimard@prefecture.fr', sender: 'Ganimard', time: '13 March 1902 \u2014 16:12',
              text: 'I am not going to Monaco, Lupin.' },
            { from: 'lupin@nowhere.fr', sender: 'Lupin', time: '13 March 1902 \u2014 18:30',
              text: 'I have already booked your room. Room 7, second floor. The key is under the third flagstone to the left of the gate. You are most welcome.' },
        ],
    },
    {
        participants: ['watson@baker.st', 'irene@opera.fr'],
        label: 'Dr J. Watson \u2014 I. Adler',
        date: 'November 1895',
        messages: [
            { from: 'irene@opera.fr', sender: 'Irene Adler', time: '3 November 1895 \u2014 11:00',
              text: 'Dear Doctor Watson. I read your latest account with some interest. The description of the woman in the case was, as usual, imprecise. I suspect you know who wrote the note. You are simply too gentlemanly to say so.' },
            { from: 'watson@baker.st', sender: 'Watson', time: '4 November 1895 \u2014 09:15',
              text: 'Miss Adler. Holmes has asked me not to confirm or deny. I am bound by professional confidence. I will say only that the handwriting was exceptional.' },
            { from: 'irene@opera.fr', sender: 'Irene Adler', time: '4 November 1895 \u2014 14:33',
              text: 'Thank you, Doctor. That is all the confirmation I required. Give my regards to Baker Street. I shall not be returning \u2014 but then, I never needed to.' },
        ],
    },
    {
        participants: ['holmes@baker.st', 'watson@baker.st'],
        label: 'S. Holmes \u2014 J. Watson',
        date: 'October 1903',
        messages: [
            { from: 'holmes@baker.st', sender: 'Holmes', time: '1 October 1903 \u2014 08:02',
              text: 'Watson. Sussex in October. Bring your coat and your revolver \u2014 the second is precautionary. A letter has arrived from Switzerland. Someone else was at Reichenbach. Come on Thursday.' },
            { from: 'watson@baker.st', sender: 'Watson', time: '1 October 1903 \u2014 10:47',
              text: 'Holmes, I thought you had put all that behind you. It has been twelve years.' },
            { from: 'holmes@baker.st', sender: 'Holmes', time: '1 October 1903 \u2014 11:15',
              text: 'It is never behind me. But the case is new and the bees are peaceful. Mrs Hudson will prepare the rooms. Thursday, Watson. I would not ask if it were not necessary.' },
            { from: 'watson@baker.st', sender: 'Watson', time: '1 October 1903 \u2014 12:00',
              text: 'I will be on the morning train. Save me a chair by the fire.' },
        ],
    },
];

async function initMessagesPage() {
    const token = getCookie('token');
    if (!token) { window.location.href = 'index.html'; return; }
    updateAuthButton(token);

    const payload = decodeToken(token);
    const userId = payload ? payload.sub : null;
    if (!userId) return;

    const res = await fetch(`${API_URL}/api/v1/users/${userId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) return;
    const user = await res.json();

    const myEmail = user.email;
    const myThreads = CONVERSATIONS.filter(c => c.participants.includes(myEmail));
    const list = document.getElementById('messages-list');

    if (!myThreads.length) {
        list.innerHTML = '<p><em>No correspondence on file.</em></p>';
        return;
    }

    myThreads.forEach(thread => {
        const body = thread.messages.map(m => {
            const side = m.from === myEmail ? 'msg-right' : 'msg-left';
            return `<div class="msg ${side}">
                <span class="msg-sender">${m.sender}</span>
                <p>${m.text}</p>
                <span class="msg-time">${m.time}</span>
            </div>`;
        }).join('');

        const el = document.createElement('div');
        el.className = 'msg-thread';
        el.innerHTML = `
            <div class="msg-thread-header">
                <span class="msg-thread-participants">${thread.label}</span>
                <span class="msg-thread-date">${thread.date}</span>
            </div>
            <div class="msg-thread-body">${body}</div>
        `;
        list.appendChild(el);
    });
}

/* ---- PROFILE ---- */

async function initProfilePage() {
    const token = getCookie('token');
    updateAuthButton(token);

    const params = new URLSearchParams(window.location.search);
    let userId = params.get('user_id');
    if (!userId && token) {
        const payload = decodeToken(token);
        userId = payload ? payload.sub : null;
    }
    if (!userId) { window.location.href = 'index.html'; return; }

    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const [userRes, placesRes] = await Promise.all([
        fetch(`${API_URL}/api/v1/users/${userId}`, { headers }),
        fetch(`${API_URL}/api/v1/places/`, { headers })
    ]);
    if (!userRes.ok) { document.getElementById('profile-content').innerHTML = '<p>User not found.</p>'; return; }

    const user = await userRes.json();
    const allPlaces = placesRes.ok ? await placesRes.json() : [];
    displayProfile(user, allPlaces.filter(p => p.owner_id === userId));
}

function displayProfile(user, places) {
    const bio = CHARACTER_BIOS[user.email] || {
        bio: 'No biography on file.',
        initials: (user.first_name[0] + user.last_name[0]).toUpperCase(),
        color: '#3A3A3A',
    };
    const placesHTML = places.length
        ? places.map(p => {
            const imgs = PLACE_IMAGES[p.title];
            const imgStyle = imgs ? `style="background-image:url('${imgs[0]}');background-size:cover;background-position:center;"` : '';
            return `<div class="place-card">
                <div class="place-card-photo" ${imgStyle}></div>
                <h3>${p.title}</h3>
                <p>$${p.price} / night</p>
                <a href="place.html?place_id=${p.id}" class="details-button">View Details</a>
            </div>`;
        }).join('')
        : '<p><em>No properties listed.</em></p>';

    document.getElementById('profile-content').innerHTML = `
        <div class="profile-header">
            <div class="profile-avatar" style="background-color:${bio.color};">${bio.initials}</div>
            <div class="profile-info">
                <h1>${user.first_name} ${user.last_name}</h1>
                <p class="profile-email">${user.email}</p>
            </div>
        </div>
        <p class="profile-bio">${bio.bio}</p>
        <h2>Properties</h2>
        <div class="profile-places-grid">${placesHTML}</div>
    `;
}

/* ---- MY PLACES ---- */

async function initMyPlacesPage() {
    const token = getCookie('token');
    if (!token) { window.location.href = 'index.html'; return; }
    updateAuthButton(token);

    const payload = decodeToken(token);
    const userId = payload ? payload.sub : null;
    if (!userId) return;

    const headers = { 'Authorization': `Bearer ${token}` };
    const res = await fetch(`${API_URL}/api/v1/places/`, { headers });
    if (!res.ok) return;

    const allPlaces = await res.json();
    displayMyPlaces(allPlaces.filter(p => p.owner_id === userId));
}

function displayMyPlaces(places) {
    const list = document.getElementById('my-places-list');
    if (!places.length) {
        list.innerHTML = '<p><em>You have no listed properties.</em></p>';
        return;
    }
    list.innerHTML = '';
    places.forEach(p => {
        const imgs = PLACE_IMAGES[p.title];
        const imgStyle = imgs ? `style="background-image:url('${imgs[0]}');background-size:cover;background-position:center;"` : '';
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <div class="place-card-photo" ${imgStyle}></div>
            <h3>${p.title}</h3>
            <p>$${p.price} / night</p>
            <div class="my-place-actions">
                <a href="place.html?place_id=${p.id}" class="my-place-delete">View</a>
                <button class="my-place-delete" onclick="simulateDelete(this, '${p.id}')">Remove listing</button>
            </div>
        `;
        list.appendChild(card);
    });
}

function simulateDelete(btn, placeId) {
    const actions = btn.parentElement;
    actions.innerHTML = `
        <span class="my-place-confirm-text">Remove this listing?</span>
        <button class="my-place-delete" onclick="btn_confirmDelete(this, '${placeId}')">Yes</button>
        <button class="my-place-cancel" onclick="cancelDelete(this, '${placeId}')">Cancel</button>
    `;
}

function btn_confirmDelete(btn, placeId) {
    btn.closest('.place-card').remove();
}

function cancelDelete(btn, placeId) {
    const actions = btn.parentElement;
    actions.innerHTML = `
        <a href="place.html?place_id=${placeId}" class="my-place-delete">View</a>
        <button class="my-place-delete" onclick="simulateDelete(this, '${placeId}')">Remove listing</button>
    `;
}
