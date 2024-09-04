import React from 'react';
import { useMessage } from '../contexts/messageContext';

const MessageDisplay: React.FC = () => {
    const { message, clearMessage } = useMessage();

    if (!message) return null;

    return (
        <div className="message-display">
            <div className="message-content">
                {message}
                <button onClick={clearMessage}>Dismiss</button>
            </div>
        </div>
    );
};

export default MessageDisplay;