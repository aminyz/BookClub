const navOpenBtn = document.querySelector(".nav-icon");
const navCloseBtn = document.querySelector(".nav-close-btn");
const mobile_nav = document.querySelector(".mobile-nav");
const overlay = document.querySelector(".overlay");
navOpenBtn.addEventListener("click", ()=>{
  mobile_nav.classList.remove("absolute")
  mobile_nav.classList.remove("-right-[100vw]")
  mobile_nav.classList.add("right-0")

  overlay.classList.remove("hidden")
  overlay.classList.add("visible")
})

navCloseBtn.addEventListener("click", () => {
  mobile_nav.classList.remove("right-0");
  mobile_nav.classList.add("absolute")
  mobile_nav.classList.add("-right-[100vw]");

  overlay.classList.remove("visible");
  overlay.classList.add("hidden");
})

overlay.addEventListener("click", () => {
  mobile_nav.classList.remove("right-0");
  mobile_nav.classList.add("-right-[100vw]");

  overlay.classList.remove("visible");
  overlay.classList.add("hidden");
})