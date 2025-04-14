// Reset button text when user starts typing in the review textarea
document.getElementById('review').addEventListener('input', function () {
    const btn = document.getElementById('submitBtn');
    if (!btn.classList.contains('loading')) {
        btn.innerHTML = '✨ Generate Response';
    }
});

// Update button text when form is being submitted
function handleSubmit(event) {
    const btn = document.getElementById('submitBtn');
    btn.classList.add('loading');
    btn.innerHTML = '⏳ Generating... <div class="spinner">🌀</div>';
}

const moonContainer = document.getElementById('moonRating');
    const moonPhases = ['1', '2', '3', '4', '5'];

    function setDefaultRating() {
        const firstMoon = moonContainer.querySelector('.face-wrap');
        if (firstMoon) {
            const selectedRating = parseInt(firstMoon.dataset.value);
            document.getElementById('rating-value').value = selectedRating;
            document.getElementById('rating-text').textContent = selectedRating;

            moonContainer.querySelectorAll('.face-wrap').forEach(innerWrap => {
                const innerValue = parseInt(innerWrap.dataset.value);
                if (innerValue <= selectedRating) {
                    innerWrap.classList.add('active');
                } else {
                    innerWrap.classList.remove('active');
                }
            });
        }
    }

    moonContainer.querySelectorAll('.face-wrap').forEach(wrap => {
        wrap.addEventListener('click', () => {
            const selectedRating = parseInt(wrap.dataset.value);
            document.getElementById('rating-value').value = selectedRating;
            document.getElementById('rating-text').textContent = selectedRating;

            moonContainer.querySelectorAll('.face-wrap').forEach(innerWrap => {
                const innerValue = parseInt(innerWrap.dataset.value);
                if (innerValue <= selectedRating) {
                    innerWrap.classList.add('active');
                } else {
                    innerWrap.classList.remove('active');
                }
            });
        });
    });

    window.onload = setDefaultRating;