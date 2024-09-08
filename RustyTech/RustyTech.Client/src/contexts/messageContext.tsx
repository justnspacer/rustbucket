/* eslint-disable react-refresh/only-export-components */
import { createContext, useState, useContext, ReactNode } from 'react';


// Message context
interface MessageContextType {
    message: string;
    setMessage: (message: string) => void;
    clearMessage: () => void;
}

const MessageContext = createContext<MessageContextType | undefined>(undefined);

export const useMessage = () => {
    const context = useContext(MessageContext);
    if (!context) {
        throw new Error('useMessage must be used within a MessageProvider');
    }
    return context;
};

// Message provider to wrap the app
export const MessageProvider = ({ children }: { children: ReactNode }) => {
    const [message, setMessageState] = useState<string>('');

    const clearMessage = () => setMessage('');

    const setMessage = (msg: string) => {
        setMessageState(msg);
        setTimeout(() => {
            clearMessage();
        }, 30000); // Clears after 30 seconds
    };

    return (
        <MessageContext.Provider value={{ message, setMessage, clearMessage }}>
            {children}
        </MessageContext.Provider>
    );
};