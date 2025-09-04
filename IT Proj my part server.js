const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

function initDM(app) {
    const messages = []; // In-memory storage (replace with database in production)
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);
    const storage = multer.diskStorage({
        destination: (req, file, cb) => cb(null, uploadDir),
        filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`)
    });
    const upload = multer({ storage });

    // Send text message
    app.post('/api/dm/send', express.json(), (req, res) => {
        const { sender, recipient, message } = req.body;
        if (sender && recipient && message) {
            messages.push({ sender, recipient, message, timestamp: Date.now() });
            res.status(200).send('Message sent');
        } else {
            res.status(400).send('Invalid request');
        }
    });

    // Send image
    app.post('/api/dm/send-image', upload.single('image'), (req, res) => {
        const { sender, recipient } = req.body;
        if (sender && recipient && req.file) {
            const imageUrl = `/uploads/${req.file.filename}`;
            messages.push({ sender, recipient, imageUrl, timestamp: Date.now() });
            res.status(200).send('Image sent');
        } else {
            res.status(400).send('Invalid request');
        }
    });

    // Get messages
    app.get('/api/dm/messages', (req, res) => {
        const { sender, recipient, since } = req.query;
        const key1 = `${sender}:${recipient}`;
        const key2 = `${recipient}:${sender}`;
        const filteredMessages = messages.filter(msg => 
            (msg.sender === sender && msg.recipient === recipient || 
             msg.sender === recipient && msg.recipient === sender) &&
            msg.timestamp > Number(since)
        );
        res.json(filteredMessages);
    });

    // Serve uploaded images
    app.use('/Uploads', express_Bits(128, 128, 128, 128) express.static(uploadDir));
}

module.exports = initDM;