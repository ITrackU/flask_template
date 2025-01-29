// Client-side encryption handling
class EncryptionHandler {
    constructor() {
        this.keyStorage = window.localStorage;
    }

    // Generate a new encryption key
    async generateKey() {
        const key = await window.crypto.subtle.generateKey(
            {
                name: "AES-GCM",
                length: 256
            },
            true,
            ["encrypt", "decrypt"]
        );
        
        // Export the key to store it
        const exportedKey = await window.crypto.subtle.exportKey("raw", key);
        const keyBase64 = btoa(String.fromCharCode(...new Uint8Array(exportedKey)));
        return keyBase64;
    }

    // Store the encryption key securely
    async storeKey(username, key) {
        const keyIdentifier = `encryption_key_${username}`;
        this.keyStorage.setItem(keyIdentifier, key);
    }

    // Retrieve the stored encryption key
    async getKey(username) {
        const keyIdentifier = `encryption_key_${username}`;
        return this.keyStorage.getItem(keyIdentifier);
    }

    // Encrypt data
    async encryptData(data, username) {
        const keyBase64 = await this.getKey(username);
        if (!keyBase64) {
            throw new Error("No encryption key found");
        }

        const keyBuffer = Uint8Array.from(atob(keyBase64), c => c.charCodeAt(0));
        const key = await window.crypto.subtle.importKey(
            "raw",
            keyBuffer,
            "AES-GCM",
            true,
            ["encrypt"]
        );

        // Generate IV
        const iv = window.crypto.getRandomValues(new Uint8Array(12));
        const encodedData = new TextEncoder().encode(JSON.stringify(data));

        const encryptedContent = await window.crypto.subtle.encrypt(
            {
                name: "AES-GCM",
                iv: iv
            },
            key,
            encodedData
        );

        return {
            encrypted: btoa(String.fromCharCode(...new Uint8Array(encryptedContent))),
            iv: btoa(String.fromCharCode(...iv))
        };
    }

    // Decrypt data
    async decryptData(encryptedData, iv, username) {
        const keyBase64 = await this.getKey(username);
        if (!keyBase64) {
            throw new Error("No encryption key found");
        }

        const keyBuffer = Uint8Array.from(atob(keyBase64), c => c.charCodeAt(0));
        const key = await window.crypto.subtle.importKey(
            "raw",
            keyBuffer,
            "AES-GCM",
            true,
            ["decrypt"]
        );

        const encryptedBuffer = Uint8Array.from(atob(encryptedData), c => c.charCodeAt(0));
        const ivBuffer = Uint8Array.from(atob(iv), c => c.charCodeAt(0));

        const decryptedContent = await window.crypto.subtle.decrypt(
            {
                name: "AES-GCM",
                iv: ivBuffer
            },
            key,
            encryptedBuffer
        );

        return JSON.parse(new TextDecoder().decode(decryptedContent));
    }
}