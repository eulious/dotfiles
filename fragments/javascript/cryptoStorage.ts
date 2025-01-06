import CryptoJS from 'crypto-js';

const K = 'ZaCV02k8-OO2rRaZrfT4s6opxdGIaXAdigbYaEepfPM';
const IV = new Uint8Array([200, 35, 63, 0, 241, 214, 166, 176, 247, 83, 10, 48, 63, 118, 246, 81]);

export default class CryptoStorage {
  public async getKey() {
    const key = await crypto.subtle.importKey(
      'jwk',
      {
        alg: 'A256GCM',
        ext: true,
        k: K,
        key_ops: ['encrypt', 'decrypt'],
        kty: 'oct'
      },
      { name: 'AES-GCM' },
      false,
      ['encrypt', 'decrypt']
    );
    return key;
  }

  public async encrypt(s: string) {
    let encryptedArrayBuffer = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv: IV },
      await this.getKey(),
      new TextEncoder().encode(s)
    );
    let encryptedBytes = Array.from(new Uint8Array(encryptedArrayBuffer), (char) => String.fromCharCode(char)).join('');
    let encryptedBase64String = btoa(encryptedBytes);
    return encryptedBase64String;
  }

  public async decrypt(s: string) {
    let encryptedBase64String = s;
    let encryptedBytes = atob(encryptedBase64String);
    let encryptedData = Uint8Array.from(encryptedBytes.split(''), (char) => char.charCodeAt(0));

    let decryptedArrayBuffer = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: IV },
      await this.getKey(),
      encryptedData
    );
    return new TextDecoder().decode(new Uint8Array(decryptedArrayBuffer));
  }
}

const AES = 'password';
export function lsSave(key: string, word: string) {
  const mm = CryptoJS.AES.encrypt(word, AES).toString();
  localStorage[key] = mm;
}

export function lsLoad(key: string): string | undefined {
  const mm = localStorage[key];
  if (mm) return CryptoJS.AES.decrypt(mm, AES).toString(CryptoJS.enc.Utf8);
}
