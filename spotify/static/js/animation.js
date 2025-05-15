// Simple Intersection Observer setup
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
      observer.unobserve(entry.target); // remove if you only want to trigger once
    }
  });
});

// Observe individual animated elements
document.querySelectorAll('.animate').forEach((el) => observer.observe(el));

// Observe groups with stagger
document
  .querySelectorAll('[data-animate-stagger]')
  .forEach((group) => observer.observe(group));
