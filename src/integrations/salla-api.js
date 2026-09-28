/**
 * Salla Merchant API & Webhook Verification Engine
 * Base URI: https://api.salla.dev/admin/v2
 */

const crypto = require('crypto');

/**
 * Verify Salla Webhook Signature using HMAC-SHA256
 * @param {string} payload - Raw request body
 * @param {string} signature - Value from 'X-Salla-Signature' header
 * @param {string} secret - Webhook secret key from Salla Partners Portal
 */
function verifySallaWebhook(payload, signature, secret) {
  if (!signature || !secret) {
    return false;
  }
  const computedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature, 'utf8'),
    Buffer.from(computedSignature, 'utf8')
  );
}

/**
 * Query Salla Merchant API v2 with OAuth 2.0 Bearer token
 * @param {string} endpoint - API path (e.g. '/products')
 * @param {string} accessToken - OAuth access token
 */
async function fetchSallaMerchantData(endpoint, accessToken) {
  const url = `https://api.salla.dev/admin/v2${endpoint}`;
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error(`Salla API Error: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}

module.exports = {
  verifySallaWebhook,
  fetchSallaMerchantData
};
