"use client";
import React, { useEffect, useState } from 'react';

const SlideShow = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    
    const interval = setInterval(() => {
      setCurrentSlide((prevSlide) => (prevSlide + 1) % slides.length);
    }, 8000);

    return () => clearInterval(interval);
  }, []);


  const handleDotClick = (index: number) => {
    setCurrentSlide(index);
  };

  const slides = [
    {
      image: "https://images.unsplash.com/photo-1652202090716-819995ac42fe?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      header: "Welcome to Rust Bucket",
      description: "Let's work together to bring your vision to life on the web!"
    },
    {
      image: "https://images.unsplash.com/photo-1735401031516-114a352f6fa3?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      header: "Request a Quote",
      description: "Every time I do it makes me laugh"
    },
    {
      image: "https://images.unsplash.com/photo-1733155259427-1c1f73ab98b1?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      header: "Check out our portfolio",
      description: "A selection of our various projects."
    },
    {
      image: "https://images.unsplash.com/photo-1735845078210-953081cee65d?q=80&w=2093&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      header: "Look at this photograph",
      description: "Every time I do it makes me laugh"
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide - 1 + slides.length) % slides.length);
  };

  return (
<section className="slideshow">
  <div className='container'>
    <button className='previous' onClick={prevSlide}><i className="fa-solid fa-angle-left"></i></button>
      <div className={`slide ${currentSlide % 2 === 0 ? 'left' : 'right'}`}>
        <div className="image-container">
          <img src={slides[currentSlide].image} alt="slide image" />
        </div>
        <div className="message">
          <h1 className="header">{slides[currentSlide].header}</h1>
          <p className="description">{slides[currentSlide].description}</p>
        </div>
      </div>
      <button className='next' onClick={nextSlide}><i className="fa-solid fa-angle-right"></i></button>
  </div>
      <div className="dots-container">
        {slides.map((_, index) => (
          <span
            key={index}
            className={`dot ${index === currentSlide ? 'active' : ''}`}
            onClick={() => handleDotClick(index)}
          ></span>
        ))}
      </div>
    </section>
  );
};

export default SlideShow;