import { Link } from "react-router-dom";

const ProjectsPage: React.FC = () => {

    return (
        <main>Projects
            <ul>
                <li><Link to="/posts">Rusty User Posts</Link></li>
            </ul>
        </main>
    );

};

export default ProjectsPage;