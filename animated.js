document.body.style.backgroundImage = "url('frog.jpg')";
document.body.style.backgroundImage = "url('lasagna.jpg')";
document.body.style.backgroundSize = "cover";
document.body.style.backgroundRepeat = "no-repeat";
document.body.style.backgroundAttachment = "fixed";
window.addEventListener('scroll', function() {
    let scrollPosition = window.scrollY;
    if (scrollPosition <= document.body.scrollHeight / 2) {
        document.body.style.transition = "background-image 5s ease-in";
        document.body.style.backgroundImage = "url('frog.jpg')";
        document.body.style.transition = "background-image 5s ease-out";
        document.body.style.backgroundImage = "url('lasagna.jpg')";
    }
    else if (scrollPosition >= document.body.scrollHeight / 2) {
        document.body.style.transition = "background-image 5s ease-in";
        document.body.style.backgroundImage = "url('lasagna.jpg')";
        document.body.style.transition = "background-image 5s ease-out";
        document.body.style.backgroundImage = "url('frog.jpg')";
    }
});
