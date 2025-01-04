import React, { useState } from 'react';

interface AccordionItemProps {
    title: string;
    content: string;
    index: number;
    activeIndex: number | null;
    handleClick: (index: number) => void;
}

const AccordionItem: React.FC<AccordionItemProps> = ({ title, content, index, activeIndex, handleClick }) => {
    const isActive = index === activeIndex;

    return (
        <div className="accordion-item">
            <button className="accordion-header" onClick={() => handleClick(index)}>
                {title}
            </button>
            <div
                className="accordion-content"
                style={{
                    maxHeight: isActive ? '500px' : '0',
                    overflow: 'hidden',
                    transition: 'max-height 0.3s ease',
                }}
            >
                {isActive && (
                    <div
                        dangerouslySetInnerHTML={{ __html: content }}
                    />
                )}
            </div>
        </div>
    );
};

const HomePage: React.FC = () => {
    const [activeIndex, setActiveIndex] = useState<number | null>(null);

    const handleClick = (index: number) => {
        setActiveIndex(prevIndex => (prevIndex === index ? null : index)); // Toggle between open/close
    };

    return (
        <><main>

            <div className="homepage-message">
                <h1 className="homepage-header">Welcome to Rust Bucket</h1>
                <p className="homepage-description">Let's work together to bring your vision to life on the web!</p>
            </div>
            {/*<div className="homepage-image-container">*/}
            {/*    <img className="homepage-image" src="https://images.unsplash.com/photo-1728708018018-a9848e3835df?q=80&w=200&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />*/}
            {/*</div>*/}


            <div className="accordion homepage-accordion">
                <div className="accordion-item">
                    <AccordionItem
                        title="About"
                        content="<p>We specialize in crafting custom websites and digital solutions that elevate your online presence.
                            With a strong foundation in the latest web technologies, We deliver responsive, user-friendly designs tailored
                            to meet the unique needs of your business. Whether you're looking to build a new website from scratch,
                            optimize an existing one, or create an engaging e-commerce platform, I am dedicated to providing high-quality,
                            innovative services that help you achieve your goals. Let's work together to bring your vision to life on the web.</p>
                        <ul><li><a href='/contact'>Contact</a></li><li><a href='/request'>Request Service</a></li></ul>"
                        index={0}
                        activeIndex={activeIndex}
                        handleClick={handleClick}
                    />
                    <AccordionItem
                        title="Projects"
                        content="<p><ul><li><a href='/users'>User Posts Project (new name)</a></li></ul></p>"
                        index={1}
                        activeIndex={activeIndex}
                        handleClick={handleClick}
                    />
                    <AccordionItem
                        title="Request Service"
                        content="<p>Request Form</p>"
                        index={2}
                        activeIndex={activeIndex}
                        handleClick={handleClick}
                    />
                    </div>
            </div>
        </main>
        </>
    );
};

export default HomePage;