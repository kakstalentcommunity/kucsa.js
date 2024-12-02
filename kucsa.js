document.querySelectorAll('nav a').forEach(anchor =>{
    anchor.addEventsListener('click', function(e){
        e.preventDefault();
        const section = document .querySelector(this.getAttribute('href'))
        section.scrollIntoView({ behavior: 'smooth'});
    });
});
const observerOptions = {
    threshold: 0.2
};
const observer = new IntersectionObserver((entries) =>{
    entries.forEach(entry=>{
        if(entry.isIntersecting){
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translate(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.news-card').forEach(card=>{
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition ='opacity 0.5s, transform 0.5s';
    observer.observe(card);
});
document.querySelectorAll('.fixture-item').forEach(item=>{
    item.addEventListener('mouseenter', () =>{
        item.style.transform = 'scale(1.02)';
        item.style.transition = 'transform 0.3s';
    });
    item.addEventListener('mouseleave', () =>{
        item.style.transform = 'scale(1)';
    });
});

document.querySelector('.contact-form button').addEventlistener('click', (e)=>{
    e.preventDefault();
    alert('Thank you for your message! We will get back to you soon.');
    document.querySelector('.contact-form').reset();
});