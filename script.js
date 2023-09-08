const search_alert = document.getElementById("btn-search");
search_alert.addEventListener("click", 
    function(){
        alert("Under Maintenance!");
    },
)

const toogle = document.getElementById('btn-menu');
const nav = document.querySelector('header ul');

toogle.addEventListener('click', function() {
    if (nav.style.display == 'none') {
        nav.style.display = 'flex';
    } else {
        nav.style.display = 'none';
    }
});

window.addEventListener('resize', function() {
    if (window.innerWidth > 955) {
        nav.style.display = 'flex';
    } else {
        nav.style.display = 'none';
    }
});