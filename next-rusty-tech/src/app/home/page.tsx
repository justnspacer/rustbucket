import SlideShow from '@/components/slides/SlideShow';
import SlideShowPlus from '@/components/slides/SlideShowPlus';

const HomePage = () => {  
  // Create a new list of slides
  const additionalSlides = [
    {
      image: "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?q=80&w=2000&auto=format&fit=crop&ixlib=rb-4.0.3",
      header: "Innovative Solutions",
      description: "Discover cutting-edge technology and innovative solutions tailored for your needs."
    },
    {
      image: "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?q=80&w=2000&auto=format&fit=crop&ixlib=rb-4.0.3",
      header: "Seamless Integration",
      description: "Experience seamless integration with our state-of-the-art tools and services."
    },
    {
      image: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=2000&auto=format&fit=crop&ixlib=rb-4.0.3",
      header: "Unparalleled Support",
      description: "Our team is here to provide unparalleled support every step of the way."
    },
    {
      image: "https://images.unsplash.com/photo-1652202090716-819995ac42fe?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      header: "Your Success, Our Mission",
      description: "Partner with us to achieve your goals and drive success."
    }
  ];
    const homeSlides = [
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
    const newSlides = [
      {
        image: "https://images.unsplash.com/photo-1729761970428-3d12c122f9d6?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        header: "Lorem ipsum dolor sit amet consectetur adipisicing",
        description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugiat dolorem facilis repellendus accusantium cupiditate iste laudantium delectus dolores"
      },
      {
        image: "https://images.unsplash.com/photo-1745613999710-1aaf60145502?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        header: "Request a Quote",
        description: "Every time I do it makes me laugh"
      },
      {
        image: "https://images.unsplash.com/photo-1650919875754-fe0c9079ca27?q=80&w=1994&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        header: "Check out our portfolio",
        description: "A selection of our various projects."
      },
      {
        image: "https://images.unsplash.com/photo-1594897030264-ab7d87efc473?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        header: "Look at this photograph",
        description: "Every time I do it makes me laugh"
      }
    ];
  return <>
    <SlideShowPlus slides={additionalSlides} slideClasses={{even: 'active', odd: 'active',}} autoplay={false} autoplayInterval={20000}/>
  <SlideShow slides={homeSlides} slideClasses={{even: 'left-arrow-shape', odd: 'right-arrow-shape',}} autoplay={true} autoplayInterval={10000}/>


  </>
  ;
};

export default HomePage;