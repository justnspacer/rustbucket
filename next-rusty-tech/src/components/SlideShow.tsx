"use client";
import React, { useEffect, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleLeft, faAngleRight } from '@fortawesome/free-solid-svg-icons';

export interface Slide {
  image: string;
  header: string;
  description: string;
}

interface SlideShowProps {
  slides: Slide[];
  slideClasses?: {
    even: string;
    odd: string;
  };
  autoplay?: boolean;
  autoplayInterval?: number;
}

export const SlideShow: React.FC<SlideShowProps> = ({ 
  slides, 
  slideClasses = { even: '', odd: '' }, 
  autoplay = true, 
  autoplayInterval = 1000 
 }) => {

  const [currentSlide, setCurrentSlide] = useState(0);

  const nextSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide + 1) % slides.length);
  };

  useEffect(() => {
    if (!autoplay) return;

    const interval = setInterval(() => {
      nextSlide();
      }, autoplayInterval);

    return () => clearInterval(interval);

  }, [autoplay, autoplayInterval, slides.length]);

  const appliedSlideClasses =
    currentSlide % 2 === 0 ? slideClasses.even || '' : slideClasses.odd || '';

  const handleDotClick = (index: number) => {
    setCurrentSlide(index);
  };



  const prevSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide - 1 + slides.length) % slides.length);
  };

  return (
<section className="slideshow">
  <div className='container'>
    <button className='previous' onClick={prevSlide}><FontAwesomeIcon icon={faAngleLeft} /></button>
      <div className={`slide ${appliedSlideClasses}`}>
        <div className="image-container">
          <img src={slides[currentSlide].image} alt="slide image" />
        </div>
        <div className="message">
          <h1 className="header">{slides[currentSlide].header}</h1>
          <p className="description">{slides[currentSlide].description}</p>
        </div>
      </div>
      <button className='next' onClick={nextSlide}><FontAwesomeIcon icon={faAngleRight} /></button>
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