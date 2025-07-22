'use client';

import { useEffect, useRef } from 'react';

interface UseIntersectionAnimationOptions {
  threshold?: number;
  rootMargin?: string;
  triggerOnce?: boolean;
}

export function useIntersectionAnimation(
  options: UseIntersectionAnimationOptions = {}
) {
  const elementRef = useRef<HTMLElement>(null);
  
  const {
    threshold = 0.1,
    rootMargin = '0px',
    triggerOnce = true
  } = options;

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('show');
            
            // Handle staggered animations
            if (entry.target.hasAttribute('data-animate-stagger')) {
              const staggerDelay = parseInt(
                entry.target.getAttribute('data-animate-stagger') || '100'
              );
              const children = entry.target.querySelectorAll('.animate');
              children.forEach((child, index) => {
                setTimeout(() => {
                  child.classList.add('show');
                }, index * staggerDelay);
              });
            }
            
            if (triggerOnce) {
              observer.unobserve(entry.target);
            }
          } else if (!triggerOnce) {
            entry.target.classList.remove('show');
          }
        });
      },
      {
        threshold,
        rootMargin,
      }
    );

    observer.observe(element);

    return () => {
      if (element) {
        observer.unobserve(element);
      }
    };
  }, [threshold, rootMargin, triggerOnce]);

  return elementRef;
}

// Setup function for initializing animations on page load
export function setupIntersectionAnimations() {
  if (typeof window === 'undefined') return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
          
          // Handle staggered animations
          if (entry.target.hasAttribute('data-animate-stagger')) {
            const staggerDelay = parseInt(
              entry.target.getAttribute('data-animate-stagger') || '100'
            );
            const children = entry.target.querySelectorAll('.animate');
            children.forEach((child, index) => {
              setTimeout(() => {
                child.classList.add('show');
              }, index * staggerDelay);
            });
          }
          
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: '0px',
    }
  );

  // Observe all animated elements
  document.querySelectorAll('.animate').forEach((el) => {
    observer.observe(el);
  });

  // Observe stagger groups
  document.querySelectorAll('[data-animate-stagger]').forEach((group) => {
    observer.observe(group);
  });
}

// Individual element observer
export function observeElement(element: Element) {
  if (typeof window === 'undefined') return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: '0px',
    }
  );

  observer.observe(element);
}
