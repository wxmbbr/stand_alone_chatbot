const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the root directory
app.use(express.static(path.join(__dirname)));

// Handle the main route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Handle the homepage route
app.get('/homepage', (req, res) => {
    res.sendFile(path.join(__dirname, 'homepage-working', 'Home _ BBR Network.html'));
});

// Fallback for any other routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    console.log(`Homepage with chatbot available at: http://localhost:${PORT}/homepage`);
});
