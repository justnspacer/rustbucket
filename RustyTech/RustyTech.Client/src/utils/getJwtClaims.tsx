import { jwtDecode } from 'jwt-decode';

interface JwtPayload {
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": string;
    "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": string;
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": string,
    exp: number;
    iss: string;
    aud: string;
}

export const getJwtClaims = (token: string) => {
    try {
        const decoded = jwtDecode<JwtPayload>(token);
        const nameIdentifier = decoded["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"];
        const role = decoded["http://schemas.microsoft.com/ws/2008/06/identity/claims/role"];
        const email = decoded["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"];
        return { nameIdentifier, role, email };
    } catch (error) {
        console.error('Invalid token', error);
        return null;
    }
};