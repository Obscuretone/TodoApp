// src/config/authConfig.js

export const msalConfig = {
    auth: {
        clientId: process.env.REACT_APP_CLIENT_ID,
        authority: process.env.REACT_APP_AUTHORITY,
        redirectUri: "http://localhost:3000/authredirect", // Update to your redirect URI
    },
    cache: {
        cacheLocation: "sessionStorage", // This configures where your cache will be stored
        storeAuthStateInCookie: true, // Set to true for IE 11
    },
};


console.log("clientId" + process.env.REACT_APP_CLIENT_ID)
console.log("authority" + process.env.REACT_APP_AUTHORITY)