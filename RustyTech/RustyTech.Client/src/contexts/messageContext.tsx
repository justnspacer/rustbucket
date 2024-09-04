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
    const [message, setMessage] = useState<string>('');

    const clearMessage = () => setMessage('');

    return (
        <MessageContext.Provider value={{ message, setMessage, clearMessage }}>
            {children}
        </MessageContext.Provider>
    );
};