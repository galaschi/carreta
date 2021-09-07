var dropdown = document.querySelector('.dropdown');
dropdown.addEventListener('click', function(event) {
  event.stopPropagation();
  dropdown.classList.toggle('is-active');
});

function loading(){
            $("#loading").show();
            $("#loading-text").show();
            $("#content").hide();
        }