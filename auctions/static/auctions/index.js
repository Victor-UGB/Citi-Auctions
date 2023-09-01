let el = document.getElementsByClassName("burger.nav")
let nav = document.getElementsByClassName("nav")
el.addEventListener("click", () => {
    if(nav.style.display === "none"){
        nav.style.display = "block"
    }else{
        nav.style.display = "none"
    }
})