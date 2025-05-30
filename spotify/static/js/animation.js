// Simple Intersection Observer setup
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
      observer.unobserve(entry.target); // remove if you only want to trigger once
    }
    // Handle staggered animations
    if (entry.target.hasAttribute('data-animate-stagger')) {
      const stagger = entry.target.getAttribute('data-animate-stagger');
      const children = entry.target.querySelectorAll('.animate');
      children.forEach((child, index) => {
        setTimeout(() => {
          child.classList.add('show');
        }, index * stagger);
      });
    }
  });
});

window.setupIntersectionAnimations = function () {
  // Observe individual animated elements
  document.querySelectorAll('.animate').forEach((el) => observer.observe(el));
  // Observe groups with stagger
  document
    .querySelectorAll('[data-animate-stagger]')
    .forEach((group) => observer.observe(group));
};

window.observeElement = function (el) {
  observer.observe(el);
};
