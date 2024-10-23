const ytdl = require('ytdl-core');
const fs = require('fs');
const readline = require('readline');

// Create an interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// Function to ask for the YouTube URL
function askForLink() {
  rl.question('Please enter the YouTube video URL: ', (videoUrl) => {
    // Validate URL format (simple validation)
    if (!ytdl.validateURL(videoUrl)) {
      console.log('Invalid YouTube URL. Please try again.');
      askForLink(); // Ask for the URL again
      return;
    }

    // Start downloading audio
    downloadAudio(videoUrl);
  });
}

// Function to download audio
function downloadAudio(videoUrl) {
  const output = fs.createWriteStream('audio.mp3');

  ytdl(videoUrl, { filter: 'audioonly' })
    .pipe(output)
    .on('finish', () => {
      console.log('Audio downloaded successfully!');
      rl.close(); // Close the readline interface after downloading
    })
    .on('error', (err) => {
      console.error('Error downloading audio:', err);
      rl.close(); // Close the readline interface in case of an error
    });

  // Handle stream errors
  output.on('error', (err) => {
    console.error('Error writing to file:', err);
    rl.close(); // Close the readline interface on write error
  });
}

// Start the process
askForLink();
