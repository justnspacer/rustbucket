import SlideShow from '@/components/SlideShow';

const HomePage = () => {  
  
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
  <SlideShow slides={homeSlides}/>
  <SlideShow slides={newSlides}/>

  </>
  ;
};

export default HomePage;