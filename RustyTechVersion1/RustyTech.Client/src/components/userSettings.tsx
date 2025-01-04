import { Link } from "react-router-dom";

const UserSettings: React.FC = () => {

    return (
        <main>User Settings
            <ul>
                <li><Link to="/account/reset/password">Rest Password</Link></li>
                <li><Link to="/account/update">Update User Info</Link></li>
                <li><Link to="/account/manage/2fa">Set 2 Factor Authenication</Link></li>
                <li><Link to="/account/manage/info">Admin Permission: Get Info</Link></li>
            </ul>
        </main>
    );

};

export default UserSettings;