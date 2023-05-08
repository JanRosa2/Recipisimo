const elements = document.querySelectorAll(".nav-link");
    elements.forEach(element => {
            if(element.getAttribute("href") === window.location.pathname)
            {
                element.classList.add("act_link");
            }
});
