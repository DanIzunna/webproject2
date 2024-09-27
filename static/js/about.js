document.addEventListener("DOMContentLoaded", function() {
    const teamMembers = document.querySelectorAll('.team-member');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('loaded');
                observer.unobserve(entry.target);
            }
        });
    });

    teamMembers.forEach(member => {
        observer.observe(member);
    });
});
