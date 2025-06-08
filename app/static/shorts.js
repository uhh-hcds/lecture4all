const iFrame = document.getElementById('currentIframe');
const metaDaten = document.querySelector('.meta-daten');
const videoButton = document.getElementById('videoButton');
const sideboard = document.querySelector('.sideboard');
const resultsJS = getResultsJS();

    document.getElementById('right').addEventListener('click', skipVideo);
    document.getElementById('left').addEventListener('click', videoBack);
    // Konfiguration
    const BASE_URL = 'https://lecture2go.uni-hamburg.de/o/iframe/?obj=';

    const chunks = resultsJS.flatMap(video =>
        video.chunks.map(chunk => ({
            url: `${BASE_URL}${video.video_id}/${Math.round(chunk.start)}/${Math.round(chunk.end)}`,
            videoId: video.video_id,
            title: video.title,
            speaker: video.speaker,
            date: video.date,
            text: chunk.text,
            rank: chunk.chunk_rank
        }))
    );

    // Chunks nach Rank sortieren
    const sortedChunks = chunks.sort((a, b) => a.rank - b.rank);

    let currentIndex = 0;

    // Aktualisieren des Iframes und Sideboards
    function updateUI(index) {
        const chunk = sortedChunks[index];
        iFrame.src = chunk.url;
        metaDaten.innerHTML = `<h5>${chunk.title}</h5><p>${chunk.speaker} <br> ${chunk.date}</p>`;
        videoButton.href = `${getVideoUrl()}?video_id=${chunk.videoId}`;
        sideboard.innerHTML = `<h3>${shortenTextIfNecessary(chunk.title, 50)}</h3><p>...${chunk.text}...</p>`;
    }
    updateUI(0);

    function skipVideo() {
        if (currentIndex < sortedChunks.length - 1) {
            currentIndex++;
            updateUI(currentIndex);
        }
    }

    function videoBack() {
        if (currentIndex > 0) {
            currentIndex--;
            updateUI(currentIndex);
        }
    }

    // Mobileview
    const MOVE_THRESHOLD = 100;

    let initialX = 0;
    let moveX = 0;
    let isDeleteButtonOpen = false;

    document.addEventListener("touchstart", e => {
        initialX = e.touches[0].pageX;
    });
    document.addEventListener("touchmove", e => {
        let currentX = e.touches[0].pageX;
        moveX = currentX - initialX;
    });
    document.addEventListener("touchend", e => {
        if (moveX < MOVE_THRESHOLD * (-1)) {
            // Swipe right
            skipVideo();
        } else if (moveX > MOVE_THRESHOLD ) {
            // Swipe left
            videoBack();
        }

        moveX = 0;
    });
