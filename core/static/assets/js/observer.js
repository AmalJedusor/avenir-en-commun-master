const headerEl = document.querySelector('.navbar-default')
const sentinalEl = document.querySelector('.jumbotron')

const handler = (entries) => {
  if (!entries[0].isIntersecting) {
    headerEl.classList.add('enabled')
  } else {
    headerEl.classList.remove('enabled')
  }
}
const observer = new window.IntersectionObserver(handler, {
    threshold: 0.9
})
observer.observe(sentinalEl)