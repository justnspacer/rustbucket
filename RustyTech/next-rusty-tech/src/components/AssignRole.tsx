"use client";

import { useState } from "react";
import { auth, functions, httpsCallable } from "@/firebase/firebaseConfig"

const AssignRole = () => {
    const [uid, setUid] = useState("");
    const [role, setRole] = useState("");
    const [message, setMessage] = useState("");

    const setUserRole = httpsCallable(functions, "setUserRole");

    const handleAssignRole = async () => {
        try {
            const response = await setUserRole({ uid, role });
            setMessage((response as any).data.message); // Adjust as per actual response structure
        } catch (error: any) {
            setMessage(error.message || "Failed to assign role.");
        }
    };

    return (
        <div>
            <h2>Assign Role</h2>
            <input
                type="text"
                placeholder="User ID"
                value={uid}
                onChange={(e) => setUid(e.target.value)}
            />
            <input
                type="text"
                placeholder="Role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
            />
            <button onClick={handleAssignRole}>Assign Role</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default AssignRole;
