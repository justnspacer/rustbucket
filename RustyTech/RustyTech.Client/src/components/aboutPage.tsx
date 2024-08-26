import { Link } from "react-router-dom";


const AboutPage: React.FC = () => {

    return (
        <main>About
            <p>We specialize in crafting custom websites and digital
                solutions that elevate your online presence.
                With a strong foundation in the latest web technologies,
                We deliver responsive, user-friendly designs tailored
                to meet the unique needs of your business.
                Whether you're looking to build a new website from scratch,
                optimize an existing one, or create an engaging e-commerce platform,
                I am dedicated to providing high-quality,
                innovative services that help you achieve your goals.
                Let's work together to bring your vision to life on the web.</p>
            <ul>
                <li><Link to="/contact">Contact</Link></li>
                <li><Link to="/request">Request Service</Link></li>
            </ul>
        </main>
    );

};

export default AboutPage;