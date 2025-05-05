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

export const SlideShowPlus: React.FC<SlideShowProps> = ({ 
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

  const randomizePositions = () => {
    const positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right'];
    const randomIndex = Math.floor(Math.random() * positions.length);
    const messagePosition = positions[randomIndex];
    const clickAreaPosition = positions[(randomIndex + 1) % positions.length]; // Opposite position

    const messageElement = document.querySelector('.messageplus') as HTMLElement;
    const clickAreaElement = document.querySelector('.click-area') as HTMLElement;

    if (clickAreaElement) {
      clickAreaElement.className = `click-area ${clickAreaPosition}`;
    }
  };

  useEffect(() => {
    randomizePositions();
  }, [currentSlide]);

  const prevSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide - 1 + slides.length) % slides.length);
  };

  return (
<section className="slideshowplus">
  <div className='slideshow-containerplus'>
  <button className='previous' onClick={prevSlide}><FontAwesomeIcon icon={faAngleLeft} /></button>
      <div className={`slideplus ${appliedSlideClasses}`} style={{ backgroundImage: `url(${slides[currentSlide].image})` }}>

        <div className="messageplus">
          <h1 className="header">{slides[currentSlide].header}</h1>
          <p className="description">{slides[currentSlide].description}</p>
        </div>
        <div className="click-area" style={{ backgroundImage: `url(${slides[(currentSlide + 1) % slides.length].image})` }} onClick={nextSlide}></div>
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

export default SlideShowPlus;